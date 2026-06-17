[README.md](https://github.com/user-attachments/files/29031773/README.md)
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
4. [Nota Industri & Penutup](#-nota-industri--penutup)

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
