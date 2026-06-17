[README (1).md](https://github.com/user-attachments/files/29032143/README.1.md)
# 🍏 Autonomous Fruit Sorting: End-to-End Edge AI Deployment Guide

<p align="center">
  <img src="https://img.shields.io/badge/Edge%20AI-Offline%20Inference-10b981?style=for-the-badge&logo=raspberry-pi&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-Raspberry%20Pi%204-C51A4A?style=for-the-badge&logo=raspberry-pi&logoColor=white" />
  <img src="https://img.shields.io/badge/SDK-Edge%20Impulse-06b6d4?style=for-the-badge&logo=edge-impulse&logoColor=white" />
  <img src="https://img.shields.io/badge/Model-MobileNetV2--SSD-ff6b6b?style=for-the-badge&logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/Latency-31ms-10b981?style=for-the-badge&logo=clockify&logoColor=white" />
</p>

> **Dokumentasi lengkap** bermula daripada fasa pengumpulan data imej (*Data Acquisition*) di **Edge Impulse Studio**, proses latihan model (*Training*), sehinggalah fasa *deployment* secara **100% Luar Talian (Offline Inference)** di dalam persekitaran maya (*Virtual Environment*) **Raspberry Pi 4** menggunakan **Thonny IDE**.

---

## 📑 Jadual Kandungan

1. [Fasa 1: Pengurusan Data & Latihan Model (Edge Impulse)](#-fasa-1-pengurusan-data--latihan-model-edge-impulse)
   - [Langkah 1: Pengumpulan Data Imej](#langkah-1-pengumpulan-data-imej-data-acquisition)
   - [Langkah 2: Konfigurasi Impulse](#langkah-2-konfigurasi-impulse-impulse-design)
   - [Langkah 3: Latihan Model & Pengesahan Ketepatan](#langkah-3-latihan-model--pengesahan-ketepatan-training--validation)
   - [Langkah 4: Eksport Fail Model (.eim)](#langkah-4-eksport-fail-model-eim)
2. [Fasa 2: Deployment & Koding (Raspberry Pi 4)](#-fasa-2-deployment--koding-raspberry-pi-4)
   - [Langkah 5: Pindahan Fail .eim](#langkah-5-pindahan-fail-eim-menggunakan-pendrive)
   - [Langkah 6: Bina & Aktifkan Persekitaran Maya (venv)](#langkah-6-bina-dan-aktifkan-persekitaran-maya-venv)
   - [Langkah 7: Pasang Pustaka Dependensi](#langkah-7-pasang-pustaka-dependensi-di-dalam-venv)
   - [Langkah 8: Beri Kebenaran Akses Fail Binari](#langkah-8-beri-kebenaran-akses-fail-binari-chmod)
   - [Langkah 9: Konfigurasi Interpreter di Thonny IDE](#langkah-9-konfigurasi-interpreter-di-thonny-ide)
   - [Langkah 10: Jalankan Skrip Python](#langkah-10-jalankan-skrip-python-anda)
3. [Struktur Folder Projek](#-struktur-folder-projek)
4. [Penjelasan Kod Python (Syntax-by-Syntax)](#-penjelasan-kod-python-syntax-by-syntax)
   - [Bahagian 1: Import & Peruntukan Pin GPIO](#bahagian-1-import--peruntukan-pin-gpio)
   - [Bahagian 2: Inisialisasi Perkakasan](#bahagian-2-inisialisasi-perkakasan)
   - [Bahagian 3: Kawasan Fokus Visi Komputer (ROI)](#bahagian-3-kawasan-fokus-visi-komputer-roi)
   - [Bahagian 4: Thread Stepper Motor](#bahagian-4-thread-stepper-motor)
   - [Bahagian 5: Sub-Routine Servo](#bahagian-5-sub-routine-servo)
   - [Bahagian 6: Thread Enjin Inferens AI](#bahagian-6-thread-enjin-inferens-ai)
   - [Bahagian 7: Program Utama (OpenCV UI)](#bahagian-7-program-utama-opencv-ui)
5. [Nota Industri & Penutup](#-nota-industri--penutup)

---

## 🛑 FASA 1: Pengurusan Data & Latihan Model (Edge Impulse)

### Langkah 1: Pengumpulan Data Imej (Data Acquisition)

1. Log masuk ke akaun **Edge Impulse Studio** melalui pelayar web dan cipta projek baharu.
2. Sediakan kamera (telefon pintar atau USB webcam yang disambungkan pada laptop / Raspberry Pi).
3. Di dalam Edge Impulse, pergi ke menu **Data Acquisition**.
4. Pilih **Collect Data** dan ambil gambar buah (contoh: Apple dan Oren) dari **pelbagai sudut, jarak, dan variasi pencahayaan** yang ada di dalam makmal ADTEC. Ini pentuk untuk memastikan model tidak mengalami ralat *overfitting*.
5. Ambil sekurang-kurangnya **100–200 gambar** untuk setiap kelas buah.
6. Lakukan **pelabelan objek** (*Bounding Box Labelling*) pada setiap gambar dengan melukis kotak tepat pada kedudukan buah dan berikan nama label (contoh: `Apple` atau `Orange`).
7. Pastikan pembahagian data (*Data Split*) berada pada nisbah:

| Jenis Data | Peratusan |
|------------|-----------|
| Training Data | **80%** |
| Testing Data | **20%** |

> 💡 **Tip:** Variasi pencahayaan dan sudut gambar yang tinggi akan meningkatkan keupayaan model untuk mengenal pasti objek dalam persekitaran sebenar.

---

### Langkah 2: Konfigurasi Impulse (Impulse Design)

1. Navigasi ke menu **Impulse Design** → **Create Impulse**.
2. Di bahagian **Input Blocks**, tetapkan saiz imej kepada **`160 × 160` piksel**. Saiz ini merupakan optimum untuk pemprosesan laju pada Raspberry Pi 4.
3. Di bahagian **Processing Blocks**, tambah blok **Image** (berfungsi untuk menukar piksel warna RGB imej kepada ciri-ciri matrik matematik).
4. Di bahagian **Learning Blocks**, tambah blok **Object Detection (Images)** yang menggunakan algoritma rangkaian neural **MobileNetV2-SSD**.
5. Klik **Save Impulse**.

| Parameter | Nilai | Keterangan |
|-----------|-------|------------|
| Saiz Imej | `160 × 160` px | Optimum untuk Raspberry Pi 4 |
| Processing Block | Image | Penukaran RGB ke matrik ciri |
| Learning Block | Object Detection | MobileNetV2-SSD |

---

### Langkah 3: Latihan Model & Pengesahan Ketepatan (Training & Validation)

1. Pergi ke sub-menu **Image** di sebelah kiri, klik tab *Generate Features* dan klik butang **Generate Features**. Proses ini mengekstrak data visual menjadi kluster matrik data.
2. Pergi ke sub-menu **Object Detection**, tetapkan parameter latihan seperti berikut:

| Parameter | Nilai | Keterangan |
|-----------|-------|------------|
| *Number of epochs* | `50` – `100` | Kitaran latihan model |
| *Learning rate* | `0.001` | Kelajuan perubahan berat neural |

3. Klik **Start Training**.
4. Setelah selesai, perhatikan nilai **Validation Accuracy (Precision & Recall %)**. Pastikan graf *accuracy* stabil dan memuaskan sebelum meneruskan ke fasa deployment.

> ⚠️ **Perhatian:** Jika *accuracy* rendah atau graf tidak menunjukkan peningkatan, pertimbangkan untuk menambah data latihan atau melaraskan parameter *learning rate*.

---

### Langkah 4: Eksport Fail Model (.eim)

1. Pergi ke menu **Deployment** di sebelah kiri pelayar web.
2. Di bawah segmen *Target Device*, cari dan pilih **Raspberry Pi 4**.
3. Di bahagian bawah halaman, pilih optimasi **Quantized (int8)** untuk mendapatkan kelajuan pemprosesan maksimum (*low latency*).
   - Format *int8* menukarkan nilai matematik apungan (*float32*) kepada integer 8-bit.
   - Ini sangat kritikal untuk menurunkan masa kelewatan inferens (*inference latency*) kepada **~31 ms** pada Raspberry Pi 4.
4. Klik butang **Build**.
5. Tunggu sehingga proses kompilasi selesai. Pelayar web akan memuat turun sebuah fail binari tanpa format biasa bernama **`buahaiv4.eim`** ke dalam folder *Downloads* laptop anda.

---

## ⚙️ FASA 2: Deployment & Koding (Raspberry Pi 4)

### Langkah 5: Pindahan Fail `.eim` Menggunakan Pendrive

1. Selepas fail `buahaiv4.eim` selesai dimuat turun ke dalam folder *Downloads* di laptop, ambil sebuah **pendrive**.
2. Cucuk pendrive tersebut pada port USB laptop.
3. Buka *File Explorer*, salin (*copy*) fail `buahaiv4.eim` dari folder *Downloads*, dan tampal (*paste*) ke dalam storan pendrive.
4. Lakukan proses *Eject* pendrive dengan selamat dari laptop, kemudian cabut pendrive.
5. Hidupkan **Raspberry Pi 4** dan buka **File Manager**.
6. Di dalam direktori utama user iaitu `/home/pi/`, **cipta satu folder baharu** dan namakan sebagai `Fruit_Sorting_Project`.
   - Folder ini akan memegang fail kod Python, fail model, dan persekitaran maya (`venv`) anda.
7. Cucuk pendrive pada port USB Raspberry Pi 4 (disyorkan port **USB 3.0 berwarna biru** untuk pindahan lebih laju).
8. Buka direktori pendrive di dalam File Manager Raspberry Pi, salin fail `buahaiv4.eim`, dan tampal ke dalam folder `/home/pi/Fruit_Sorting_Project/`.

---

### Langkah 6: Bina dan Aktifkan Persekitaran Maya (venv)

> 📌 **Mengapa venv diperlukan?**  
> Sistem operasi Raspberry Pi yang baharu (Debian Bookworm ke atas) **mewajibkan** penggunaan *Virtual Environment* (`venv`) untuk mengelakkan ralat sistem `externally-managed-environment` semasa memasang pustaka luar menggunakan perintah `pip`.

1. Buka **Terminal** di Raspberry Pi.
2. Navigasi masuk ke dalam folder projek:

```bash
cd /home/pi/Fruit_Sorting_Project
```

3. Bina persekitaran maya baharu di dalam folder tersebut dan namakan sebagai `env`:

```bash
python3 -m venv env
```

4. Aktifkan persekitaran maya tersebut. Selepas diaktifkan, indikator `(env)` akan muncul di bahagian paling hadapan baris Terminal, menandakan persekitaran telah terisolasi dengan selamat:

```bash
source env/bin/activate
```

> ✅ Anda akan melihat prompt Terminal bertukar kepada: `(env) pi@raspberrypi:~/Fruit_Sorting_Project $`

---

### Langkah 7: Pasang Pustaka Dependensi (Di Dalam venv)

> ⚠️ **Pastikan Terminal anda masih memaparkan status aktif `(env)` sebelum menjalankan arahan di bawah.**

Jalankan arahan berikut mengikut turutan untuk memasang OpenCV dan Edge Impulse Linux Python SDK:

**1. Kemas kini pengurus pakej `pip`:**

```bash
pip install --upgrade pip setuptools wheel
```

**2. Pasang pustaka OpenCV untuk pemprosesan imej dan kamera:**

```bash
pip install opencv-python
```

**3. Pasang Edge Impulse Linux Python SDK rasmi:**

```bash
pip install edge-impulse-linux
```

| Pustaka | Fungsi |
|---------|--------|
| `pip`, `setuptools`, `wheel` | Pengurus pakej Python yang dikemas kini |
| `opencv-python` | Pemprosesan imej dan penstriman kamera |
| `edge-impulse-linux` | SDK rasmi untuk menjalankan model `.eim` secara lokal |

---

### Langkah 8: Beri Kebenaran Akses Fail Binari (Chmod)

Secara lalai, sistem operasi Linux akan menyekat fail binari luar (fail `.eim`) daripada dieksekusi atas faktor keselamatan. Anda **wajib** menukar status fail ini kepada jenis "boleh laku" (*executable*).

Jalankan arahan ini di Terminal:

```bash
chmod +x buahaiv4.eim
```

> 🔒 **Penjelasan:** `chmod +x` memberikan kebenaran *execute* kepada fail binari, membolehkan Edge Impulse SDK untuk memuatkan dan menjalankan model neural di dalam CPU Raspberry Pi 4.

---

### Langkah 9: Konfigurasi Interpreter di Thonny IDE

Supaya Thonny IDE boleh mengesan pustaka yang telah dipasang di dalam persekitaran maya (`env`) dan mengelakkan ralat `ModuleNotFoundError`, ikut tetapan interpreter berikut:

1. Buka perisian **Thonny IDE** pada Raspberry Pi 4.
2. Di menu atas, klik pada **Tools → Options...**
3. Pilih tab **Interpreter**.
4. Pada menu lungsur (*dropdown*), pilih **Alternative Python 3 interpreter or virtual environment**.
5. Klik butang tiga titik `...` di sebelah kanan ruang *Details* untuk mencari laluan interpreter secara manual.
6. Navigasi masuk ke dalam folder projek:
   ```
   /home/pi/Fruit_Sorting_Project/
   ```
   - Pilih folder `env`
   - Masuk ke folder `bin`
   - Pilih fail executable bernama `python3` atau `python`
7. **Laluan mutlak (Absolute Path):**
   ```
   /home/pi/Fruit_Sorting_Project/env/bin/python3
   ```
8. Klik **OK** dan klik **OK** sekali lagi untuk menyimpan konfigurasi.
9. Perhatikan status di penjuru bawah kanan skrin Thonny — kini memaparkan persekitaran maya `(env)` anda sedang aktif.

---

### Langkah 10: Jalankan Skrip Python Anda

1. Sediakan skrip Python utama anda (skrip kawalan konveyor dan kamera) dan simpan di dalam folder yang sama:
   ```
   /home/pi/Fruit_Sorting_Project/
   ```
   - Contoh nama fail: `skrip_projek.py`

2. Pastikan di dalam kod tersebut, anda memanggil modul `ImageImpulseRunner` untuk memuatkan fail model `buahaiv4.eim` secara lokal:

```python
from edge_impulse_linux.image import ImageImpulseRunner

modelfile = "/home/pi/Fruit_Sorting_Project/buahaiv4.eim"
runner = ImageImpulseRunner(modelfile)
```

3. Di dalam Thonny, buka fail `skrip_projek.py` tersebut dan tekan butang **Run Current Script** (ikon bulat hijau dengan anak panah putih, atau tekan kekunci `F5`).

4. Hasil pulangan (*return value*) daripada inferens fail `.eim` adalah data berformat **JSON** yang mengandungi:
   - `label` — nama kelas objek yang dikenal pasti
   - `value` — tahap keyakinan (*confidence score*)

5. Gunakan logik `if-else` dalam kod anda untuk menghantar isyarat pemicu (*trigger*) ke pin GPIO bagi menggerakkan perkakasan mekatronik fizikal (seperti motor servo atau motor stepper) tepat pada waktunya.

6. Untuk menghentikan sistem dengan selamat, tekan kekunci **`q`** pada papan kekunci untuk menyahtugaskan (*cleanup*) keseluruhan penstriman OpenCV dan pin GPIO.

---

## 📁 Struktur Folder Projek

```
/home/pi/Fruit_Sorting_Project/
│
├── env/                          # Persekitaran maya (venv)
│   ├── bin/
│   ├── lib/
│   └── ...
│
├── buahaiv4.eim                  # Fail model Edge Impulse (quantized int8)
│
├── skrip_projek.py               # Skrip Python utama (kawalan kamera + konveyor)
│
└── README.md                     # Dokumentasi projek (fail ini)
```

---

## 🐍 Penjelasan Kod Python (Syntax-by-Syntax)

> **Fail utama:** `skrip_projek.py`  
> **Bahasa:** Python 3  
> **Platform:** Raspberry Pi 4 (Debian Bookworm)  
> **IDE:** Thonny IDE dengan interpreter venv

---

### Bahagian 1: Import & Peruntukan Pin GPIO

```python
import cv2
import threading
import RPi.GPIO as GPIO
import time
import numpy as np
from edge_impulse_linux.image import ImageImpulseRunner
```

| Pustaka | Fungsi |
|---------|--------|
| `cv2` | OpenCV — pemprosesan imej, kamera, dan antaramuka grafik (GUI) |
| `threading` | Multi-threading — menjalankan tugas serentak (stepper + AI + kamera) |
| `RPi.GPIO` | Kawalan pin GPIO Raspberry Pi untuk input/output perkakasan |
| `time` | Pengurusan masa, jeda (*delay*), dan pemasa (*timer*) |
| `numpy` | Pengendalian matrik data (walaupun tidak digunakan secara langsung, biasanya diperlukan oleh OpenCV) |
| `ImageImpulseRunner` | Kelas utama Edge Impulse SDK untuk memuatkan model `.eim` dan menjalankan inferens imej |

```python
# ============================================================================
# 1. PERUNTUKAN PIN INPUT/OUTPUT (GPIO MAP - BROADCOM MODE)
# ============================================================================
```
> **Broadcom (BCM)** adalah sistem penomboran pin berdasarkan chip Broadcom BCM2835/6/7. Nombor pin ini merujuk kepada saluran GPIO sebenar di dalam chip, bukan nombor fizikal pada board.

```python
# Pemacu Motor Stepper NEMA 23 via TB6600
PUL = 17                # Pin Fizikal 11 - Isyarat Denyutan Nadi (Kelajuan)
DIR = 27                # Pin Fizikal 13 - Tahap Voltan Arah Putaran (Direction)
```
| Pembolehubah | Pin BCM | Pin Fizikal | Fungsi |
|-------------|---------|-------------|--------|
| `PUL` | GPIO 17 | Pin 11 | Denyutan kelajuan stepper motor |
| `DIR` | GPIO 27 | Pin 13 | Arah putaran stepper motor (LOW = ke hadapan) |

> **TB6600** adalah *driver* stepper motor yang menerima isyarat digital (PUL + DIR) untuk mengawal motor NEMA 23.

```python
# Aktuator & Penderia Isyarat Kit Latihan
SERVO = 18              # Pin Fizikal 12 - Isyarat Output PWM 50Hz (Sudut Lengan)
SENSOR_GATE_1 = 22      # Pin Fizikal 15 - Input Penderia IR Obstacle (Active LOW)
```
| Pembolehubah | Pin BCM | Pin Fizikal | Fungsi |
|-------------|---------|-------------|--------|
| `SERVO` | GPIO 18 | Pin 12 | Output PWM 50Hz untuk servo MG996R |
| `SENSOR_GATE_1` | GPIO 22 | Pin 15 | Input sensor IR obstacle (aktif LOW = objek dikesan) |

> **PWM 50Hz** adalah frekuensi standard untuk servo motor. *Duty cycle* menentukan sudut lengan (2% = 0°, 12% = 90°).

```python
# Modul Geganti Tower Lamp Industri
RELAY_GREEN = 24        # Pin Fizikal 18 - Lampu Indikator Mesin Aktif (RUN)
RELAY_RED = 23          # Pin Fizikal 16 - Lampu Indikator Mesin Pegun (IDLE)
```
| Pembolehubah | Pin BCM | Pin Fizikal | Fungsi |
|-------------|---------|-------------|--------|
| `RELAY_GREEN` | GPIO 24 | Pin 18 | Relay lampu hijau (mesin aktif) |
| `RELAY_RED` | GPIO 23 | Pin 16 | Relay lampu merah (mesin pegun) |

> **Tower Lamp** adalah lampu isyarat industri 3-warna. Di sini hanya gunakan 2 warna (hijau + merah) untuk status sistem.

```python
# Suis Tekan Panel Kawalan Manual
BUTTON_START = 16       # Pin Fizikal 36 - Suis Mula NO (Active LOW)
```
| Pembolehubah | Pin BCM | Pin Fizikal | Fungsi |
|-------------|---------|-------------|--------|
| `BUTTON_START` | GPIO 16 | Pin 36 | Suis tekan *Normally Open* (NO) — aktif LOW apabila ditekan |

---

### Bahagian 2: Inisialisasi Perkakasan

```python
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
```
| Syntax | Maksud |
|--------|--------|
| `GPIO.setmode(GPIO.BCM)` | Tetapkan mod penomboran pin kepada Broadcom (menggunakan nombor GPIO, bukan nombor fizikal) |
| `GPIO.setwarnings(False)` | Matikan amaran Python jika pin telah digunakan oleh proses lain |

```python
# Konfigurasi Output Arus Tinggi & PWM
GPIO.setup([PUL, DIR, RELAY_GREEN, RELAY_RED], GPIO.OUT)
GPIO.setup(SERVO, GPIO.OUT)
```
| Syntax | Maksud |
|--------|--------|
| `GPIO.setup(pin, GPIO.OUT)` | Tetapkan pin sebagai **output** (menghantar isyarat keluar ke perkakasan) |
| `GPIO.setup([...], GPIO.OUT)` | Boleh konfigurasi multiple pin serentak menggunakan senarai (*list*) |

```python
# Konfigurasi Input Digital Menggunakan Perintang Pull-Up Dalaman
GPIO.setup(SENSOR_GATE_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)
```
| Syntax | Maksud |
|--------|--------|
| `GPIO.setup(pin, GPIO.IN)` | Tetapkan pin sebagai **input** (menerima isyarat dari sensor/suis) |
| `pull_up_down=GPIO.PUD_UP` | Aktifkan perintang *pull-up* dalaman — pin akan sentiasa HIGH sehingga disambungkan ke GND (Active LOW) |

> **Active LOW** bermaksud isyarat dianggap "aktif" apabila pin jatuh ke 0V (GND). Ini lebih selamat kerana *short circuit* ke GND tidak merosakkan pin.

```python
# Mengaktifkan Isyarat Modulasi Lebar Pulsa (PWM) untuk Servo MG996R
pwm_servo = GPIO.PWM(SERVO, 50)
pwm_servo.start(0)
```
| Syntax | Maksud |
|--------|--------|
| `GPIO.PWM(pin, frekuensi)` | Cipta objek PWM pada pin tertentu dengan frekuensi tertentu (Hz) |
| `50` | Frekuensi 50Hz = 20ms per kitaran (standard untuk servo) |
| `.start(0)` | Mula PWM dengan *duty cycle* 0% (servo dalam keadaan rehat) |

```python
# Pembolehubah Status Utama Pengurusan Sistem (Global State Management)
latest_frame = None
is_running = True
system_activated = False   # Flag Status Aktivasi Sistem Keseluruhan
stepper_active = False      # Status Operasi Pemacu Stepper Motor
ai_result_text = "Sistem Idle"
system_status = "SYSTEM IDLE: TEKAN BUTANG START..." 
detected_fruit_memory = None  
```
| Pembolehubah | Jenis | Maksud |
|-------------|-------|--------|
| `latest_frame` | `None` / `numpy array` | Simpan frame kamera terkini untuk thread AI akses |
| `is_running` | `bool` | Flag utama untuk menghentikan semua thread secara selamat |
| `system_activated` | `bool` | Flag menunjukkan sistem sudah ditekan START atau belum |
| `stepper_active` | `bool` | Status motor stepper — `True` = bergerak, `False` = berhenti |
| `ai_result_text` | `str` | Teks keputusan AI untuk dipaparkan di skrin |
| `system_status` | `str` | Status sistem untuk log dan paparan UI |
| `detected_fruit_memory` | `str` / `None` | Ingat buah yang terakhir dikesan ("apple" atau "oren") |

> **Global State Management** adalah teknik menggunakan pembolehubah global supaya multiple thread boleh berkongsi maklumat status sistem yang sama.

```python
# Bendera Perlindungan Interlock Anti-Double Trigger
is_scanning_lock = False
oren_timer_lock = 0
```
| Pembolehubah | Jenis | Maksud |
|-------------|-------|--------|
| `is_scanning_lock` | `bool` | Kunci sistem supaya tidak imbas semula sebelum proses pengasingan selesai |
| `oren_timer_lock` | `float` | Simpan masa Unix timestamp untuk cooldown 5 saat selepas buah oren |

> **Anti-Double Trigger** adalah mekanisme keselamatan untuk mengelakkan sistem membaca frame yang sama berulang kali dan memicu aktuator secara berlebihan.

---

### Bahagian 3: Kawasan Fokus Visi Komputer (ROI)

```python
ROI_X, ROI_Y = 210, 190   
ROI_W, ROI_H = 250, 250 
```
| Pembolehubah | Nilai | Maksud |
|-------------|-------|--------|
| `ROI_X` | `210` | Koordinat X mula (pojok kiri atas) kawasan imbasan |
| `ROI_Y` | `190` | Koordinat Y mula (pojok kiri atas) kawasan imbasan |
| `ROI_W` | `250` | Lebar kawasan imbasan dalam piksel |
| `ROI_H` | `250` | Tinggi kawasan imbasan dalam piksel |

> **ROI** = *Region of Interest* — kawasan kecil dalam frame kamera yang difokuskan untuk analisis AI. Ini mengurangkan beban pemprosesan CPU dan meningkatkan kelajuan inferens.

```python
LINE_Y = ROI_Y + (ROI_H // 2)
LINE_START_X = ROI_X
LINE_END_X = ROI_X + ROI_W
```
| Pembolehubah | Formula | Maksud |
|-------------|---------|--------|
| `LINE_Y` | `ROI_Y + (ROI_H // 2)` | Garisan trigger di tengah-tengah ROI (koordinat Y) |
| `LINE_START_X` | `ROI_X` | Mula garisan trigger (kiri) |
| `LINE_END_X` | `ROI_X + ROI_W` | Tamat garisan trigger (kanan) |

> **Trigger Line** adalah garisan maya dalam ROI. Apabila objek (buah) melintasi garisan ini, sistem akan memicu proses inferens AI.

```python
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
```
| Pembolehubah | Nilai BGR | Maksud |
|-------------|-----------|--------|
| `C_BG` | `(15, 18, 25)` | Warna latar belakang gelap (industrial dark) |
| `C_PANEL` | `(22, 28, 38)` | Warna panel atas |
| `C_CARD` | `(30, 38, 52)` | Warna kad maklumat bawah |
| `C_LINE` | `(50, 60, 80)` | Warna garisan sempadan |
| `C_ACTIVE` | `(0, 170, 255)` | Biru neon — status aktif / berjalan |
| `C_OK` | `(60, 220, 100)` | Hijau — status OK / berjaya |
| `C_ALERT` | `(0, 180, 255)` | Biru cerah — amaran / proses |
| `C_ERR` | `(50, 50, 220)` | Merah — ralat / berhenti |
| `C_TXT` | `(230, 235, 245)` | Putih kebiruan — teks utama |
| `C_TXT2` | `(160, 170, 190)` | Kelabu — teks sekunder |
| `C_DIM` | `(100, 110, 130)` | Kelabu gelap — komponen tidak aktif |
| `C_AMBER` | `(255, 170, 0)` | Amber / oren — imbasan / trigger |

> **BGR** = *Blue, Green, Red* — format warna standard OpenCV (berbeza dengan RGB yang biasa digunakan di web).

---

### Bahagian 4: Thread Stepper Motor

```python
def stepper_thread():
    global stepper_active, is_running
    GPIO.output(DIR, GPIO.LOW) # Menetapkan arah putaran linear ke hadapan
    while is_running:
        if stepper_active:
```
| Syntax | Maksud |
|--------|--------|
| `def stepper_thread():` | Definisi fungsi untuk thread stepper motor |
| `global stepper_active, is_running` | Isytihar pembolehubah global supaya boleh diubah dalam fungsi |
| `GPIO.output(DIR, GPIO.LOW)` | Tetapkan arah stepper ke hadapan (LOW = satu arah, HIGH = arah songsang) |
| `while is_running:` | Gelung tanpa henti selagi sistem masih aktif |
| `if stepper_active:` | Semak sama ada motor perlu bergerak atau tidak |

```python
            # Memancarkan Output Isyarat Lampu RUN dan Menghidupkan Nadi Motor
            GPIO.output(RELAY_GREEN, GPIO.LOW)  # Lampu Hijau Aktif
            GPIO.output(RELAY_RED, GPIO.HIGH)   # Lampu Merah Padam
```
> **Logik Relay:** Relay ini menggunakan logik *active LOW* — `GPIO.LOW` menghidupkan relay, `GPIO.HIGH` memadamkannya. Ini bergantung pada jenis modul relay yang digunakan (common cathode).

```python
            GPIO.output(PUL, GPIO.HIGH)
            time.sleep(0.009) 
            GPIO.output(PUL, GPIO.LOW)
            time.sleep(0.009)
```
| Syntax | Maksud |
|--------|--------|
| `GPIO.output(PUL, GPIO.HIGH)` | Hantar denyutan HIGH ke pin PUL |
| `time.sleep(0.009)` | Jeda 9ms (9000 mikrosaat) |
| `GPIO.output(PUL, GPIO.LOW)` | Hantar denyutan LOW ke pin PUL |
| `time.sleep(0.009)` | Jeda 9ms lagi |

> **Denyutan (Pulse):** Setiap denyutan HIGH→LOW menggerakkan motor stepper satu *step*. Dengan jeda 9ms + 9ms = 18ms per step, kelajuan ≈ 55.5 step/saat. Untuk motor NEMA 23 dengan 200 step/revolution, ini ≈ 16.7 RPM.

```python
        else:
            # Mengubah Status Papan Latihan ke Mod Sedia (IDLE Mode)
            GPIO.output(RELAY_GREEN, GPIO.HIGH) # Lampu Hijau Padam
            GPIO.output(RELAY_RED, GPIO.LOW)    # Lampu Merah Aktif
            time.sleep(0.1)
```
> Apabila `stepper_active = False`, motor berhenti bergerak dan lampu merah menyala untuk menunjukkan status IDLE.

---

### Bahagian 5: Sub-Routine Servo

```python
def open_gate(label):
    label_check = label.lower()
    if label_check == "apple":
        print(">>> ACTUATOR: OPENING GATE FOR APPLE <<<")
        pwm_servo.ChangeDutyCycle(12)  # Sudut 90 darjah lengan penolak objek
        time.sleep(1.2)
        pwm_servo.ChangeDutyCycle(0)   # Mematikan isyarat memegang untuk elak servo bergegar
```
| Syntax | Maksud |
|--------|--------|
| `def open_gate(label):` | Fungsi untuk membuka gate servo |
| `label.lower()` | Tukar label kepada huruf kecil supaya perbandingan tidak sensitif huruf besar/kecil |
| `pwm_servo.ChangeDutyCycle(12)` | Tukar *duty cycle* kepada 12% = sudut ~90° (lengan menolak buah) |
| `time.sleep(1.2)` | Tunggu 1.2 saat untuk servo mencapai sudut |
| `ChangeDutyCycle(0)` | Set *duty cycle* kepada 0% — mematikan isyarat PWM untuk mengelakkan servo bergegar (*jitter*) |

> **Formula Servo:** Sudut ≈ (DutyCycle - 2) × 10. Jadi 12% ≈ (12-2) × 10 = 100°. Nilai sebenar bergantung pada servo MG996R individu.

```python
def reset_gate():
    print(">>> ACTUATOR: CLOSING GATE (RESET) <<<")
    pwm_servo.ChangeDutyCycle(2)   # Kembali ke kedudukan asal (0 darjah)
    time.sleep(1.2)
    pwm_servo.ChangeDutyCycle(0)
```
| Syntax | Maksud |
|--------|--------|
| `ChangeDutyCycle(2)` | *Duty cycle* 2% = sudut ~0° (lengan dalam kedudukan asal) |

---

### Bahagian 6: Thread Enjin Inferens AI

```python
def ai_logic(model_path):
    global latest_frame, is_running, stepper_active, ai_result_text, system_status, detected_fruit_memory, system_activated
    global is_scanning_lock, oren_timer_lock
```
> Semua pembolehubah global diisytihar supaya thread AI boleh berkomunikasi dengan thread utama dan thread stepper.

```python
    with ImageImpulseRunner(model_path) as runner:
        runner.init()
        print("[SISTEM] Model .eim Berjaya Dimuatkan. Menunggu Isyarat Panel...")
```
| Syntax | Maksud |
|--------|--------|
| `with ... as runner:` | *Context manager* — memastikan model dibersihkan (*cleanup*) dengan betul apabila thread tamat |
| `ImageImpulseRunner(model_path)` | Cipta objek runner dengan memuatkan fail model `.eim` |
| `runner.init()` | Inisialisasi model — memuatkan neural network ke dalam RAM |

```python
        while is_running:
            # SEMAKAN PANEL 1: PENGESANAN ISYARAT BUTANG MULA (START SWITCH)
            if not system_activated:
                if GPIO.input(BUTTON_START) == GPIO.LOW:
                    print("[PANEL COMMAND] Isyarat START Diterima. Konveyor Beroperasi.")
                    time.sleep(0.5)  # Debounce delay
                    system_activated = True
                    stepper_active = True
                    detected_fruit_memory = None
                    is_scanning_lock = False
                    ai_result_text = "Mencari..."
                    system_status = "READY: MENCARI BUAH..."
```
| Syntax | Maksud |
|--------|--------|
| `GPIO.input(BUTTON_START)` | Baca status pin butang START |
| `== GPIO.LOW` | Semak sama ada butang ditekan (Active LOW) |
| `time.sleep(0.5)` | **Debounce delay** — elakkan isyarat berlipat ganda akibat getaran mekanikal suis |
| `system_activated = True` | Aktifkan sistem secara keseluruhan |
| `stepper_active = True` | Mula gerakkan motor stepper |

> **Debounce** adalah teknik elektronik/penogranan untuk mengelakkan isyarat berbilang daripada suis mekanikal yang bergetar apabila ditekan.

```python
            # KONTROL TIMING: PELEPASAN KUNCI COOLDOWN KHAS UNTUK OREN (5 SAAT)
            if is_scanning_lock and detected_fruit_memory == "oren":
                if time.time() > oren_timer_lock:
                    detected_fruit_memory = None      
                    is_scanning_lock = False
                    ai_result_text = "Mencari..."
                    system_status = "READY: MENCARI BUAH..."
                    print("[SISTEM LOG] Pemasa 5s Oren Tamat. Mengaktifkan Semula Radar Imbasan Kamera.")
```
| Syntax | Maksud |
|--------|--------|
| `time.time()` | Dapatkan masa semasa dalam format Unix timestamp (saat) |
| `> oren_timer_lock` | Semak sama ada masa semasa sudah melebihi masa tamat cooldown |
| `detected_fruit_memory = None` | Kosongkan memori buah — sedia untuk objek seterusnya |
| `is_scanning_lock = False` | Buka kunci imbasan — benarkan AI imbas semula |

> **Cooldown 5 saat** untuk buah oren: Oren tidak perlu disisihkan (terus meluncur), jadi sistem perlu tunggu 5 saat supaya buah oren yang sama tidak dibaca berulang kali.

```python
            # Fasa Pemprosesan Inferens AI Sekiranya Talian Konveyor Aktif
            if latest_frame is not None and system_activated:

                # FASA 1: VISI KOMPUTER & PENGIMBASAN MATRIKS MODEL AI
                if detected_fruit_memory is None and not is_scanning_lock:
                    roi_frame = latest_frame[ROI_Y:ROI_Y+ROI_H, ROI_X:ROI_X+ROI_W]
                    roi_resized = cv2.resize(roi_frame, (320, 320))
                    roi_rgb = cv2.cvtColor(roi_resized, cv2.COLOR_BGR2RGB)
```
| Syntax | Maksud |
|--------|--------|
| `latest_frame is not None` | Pastikan frame kamera sudah tersedia |
| `system_activated` | Pastikan sistem sudah ditekan START |
| `detected_fruit_memory is None` | Pastikan tiada buah sedang diproses |
| `not is_scanning_lock` | Pastikan kunci imbasan tidak aktif |
| `latest_frame[y1:y2, x1:x2]` | *Array slicing* — potong ROI dari frame penuh |
| `cv2.resize(..., (320, 320))` | Tukar saiz ROI kepada 320×320 px untuk input model |
| `cv2.cvtColor(..., COLOR_BGR2RGB)` | Tukar format warna BGR (OpenCV) kepada RGB (Edge Impulse) |

```python
                    features, _ = runner.get_features_from_image(roi_rgb)
                    res = runner.classify(features)
```
| Syntax | Maksud |
|--------|--------|
| `runner.get_features_from_image(roi_rgb)` | Ekstrak ciri-ciri matrik dari imej RGB |
| `runner.classify(features)` | Jalankan inferens neural network — kembalikan keputusan klasifikasi |

```python
                    bboxes = []
                    if isinstance(res, dict):
                        if "bounding_boxes" in res:
                            bboxes = res["bounding_boxes"]
                        elif "result" in res and "bounding_boxes" in res["result"]:
                            bboxes = res["result"]["bounding_boxes"]
```
| Syntax | Maksud |
|--------|--------|
| `isinstance(res, dict)` | Semak sama ada keputusan adalah dictionary |
| `"bounding_boxes" in res` | Semak sama ada kekunci `bounding_boxes` wujud |
| `res["bounding_boxes"]` | Ekstrak senarai kotak sempadan (bounding boxes) |

> Keputusan inferens Edge Impulse mungkin datang dalam dua format bergantung pada versi SDK. Kod ini menyokong kedua-dua format.

```python
                    for bb in bboxes:
                        label = bb.get("label", "unknown").lower()
                        score = float(bb.get("confidence", bb.get("value", 0.0)))

                        if score > 0.60 and (label == "apple" or label == "oren"):
```
| Syntax | Maksud |
|--------|--------|
| `bb.get("label", "unknown")` | Dapatkan label objek; jika tiada, default "unknown" |
| `.lower()` | Tukar kepada huruf kecil untuk perbandingan |
| `float(bb.get("confidence", ...))` | Dapatkan skor keyakinan (0.0 hingga 1.0) |
| `score > 0.60` | Ambang keyakinan — hanya terima jika > 60% |

> **Threshold 60%** adalah ambang keyakinan. Jika skor terlalu rendah, sistem akan mengabaikan objek untuk mengelakkan *false positive*.

```python
                            by = int(bb.get("y", 0))
                            bh = int(bb.get("height", 0))
                            MODEL_LINE_Y = 160 

                            # Logik Pengesanan Melintasi Garisan Visual (Trigger Line)
                            if by <= MODEL_LINE_Y <= (by + bh):
```
| Syntax | Maksud |
|--------|--------|
| `by` | Koordinat Y atas bounding box |
| `bh` | Tinggi bounding box |
| `MODEL_LINE_Y = 160` | Garisan trigger dalam koordinat model (320×320) |
| `by <= MODEL_LINE_Y <= (by + bh)` | Semak sama ada garisan trigger berada di dalam bounding box |

> **Trigger Line Logic:** Apabila objek melintasi garisan maya, sistem memicu proses pengesanan. Ini memastikan objek dianalisis pada kedudukan yang konsisten setiap kali.

```python
                                # Rejam Isyarat Serta-merta untuk Elak Ralat Pengesanan Bertindih
                                is_scanning_lock = True 
                                stepper_active = False 

                                print(f"[CAM TRIGGER] Peranti {label.upper()} Memotong Garisan. Memulakan Analisis...")
                                system_status = f"{label.upper()} BERHENTI (MULA IMBASAN AI)"
                                ai_result_text = "SCANNING..."
                                time.sleep(1.5) # Jeda Masa untuk Penilaian Matriks AI

                                ai_result_text = f"{label.upper()} ({int(score*100)}%)"
```
| Syntax | Maksud |
|--------|--------|
| `is_scanning_lock = True` | Kunci sistem — elak bacaan berulang |
| `stepper_active = False` | Hentikan stepper supaya buah berhenti di hadapan sensor |
| `time.sleep(1.5)` | Jeda 1.5 saat untuk stabilisasi imej sebelum inferens akhir |
| `int(score*100)` | Tukar skor perpuluhan kepada peratusan (contoh: 0.85 → 85%) |

```python
                                # PROSEDUR PENGASINGAN ALIRAN LOGIK HIBRID
                                if label == "oren":
                                    print(f"[LOGIK LOG] Buah Oren Sah. Mengunci Sistem Selama 5 Saat.")
                                    detected_fruit_memory = "oren"
                                    system_status = "BUAH: OREN // MELUNCUR JALAN TERUS..."
                                    stepper_active = True 
                                    oren_timer_lock = time.time() + 5.0

                                elif label == "apple":
                                    print(f"[LOGIK LOG] Buah Apple Sah. Mengunci Sehingga Trigger Isyarat IR.")
                                    detected_fruit_memory = "apple" 
                                    system_status = "BUAH: APPLE // MENUJU KE SENSOR GATE 1..."
                                    stepper_active = True 
```
| Logik | Tindakan |
|-------|----------|
| **Oren** | Buah terus meluncur (tidak perlu disisihkan). Sistem dikunci 5 saat supaya buah yang sama tidak dibaca ulang. |
| **Apple** | Buah perlu disisihkan. Stepper bergerak untuk membawa apple ke sensor Gate 1. Sistem menunggu isyarat IR. |

```python
                # FASA 2: MAKLUM BALAS SENSOR FIZIKAL (PELEPASAN KUNCI SENSOR UNTUK APPLE)
                if detected_fruit_memory == "apple" and (GPIO.input(SENSOR_GATE_1) == GPIO.LOW):
                    print("[SENSOR TRIGGER] Isyarat IR Terputus. Mengaktifkan Lengan Penolak Servo...")
                    stepper_active = False
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
```
| Syntax | Maksud |
|--------|--------|
| `GPIO.input(SENSOR_GATE_1) == GPIO.LOW` | Sensor IR mendetek apple — isyarat LOW (objek menghalang sinar IR) |
| `open_gate("apple")` | Aktifkan servo untuk menolak apple ke slot gred |
| `time.sleep(3.0)` | Tunggu 3 saat untuk apple jatuh ke slot |
| `reset_gate()` | Tutup semula gate servo |
| `for i in range(3, 0, -1)` | Kira mundur 3→2→1 sebelum sistem sedia untuk buah seterusnya |

```python
            time.sleep(0.01) # Kadar Kitaran Polling Ringan (10ms) untuk Kestabilan CPU Pi
```
> **Polling 10ms** = 100Hz. Ini memberi keseimbangan antara responsif sistem dan penggunaan CPU yang tidak terlalu tinggi.

---

### Bahagian 7: Program Utama (OpenCV UI)

```python
def main():
    global latest_frame, is_running, ai_result_text, system_status, stepper_active, system_activated

    modelfile = "/home/iskandar/buahaiv4.eim" 
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```
| Syntax | Maksud |
|--------|--------|
| `cv2.VideoCapture(0)` | Buka kamera USB pertama (index 0) |
| `cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)` | Tetapkan lebar frame kepada 640 px |
| `cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)` | Tetapkan tinggi frame kepada 480 px |

```python
    if not cap.isOpened():
        print("[RALAT CRITICAL] Gagal Mengakses Pangkalan Data Kamera USB!")
        return
```
| Syntax | Maksud |
|--------|--------|
| `cap.isOpened()` | Semak sama ada kamera berjaya dibuka |
| `return` | Keluar dari fungsi `main()` jika kamera gagal |

```python
    # Melancarkan Pengurusan Tugasan Serentak (Multi-Threading Deployment)
    threading.Thread(target=stepper_thread, daemon=True).start()
    threading.Thread(target=ai_logic, args=(modelfile,), daemon=True).start()
```
| Syntax | Maksud |
|--------|--------|
| `threading.Thread(target=..., daemon=True)` | Cipta thread baharu dengan `daemon=True` (thread akan mati automatik apabila program utama tamat) |
| `args=(modelfile,)` | Hantar argumen `modelfile` kepada fungsi `ai_logic` (perlu koma untuk tuple satu elemen) |
| `.start()` | Mula thread |

> **Multi-Threading:** 3 thread berjalan serentak:
> 1. **Thread utama** — OpenCV UI + kamera
> 2. **Thread stepper** — Kawalan motor stepper
> 3. **Thread AI** — Inferens Edge Impulse + logik pengasingan

```python
    print("--- SISTEM INFERENS INTEGRASI KORPORAT SELESAI ---")
    camera_error_count = 0
```
> `camera_error_count` — menghitung kegagalan bacaan kamera berturut-turut. Jika > 10, sistem keluar.

```python
    while is_running:
        ret, frame = cap.read()
        if not ret: 
            camera_error_count += 1
            time.sleep(0.1)
            if camera_error_count > 10: break
            continue
```
| Syntax | Maksud |
|--------|--------|
| `ret, frame = cap.read()` | Baca frame dari kamera. `ret` = boolean kejayaan, `frame` = imej |
| `if not ret` | Jika bacaan gagal |
| `camera_error_count += 1` | Tambah penghitung ralat |
| `if camera_error_count > 10: break` | Keluar gelung jika kamera gagal 10 kali berturut-turut |
| `continue` | Langkau ke iterasi seterusnya |

```python
        camera_error_count = 0
        latest_frame = frame.copy()

        is_active = system_activated
```
| Syntax | Maksud |
|--------|--------|
| `camera_error_count = 0` | Reset penghitung ralat apabila bacaan berjaya |
| `frame.copy()` | Buat salinan frame supaya thread AI tidak ubah frame asal |
| `is_active = system_activated` | Salin status ke pembolehubah tempatan untuk kegunaan UI |

#### Melukis Komponen UI (Antaramuka Grafik)

```python
        # Melukis Komponen Atas (Top Slim Status Bar)
        accent = C_OK if is_active else C_ERR
        cv2.rectangle(frame, (0, 0), (640, 40), C_PANEL, -1)
        cv2.line(frame, (0, 40), (640, 40), accent, 2)
```
| Syntax | Maksud |
|--------|--------|
| `cv2.rectangle(img, (x1,y1), (x2,y2), color, -1)` | Lukis segi empat tepat penuh (*filled*) |
| `cv2.line(img, (x1,y1), (x2,y2), color, thickness)` | Lukis garisan |
| `accent = C_OK if is_active else C_ERR` | Ternary operator — hijau jika aktif, merah jika tidak |

```python
        # Animasi Lampu LED Status Dinamik
        cv2.circle(frame, (18, 20), 6, accent, -1)
        cv2.circle(frame, (18, 20), 8, accent, 1)
```
| Syntax | Maksud |
|--------|--------|
| `cv2.circle(img, (x,y), radius, color, -1)` | Lukis bulatan penuh (LED) |
| `cv2.circle(img, (x,y), radius, color, 1)` | Lukis bulatan kosong (border LED) |

```python
        cv2.putText(frame, txt, (35, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.55, col, 2)
```
| Syntax | Maksud |
|--------|--------|
| `cv2.putText(img, text, (x,y), font, scale, color, thickness)` | Tulis teks pada imej |
| `cv2.FONT_HERSHEY_SIMPLEX` | Font standard OpenCV |
| `0.55` | Skala saiz font |
| `2` | Ketebalan teks dalam piksel |

```python
        # Paparan Mod Operasi Badge
        mode = "AUTO" if is_active else "MANUAL"
        mcol = C_OK if is_active else C_DIM
        ts = cv2.getTextSize(mode, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)[0]
        cv2.rectangle(frame, (620-ts[0]-10, 8), (630, 32), mcol, -1)
        cv2.putText(frame, mode, (625-ts[0]-5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_BG, 1)
```
| Syntax | Maksud |
|--------|--------|
| `cv2.getTextSize(text, font, scale, thickness)` | Dapatkan saiz (lebar, tinggi) teks sebelum dilukis |
| `[0]` | Ambil elemen pertama (tuple saiz) |
| `ts[0]` | Lebar teks dalam piksel |

> **Badge AUTO/MANUAL:** Lukis segi empat tepat dengan lebar mengikut saiz teks supaya badge sentiasa kemas.

```python
        # Melukis Komponen Tengah (Neon Style ROI Box Display)
        roi_color = C_ACTIVE if is_active else C_DIM
        scan_color = C_AMBER if is_active else C_DIM

        for i in range(3, 0, -1):
            glow = tuple(int(c * 0.15 + 15 * 0.85) for c in roi_color)
            cv2.rectangle(frame, (ROI_X-i, ROI_Y-i), (ROI_X+ROI_W+i, ROI_Y+ROI_H+i), glow, 1)
```
| Syntax | Maksud |
|--------|--------|
| `for i in range(3, 0, -1)` | Ulang 3 kali (i=3, 2, 1) untuk efek glow berlapis |
| `tuple(int(c * 0.15 + 15 * 0.85) for c in roi_color)` | Formula *glow* — campurkan warna ROI dengan warna gelap (15) untuk efek kekaburan |
| `(ROI_X-i, ROI_Y-i)` | Koordinat atas-kiri yang diperluas mengikut lapisan glow |

> **Neon Glow Effect:** 3 lapisan segi empat tepat dengan warna semakin pudar menjauhi ROI untuk meniru efek neon.

```python
        # Melukis Penjuru Sempadan Kotak Ticks
        tick = 18
        cv2.line(frame, (ROI_X, ROI_Y), (ROI_X+tick, ROI_Y), roi_color, 2)
        cv2.line(frame, (ROI_X, ROI_Y), (ROI_X, ROI_Y+tick), roi_color, 2)
        ...
```
> **Corner Ticks:** Garisan pendek di setiap penjuru ROI untuk meniru antaramuka *heads-up display* (HUD) industri dan tentera.

```python
        # Melukis Garisan Laser Sensor Maya (Virtual Laser Alignment)
        scan_y = LINE_Y
        cv2.line(frame, (LINE_START_X, scan_y), (LINE_END_X, scan_y), scan_color, 2)
        cv2.line(frame, (LINE_START_X, scan_y-6), (LINE_START_X, scan_y+6), scan_color, 2)
        cv2.line(frame, (LINE_END_X, scan_y-6), (LINE_END_X, scan_y+6), scan_color, 2)
```
> **Virtual Laser:** Garisan melintang dengan penanda T di hujung untuk menunjukkan garisan trigger AI.

```python
        # Melukis Animasi Status Pergerakan Belt Tali Sawat
        belt_y = ROI_Y + ROI_H + 8
        cv2.rectangle(frame, (ROI_X, belt_y), (ROI_X+ROI_W, belt_y+4), C_LINE, -1)
        if stepper_active:
            cv2.rectangle(frame, (ROI_X+ROI_W//2-10, belt_y-2), (ROI_X+ROI_W//2+10, belt_y+6), C_OK, -1)
            cv2.putText(frame, ">>", (ROI_X+ROI_W//2-8, belt_y+4), cv2.FONT_HERSHEY_SIMPLEX, 0.3, C_BG, 1)
        else:
            cv2.rectangle(frame, (ROI_X+ROI_W//2-10, belt_y-2), (ROI_X+ROI_W//2+10, belt_y+6), C_ERR, -1)
            cv2.putText(frame, "X", (ROI_X+ROI_W//2-3, belt_y+4), cv2.FONT_HERSHEY_SIMPLEX, 0.3, C_BG, 1)
```
> **Belt Indicator:** Paparan kecil di bawah ROI untuk menunjukkan status tali sawat — `>>` = bergerak, `X` = berhenti.

```python
        # Melukis Kad Data Klasifikasi (Glassmorphism-Inspired Bottom Card)
        show_card = (detected_fruit_memory is not None or
                     not stepper_active or
                     not is_active or
                     "OREN" in system_status)

        if show_card:
            card_y = 370
            overlay = frame.copy()
            cv2.rectangle(overlay, (30, card_y), (610, card_y+90), C_CARD, -1)
            cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
```
| Syntax | Maksud |
|--------|--------|
| `cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)` | Campurkan dua imej dengan nisbah 85:15 untuk efek *translucent* / glassmorphism |

> **Glassmorphism Effect:** Imej asal (frame) dicampur dengan overlay gelap (85% opacity) untuk meniru kesan kaca lutsinar.

```python
        # Bulatan Isyarat Sub-Komponen Fizikal (Sub-Component Diagnostic LEDs)
        ccol = C_OK if stepper_active else C_DIM
        cv2.circle(frame, (520, card_y+35), 4, ccol, -1)
        cv2.putText(frame, "CONV", (530, card_y+38), cv2.FONT_HERSHEY_SIMPLEX, 0.3, C_TXT2, 1)

        gcol = C_ALERT if detected_fruit_memory == 'apple' else C_DIM
        cv2.circle(frame, (520, card_y+55), 4, gcol, -1)
        cv2.putText(frame, "GATE", (530, card_y+58), cv2.FONT_HERSHEY_SIMPLEX, 0.3, C_TXT2, 1)
```
> **Diagnostic LEDs:** Bulatan kecil yang meniru lampu status pada panel kawalan industri — hijau = OK, amber = aktif/proses, kelabu = tidak aktif.

```python
        # Kapsyen Institusi & Label Diagnostik Perkakasan Manual (Footer)
        cv2.putText(frame, "ADTEC BP // MECHATRONICS FYP V5.8", (420, 472), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_DIM, 1)

        start_state = "LOW(PRS)" if GPIO.input(BUTTON_START) == GPIO.LOW else "HIGH"
        cv2.putText(frame, f"START SWITCH: {start_state} | QUIT: PRESS 'q'", (20, 472), cv2.FONT_HERSHEY_SIMPLEX, 0.35, C_DIM, 1)
```
> **Footer:** Paparan versi sistem dan status suis START secara real-time untuk tujuan debugging.

```python
        cv2.imshow('SISTEM SORTING ADTEC BP', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            is_running = False
            break
```
| Syntax | Maksud |
|--------|--------|
| `cv2.imshow('window_name', frame)` | Paparkan frame dalam tetingkap OpenCV |
| `cv2.waitKey(1)` | Tunggu 1ms untuk input papan kekunci |
| `& 0xFF` | Mask 8-bit untuk dapatkan kod ASCII kekunci |
| `ord('q')` | Kod ASCII untuk huruf 'q' |
| `is_running = False` | Set flag global supaya semua thread berhenti |
| `break` | Keluar dari gelung `while` |

```python
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
```
| Syntax | Maksud |
|--------|--------|
| `GPIO.output(PUL, GPIO.LOW)` | Pastikan pin PUL dalam keadaan LOW (motor berhenti) |
| `GPIO.output(RELAY_GREEN, GPIO.HIGH)` | Padamkan lampu hijau |
| `GPIO.output(RELAY_RED, GPIO.HIGH)` | Padamkan lampu merah |
| `pwm_servo.stop()` | Hentikan isyarat PWM servo |
| `GPIO.cleanup()` | Bersihkan semua tetapan GPIO — **WAJIB** untuk elakkan ralat pada run seterusnya |
| `cap.release()` | Lepaskan kamera USB |
| `cv2.destroyAllWindows()` | Tutup semua tetingkap OpenCV |

> **Fail-Safe Shutdown:** Kod ini memastikan semua perkakasan berada dalam keadaan selamat apabila program tamat. Ini adalah amalan terbaik dalam kawalan industri untuk mengelakkan keadaan bahaya (*hazardous states*).

```python
if __name__ == "__main__":
    main()
```
| Syntax | Maksud |
|--------|--------|
| `if __name__ == "__main__":` | Semak sama ada fail dijalankan secara langsung (bukan diimport sebagai modul) |
| `main()` | Panggil fungsi utama |

> **Standard Python Practice:** Ini memastikan kod hanya berjalan apabila fail dieksekusi terus, bukan apabila diimport oleh fail lain.

---

## 🏭 Nota Industri & Penutup

Melalui kaedah **fail `.eim`** dan persekitaran **venv** ini, sistem dapat menjalankan pemprosesan rangkaian neural sepenuhnya di dalam CPU Raspberry Pi 4 secara **luar talian** (**100% Offline Inference**).

| Kebaikan | Huraian |
|----------|---------|
| **Tiada Internet Diperlukan** | Operasi sistem tidak bergantung pada isyarat internet makmal |
| **Kelewatan Rendah** | Inferens ~31 ms menggunakan format `int8` |
| **Kestabilan Operasi** | Sistem konveyor berfungsi secara autonomi tanpa gangguan |
| **Keselamatan Data** | Data imej tidak dihantar ke pelayan luar; pemprosesan lokal sepenuhnya |
| **Kos Operasi Rendah** | Tiada keperluan langganan cloud atau API berbayar |

> 🎯 **Kesimpulan:** Pendekatan *Edge AI* ini menjamin kestabilan operasi sistem konveyor pengasingan buah tanpa bergantung pada sebarang infrastruktur internet, menjadikannya sesuai untuk persekitaran industri dan makmal latihan.

---

<p align="center">
  <strong>Dibangunkan oleh Mohd Iskandar Shah bin Rosli</strong><br>
  <em>Diploma in Mechatronics Technology | ADTEC JTM Kampus Batu Pahat</em><br>
  <sub>Final Year Project (PTA 2) — AI-Based Fruit Sorting Conveyor Training Kit</sub>
</p>
