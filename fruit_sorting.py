import cv2
import threading
import RPi.GPIO as GPIO
import time
import numpy as np
from edge_impulse_linux.image import ImageImpulseRunner

# ============================================================================
# 1. PERUNTUKAN PIN INPUT/OUTPUT (GPIO MAP - BROADCOM MODE)
# ============================================================================
# Pemacu Motor Stepper NEMA 23 via TB6600
PUL = 17                # Pin Fizikal 11 - Isyarat Denyutan Nadi (Kelajuan)
DIR = 27                # Pin Fizikal 13 - Tahap Voltan Arah Putaran (Direction)

# Aktuator & Penderia Isyarat Kit Latihan
SERVO = 18              # Pin Fizikal 12 - Isyarat Output PWM 50Hz (Sudut Lengan)
SENSOR_GATE_1 = 22      # Pin Fizikal 15 - Input Penderia IR Obstacle (Active LOW)

# Modul Geganti Tower Lamp Industri
RELAY_GREEN = 24        # Pin Fizikal 18 - Lampu Indikator Mesin Aktif (RUN)
RELAY_RED = 23          # Pin Fizikal 16 - Lampu Indikator Mesin Pegun (IDLE)

# Suis Tekan Panel Kawalan Manual
BUTTON_START = 16       # Pin Fizikal 36 - Suis Mula NO (Active LOW)

# ============================================================================
# 2. INASIALISASI PERKAKASAN DAN TETAPAN DAFTAR GPIO
# ============================================================================
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Konfigurasi Output Arus Tinggi & PWM
GPIO.setup([PUL, DIR, RELAY_GREEN, RELAY_RED], GPIO.OUT)
GPIO.setup(SERVO, GPIO.OUT)

# Konfigurasi Input Digital Menggunakan Perintang Pull-Up Dalaman (Internal Pull-Up)
GPIO.setup(SENSOR_GATE_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Mengaktifkan Isyarat Modulasi Lebar Pulsa (PWM) untuk Servo MG996R
pwm_servo = GPIO.PWM(SERVO, 50)
pwm_servo.start(0)

# Pembolehubah Status Utama Pengurusan Sistem (Global State Management)
latest_frame = None
is_running = True
system_activated = False   # Flag Status Aktivasi Sistem Keseluruhan
stepper_active = False      # Status Operasi Pemacu Stepper Motor
ai_result_text = "Sistem Idle"
system_status = "SYSTEM IDLE: TEKAN BUTANG START..." 
detected_fruit_memory = None  

# Bendera Perlindungan Interlock Anti-Double Trigger (Hybrid Security Flags)
is_scanning_lock = False
oren_timer_lock = 0

# ============================================================================
# 3. KAWASAN FOKUS VISI KOMPUTER (ROI - REGION OF INTEREST)
# ============================================================================
ROI_X, ROI_Y = 210, 190   
ROI_W, ROI_H = 250, 250 

LINE_Y = ROI_Y + (ROI_H // 2)
LINE_START_X = ROI_X
LINE_END_X = ROI_X + ROI_W

# Matriks Kod Warna BGR untuk Paparan Antaramuka Grafik (Industrial UI Theme)
C_BG = (15, 18, 25)
C_PANEL = (22, 28, 38)
C_CARD = (30, 38, 52)
C_LINE = (50, 60, 80)
C_ACTIVE = (0, 170, 255)
C_OK = (60, 220, 100)
C_ALERT = (0, 180, 255)
C_ERR = (50, 50, 220)
C_TXT = (230, 235, 245)
C_TXT2 = (160, 170, 190)
C_DIM = (100, 110, 130)
C_AMBER = (255, 170, 0)

# ============================================================================
# 4. SUB-THREAD KAWALAN MOTOR STEPPER (GENERASI DENYUTAN PULSE)
# ============================================================================
def stepper_thread():
    global stepper_active, is_running
    GPIO.output(DIR, GPIO.LOW) # Menetapkan arah putaran linear ke hadapan
    while is_running:
        if stepper_active:
            # Memancarkan Output Isyarat Lampu RUN dan Menghidupkan Nadi Motor
            GPIO.output(RELAY_GREEN, GPIO.LOW)  # Lampu Hijau Aktif
            GPIO.output(RELAY_RED, GPIO.HIGH)   # Lampu Merah Padam

            GPIO.output(PUL, GPIO.HIGH)
            time.sleep(0.009) 
            GPIO.output(PUL, GPIO.LOW)
            time.sleep(0.009)
        else:
            # Mengubah Status Papan Latihan ke Mod Sedia (IDLE Mode)
            GPIO.output(RELAY_GREEN, GPIO.HIGH) # Lampu Hijau Padam
            GPIO.output(RELAY_RED, GPIO.LOW)    # Lampu Merah Aktif
            time.sleep(0.1)

# ============================================================================
# 5. SUB-ROUTINE PEMANDU AKTUATOR SERVO (PENGASINGAN FIZIKAL GRED BUAH)
# ============================================================================
def open_gate(label):
    label_check = label.lower()
    if label_check == "apple":
        print(">>> ACTUATOR: OPENING GATE FOR APPLE <<<")
        pwm_servo.ChangeDutyCycle(12)  # Sudut 90 darjah lengan penolak objek
        time.sleep(1.2)
        pwm_servo.ChangeDutyCycle(0)   # Mematikan isyarat memegang untuk elak servo bergegar

def reset_gate():
    print(">>> ACTUATOR: CLOSING GATE (RESET) <<<")
    pwm_servo.ChangeDutyCycle(2)   # Kembali ke kedudukan asal (0 darjah)
    time.sleep(1.2)
    pwm_servo.ChangeDutyCycle(0)

# ============================================================================
# 6. THREAD ENJIN INFERENS EDGE AI & LOGIK PEMPROSESAN HIBRID
# ============================================================================
def ai_logic(model_path):
    global latest_frame, is_running, stepper_active, ai_result_text, system_status, detected_fruit_memory, system_activated
    global is_scanning_lock, oren_timer_lock

    with ImageImpulseRunner(model_path) as runner:
        runner.init()
        print("[SISTEM] Model .eim Berjaya Dimuatkan. Menunggu Isyarat Panel...")

        while is_running:
            # ------------------------------------------------------------
            # SEMAKAN PANEL 1: PENGESANAN ISYARAT BUTANG MULA (START SWITCH)
            # ------------------------------------------------------------
            if not system_activated:
                if GPIO.input(BUTTON_START) == GPIO.LOW:
                    print("[PANEL COMMAND] Isyarat START Diterima. Konveyor Beroperasi.")
                    time.sleep(0.5) 
                    system_activated = True
                    stepper_active = True
                    detected_fruit_memory = None
                    is_scanning_lock = False
                    ai_result_text = "Mencari..."
                    system_status = "READY: MENCARI BUAH..."

            # ------------------------------------------------------------
            # KONTROL TIMING: PELEPASAN KUNCI COOLDOWN KHAS UNTUK OREN (5 SAAT)
            # ------------------------------------------------------------
            if is_scanning_lock and detected_fruit_memory == "oren":
                if time.time() > oren_timer_lock:
                    detected_fruit_memory = None      
                    is_scanning_lock = False
                    ai_result_text = "Mencari..."
                    system_status = "READY: MENCARI BUAH..."
                    print("[SISTEM LOG] Pemasa 5s Oren Tamat. Mengaktifkan Semula Radar Imbasan Kamera.")

            # Fasa Pemprosesan Inferens AI Sekiranya Talian Konveyor Aktif
            if latest_frame is not None and system_activated:

                # ------------------------------------------------------------
                # FASA 1: VISI KOMPUTER & PENGIMBASAN MATRIKS MODEL AI
                # ------------------------------------------------------------
                if detected_fruit_memory is None and not is_scanning_lock:
                    roi_frame = latest_frame[ROI_Y:ROI_Y+ROI_H, ROI_X:ROI_X+ROI_W]
                    roi_resized = cv2.resize(roi_frame, (320, 320))
                    roi_rgb = cv2.cvtColor(roi_resized, cv2.COLOR_BGR2RGB)

                    features, _ = runner.get_features_from_image(roi_rgb)
                    res = runner.classify(features)

                    bboxes = []
                    if isinstance(res, dict):
                        if "bounding_boxes" in res:
                            bboxes = res["bounding_boxes"]
                        elif "result" in res and "bounding_boxes" in res["result"]:
                            bboxes = res["result"]["bounding_boxes"]

                    for bb in bboxes:
                        label = bb.get("label", "unknown").lower()
                        score = float(bb.get("confidence", bb.get("value", 0.0)))

                        if score > 0.60 and (label == "apple" or label == "oren"):
                            by = int(bb.get("y", 0))
                            bh = int(bb.get("height", 0))
                            MODEL_LINE_Y = 160 

                            # Logik Pengesanan Melintasi Garisan Visual (Trigger Line)
                            if by <= MODEL_LINE_Y <= (by + bh):
                                # Rejam Isyarat Serta-merta untuk Elak Ralat Pengesanan Bertindih
                                is_scanning_lock = True 
                                stepper_active = False 

                                print(f"[CAM TRIGGER] Peranti {label.upper()} Memotong Garisan. Memulakan Analisis...")
                                system_status = f"{label.upper()} BERHENTI (MULA IMBASAN AI)"
                                ai_result_text = "SCANNING..."
                                time.sleep(1.5) # Jeda Masa untuk Penilaian Matriks AI

                                ai_result_text = f"{label.upper()} ({int(score*100)}%)"

                                # --- PROSEDUR PENGASINGAN ALIRAN LOGIK HIBRID ---
                                if label == "oren":
                                    print(f"[LOGIK LOG] Buah Oren Sah. Mengunci Sistem Selama 5 Saat.")
                                    detected_fruit_memory = "oren"
                                    system_status = "BUAH: OREN // MELUNCUR JALAN TERUS..."
                                    stepper_active = True 
                                    oren_timer_lock = time.time() + 5.0 # Pendaftaran Pemasa Perlindungan

                                elif label == "apple":
                                    print(f"[LOGIK LOG] Buah Apple Sah. Mengunci Sehingga Trigger Isyarat IR.")
                                    detected_fruit_memory = "apple" 
                                    system_status = "BUAH: APPLE // MENUJU KE SENSOR GATE 1..."
                                    stepper_active = True 

                                break

                # ------------------------------------------------------------
                # FASA 2: MAKLUM BALAS SENSOR FIZIKAL (PELEPASAN KUNCI SENSOR UNTUK APPLE)
                # ------------------------------------------------------------
                if detected_fruit_memory == "apple" and (GPIO.input(SENSOR_GATE_1) == GPIO.LOW):
                    print("[SENSOR TRIGGER] Isyarat IR Terputus. Mengaktifkan Lengan Penolak Servo...")
                    stepper_active = False # Memberhentikan Tali Sawat Semasa Proses Penyisihan Fizikal
                    system_status = "SENSOR 1 KENA: MEMBUKA GATE APPLE..."

                    open_gate("apple") 
                    time.sleep(3.0) # Pemasa Menunggu Objek Ditendang Masuk ke Slot Gred   
                    reset_gate()                       

                    # Pembersihan Daftar Kunci bagi Persediaan Objek Seterusnya
                    detected_fruit_memory = None      
                    is_scanning_lock = False
                    ai_result_text = "Mencari..."
                    stepper_active = True             

                    for i in range(3, 0, -1):
                        system_status = f"SEDIA UNTUK BUAH SETERUSNYA DALAM: {i}s"
                        time.sleep(1.0)

                    if system_activated:
                        system_status = "READY: MENCARI BUAH..."

            time.sleep(0.01) # Kadar Kitaran Polling Ringan (10ms) untuk Kestabilan CPU Pi

# ============================================================================
# 7. PROGRAM UTAMA (PENGURUSAN ANTARAMUKA GRAFIK OPENCV MONITORS)
# ============================================================================
def main():
    global latest_frame, is_running, ai_result_text, system_status, stepper_active, system_activated

    modelfile = "/home/iskandar/buahaiv4.eim" 
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("[RALAT CRITICAL] Gagal Mengakses Pangkalan Data Kamera USB!")
        return

    # Melancarkan Pengurusan Tugasan Serentak (Multi-Threading Deployment)
    threading.Thread(target=stepper_thread, daemon=True).start()
    threading.Thread(target=ai_logic, args=(modelfile,), daemon=True).start()

    print("--- SISTEM INFERENS INTEGRASI KORPORAT SELESAI ---")
    camera_error_count = 0

    while is_running:
        ret, frame = cap.read()
        if not ret: 
            camera_error_count += 1
            time.sleep(0.1)
            if camera_error_count > 10: break
            continue

        camera_error_count = 0
        latest_frame = frame.copy()

        is_active = system_activated

        # --- Melukis Komponen Atas (Top Slim Status Bar) ---
        accent = C_OK if is_active else C_ERR
        cv2.rectangle(frame, (0, 0), (640, 40), C_PANEL, -1)
        cv2.line(frame, (0, 40), (640, 40), accent, 2)

        # Animasi Lampu LED Status Dinamik
        cv2.circle(frame, (18, 20), 6, accent, -1)
        cv2.circle(frame, (18, 20), 8, accent, 1)

        # Logik Penukaran Teks Penerangan Grafik
        if not is_active:
            txt = "STANDBY - Press START"
            col = C_TXT2
        elif "READY" in system_status:
            txt = "SCANNING FOR FRUIT..."
            col = C_OK
        elif "BERHENTI" in system_status or "SENSOR" in system_status:
            txt = "PROCESSING..."
            col = C_ALERT
        elif "MELUNCUR" in system_status or "MENUJU" in system_status:
            txt = "CONVEYOR RUNNING"
            col = C_ACTIVE
        else:
            txt = system_status
            col = C_TXT

        cv2.putText(frame, txt, (35, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.55, col, 2)

        # Paparan Mod Operasi Badge
        mode = "AUTO" if is_active else "MANUAL"
        mcol = C_OK if is_active else C_DIM
        ts = cv2.getTextSize(mode, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)[0]
        cv2.rectangle(frame, (620-ts[0]-10, 8), (630, 32), mcol, -1)
        cv2.putText(frame, mode, (625-ts[0]-5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_BG, 1)

        # --- Melukis Komponen Tengah (Neon Style ROI Box Display) ---
        roi_color = C_ACTIVE if is_active else C_DIM
        scan_color = C_AMBER if is_active else C_DIM

        for i in range(3, 0, -1):
            glow = tuple(int(c * 0.15 + 15 * 0.85) for c in roi_color)
            cv2.rectangle(frame, (ROI_X-i, ROI_Y-i), (ROI_X+ROI_W+i, ROI_Y+ROI_H+i), glow, 1)

        cv2.rectangle(frame, (ROI_X, ROI_Y), (ROI_X+ROI_W, ROI_Y+ROI_H), roi_color, 2)

        # Melukis Penjuru Sempadan Kotak Ticks
        tick = 18
        cv2.line(frame, (ROI_X, ROI_Y), (ROI_X+tick, ROI_Y), roi_color, 2)
        cv2.line(frame, (ROI_X, ROI_Y), (ROI_X, ROI_Y+tick), roi_color, 2)
        cv2.line(frame, (ROI_X+ROI_W, ROI_Y), (ROI_X+ROI_W-tick, ROI_Y), roi_color, 2)
        cv2.line(frame, (ROI_X+ROI_W, ROI_Y), (ROI_X+ROI_W, ROI_Y+tick), roi_color, 2)
        cv2.line(frame, (ROI_X, ROI_Y+ROI_H), (ROI_X+tick, ROI_Y+ROI_H), roi_color, 2)
        cv2.line(frame, (ROI_X, ROI_Y+ROI_H), (ROI_X, ROI_Y+ROI_H-tick), roi_color, 2)
        cv2.line(frame, (ROI_X+ROI_W, ROI_Y+ROI_H), (ROI_X+ROI_W-tick, ROI_Y+ROI_H), roi_color, 2)
        cv2.line(frame, (ROI_X+ROI_W, ROI_Y+ROI_H), (ROI_X+ROI_W, ROI_Y+ROI_H-tick), roi_color, 2)

        # Melukis Garisan Laser Sensor Maya (Virtual Laser Alignment)
        scan_y = LINE_Y
        cv2.line(frame, (LINE_START_X, scan_y), (LINE_END_X, scan_y), scan_color, 2)
        cv2.line(frame, (LINE_START_X, scan_y-6), (LINE_START_X, scan_y+6), scan_color, 2)
        cv2.line(frame, (LINE_END_X, scan_y-6), (LINE_END_X, scan_y+6), scan_color, 2)

        # Label Kotak Imbasan Visual
        cv2.rectangle(frame, (ROI_X, ROI_Y-22), (ROI_X+120, ROI_Y), roi_color, -1)
        cv2.putText(frame, "SCAN AREA", (ROI_X+8, ROI_Y-6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, C_BG, 1)

        # --- Melukis Animasi Status Pergerakan Belt Tali Sawat ---
        belt_y = ROI_Y + ROI_H + 8
        cv2.rectangle(frame, (ROI_X, belt_y), (ROI_X+ROI_W, belt_y+4), C_LINE, -1)
        if stepper_active:
            cv2.rectangle(frame, (ROI_X+ROI_W//2-10, belt_y-2), (ROI_X+ROI_W//2+10, belt_y+6), C_OK, -1)
            cv2.putText(frame, ">>", (ROI_X+ROI_W//2-8, belt_y+4), cv2.FONT_HERSHEY_SIMPLEX, 0.3, C_BG, 1)
        else:
            cv2.rectangle(frame, (ROI_X+ROI_W//2-10, belt_y-2), (ROI_X+ROI_W//2+10, belt_y+6), C_ERR, -1)
            cv2.putText(frame, "X", (ROI_X+ROI_W//2-3, belt_y+4), cv2.FONT_HERSHEY_SIMPLEX, 0.3, C_BG, 1)

        # --- Melukis Kad Data Klasifikasi (Glassmorphism-Inspired Bottom Card) ---
        show_card = (detected_fruit_memory is not None or
                     not stepper_active or
                     not is_active or
                     "OREN" in system_status)

        if show_card:
            card_y = 370
            overlay = frame.copy()
            cv2.rectangle(overlay, (30, card_y), (610, card_y+90), C_CARD, -1)
            cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)

            if "BERHENTI" in system_status or "SENSOR" in system_status:
                bcol = C_ALERT
            elif not is_active:
                bcol = C_DIM
            elif "OREN" in system_status:
                bcol = C_ALERT
            else:
                bcol = C_LINE

            cv2.rectangle(frame, (30, card_y), (610, card_y+90), bcol, 1)

            ai = ai_result_text
            if "APPLE" in ai:
                acol = C_OK
                sym = "[APPLE]"
            elif "OREN" in ai:
                acol = C_ALERT
                sym = "[OREN]"
            elif "SCANNING" in ai:
                acol = C_ACTIVE
                sym = "[...]"
            else:
                acol = C_TXT
                sym = "[IDLE]"

            cv2.putText(frame, f"{sym} {ai}", (50, card_y+35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, acol, 2)
            cv2.putText(frame, f"LIVE LOG: {system_status}", (50, card_y+60), cv2.FONT_HERSHEY_SIMPLEX, 0.45, C_TXT2, 1)

            # Bulatan Isyarat Sub-Komponen Fizikal (Sub-Component Diagnostic LEDs)
            ccol = C_OK if stepper_active else C_DIM
            cv2.circle(frame, (520, card_y+35), 4, ccol, -1)
            cv2.putText(frame, "CONV", (530, card_y+38), cv2.FONT_HERSHEY_SIMPLEX, 0.3, C_TXT2, 1)

            gcol = C_ALERT if detected_fruit_memory == 'apple' else C_DIM
            cv2.circle(frame, (520, card_y+55), 4, gcol, -1)
            cv2.putText(frame, "GATE", (530, card_y+58), cv2.FONT_HERSHEY_SIMPLEX, 0.3, C_TXT2, 1)

        # --- Kapsyen Institusi & Label Diagnostik Perkakasan Manual (Footer) ---
        cv2.putText(frame, "ADTEC BP // MECHATRONICS FYP V5.8", (420, 472), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_DIM, 1)

        start_state = "LOW(PRS)" if GPIO.input(BUTTON_START) == GPIO.LOW else "HIGH"
        cv2.putText(frame, f"START SWITCH: {start_state} | QUIT: PRESS 'q'", (20, 472), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_DIM, 1)

        cv2.imshow('SISTEM SORTING ADTEC BP', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            is_running = False
            break

    # Penutupan Kuasa Keselamatan Am (General Hardware Fail-Safe Shutdown)
    GPIO.output(PUL, GPIO.LOW)
    GPIO.output(DIR, GPIO.LOW)
    GPIO.output(RELAY_GREEN, GPIO.HIGH)
    GPIO.output(RELAY_RED, GPIO.HIGH)
    pwm_servo.stop()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Semua I/O dinonaktifkan dengan selamat.")

if __name__ == "__main__":
    main()
