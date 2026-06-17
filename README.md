# 🍏 Autonomous Fruit Sorting: End-to-End Edge AI Deployment Guide (A to Z)

Dokumentasi ini menyediakan panduan lengkap bermula daripada fasa pengumpulan data imej (*Data Acquisition*) di Edge Impulse Studio, proses latihan model (*Training*), sehinggalah fasa *deployment* secara **100% Luar Talian (Offline Inference)** di dalam persekitaran maya (*Virtual Environment*) Raspberry Pi 4 menggunakan Thonny IDE.

---

## 🛑 FASA 1: PENGURUSAN DATA & LATHAN MODEL (EDGE IMPULSE)

### Langkah 1: Pengumpulan Data Imej (Data Acquisition)
1. Log masuk ke akaun **Edge Impulse Studio** melalui pelayar web laptop anda dan cipta projek baharu.
2. Sediakan kamera (boleh menggunakan telefon pintar atau USB webcam yang disambungkan pada laptop/Raspberry Pi).
3. Di dalam Edge Impulse, pergi ke menu **Data Acquisition**.
4. Pilih **Collect Data** dan ambil gambar buah (contoh: Apple dan Oren) dari pelbagai sudut, jarak, dan variasi pencahayaan yang ada di dalam makmal ADTEC bagi memastikan model tidak mengalami ralat *overfitting*.
5. Ambil sekurang-kurangnya 100-200 gambar untuk setiap kelas buah.
6. Lakukan pelabelan objek (*Bounding Box Labelling*) pada setiap gambar dengan melukis kotak tepat pada kedudukan buah dan berikan nama label (Contoh: `Apple` atau `Orange`).
7. Pastikan pembahagian data (*Data Split*) berada pada nisbah **80% Training Data** dan **20% Testing Data**.

### Langkah 2: Konfigurasi Impulsen (Impulse Design)
1. Navigasi ke menu **Impulse Design** -> **Create Impulse**.
2. Di bahagian **Input Blocks**, tetapkan saiz imej kepada `160 x 160` piksel (saiz optimum untuk pemprosesan laju pada Raspberry Pi 4).
3. Di bahagian **Processing Blocks**, tambah blok **Image** (berfungsi untuk menukar piksel warna RGB imej kepada ciri-ciri matrik matematik).
4. Di bahagian **Learning Blocks**, tambah blok **Object Detection (Images)** (menggunakan algoritma rangkaian neural MobileNetV2-SSD).
5. Klik **Save Impulse**.

### Langkah 3: Latihan Model & Pengesahan Ketepatan (Training & Validation)
1. Pergi ke sub-menu **Image** di sebelah kiri, klik tab *Generate Features* dan klik butang **Generate Features**. Proses ini mengekstrak data visual menjadi kluster matrik data.
2. Pergi ke sub-menu **Object Detection**, tetapkan parameter latihan:
   * *Number of epochs:* `50` hingga `100` (kitaran latihan).
   * *Learning rate:* `0.001` (kelajuan perubahan berat neural).
3. Klik **Start Training**. Setelah selesai, perhatikan nilai **Validation Accuracy (Precision & Recall %)**. Pastikan graf *accuracy* stabil dan memuaskan.

### Langkah 4: Eksport Fail Model (.eim)
1. Pergi ke menu **Deployment** di sebelah kiri pelayar web anda.
2. Di bawah segmen *Target Device*, cari dan pilih **Raspberry Pi 4**.
3. Di bahagian bawah halaman, pilih optimasi **Quantized (int8)**. Format *int8* menukarkan nilai matematik apungan (float32) kepada integer 8-bit. Ini sangat kritikal untuk menurunkan masa kelewatan inferens (*inference latency*) kepada ~31 ms pada Raspberry Pi 4.
4. Klik butang **Build**. Tunggu sehingga proses kompilasi selesai, pelayar web akan memuat turun sebuah fail binari tanpa format biasa bernama **`buahaiv4.eim`** ke laptop anda.

---

## ⚙️ FASA 2: DEPLOYMENT & KODING (RASPBERRY PI 4)

### Langkah 5: Cipta Folder Projek & Pindah Fail `.eim`
1. Hidupkan Raspberry Pi 4 anda dan buka **File Manager**.
2. Di dalam direktori utama user iaitu `/home/pi/`, **cipta satu folder baru** dan namakan folder tersebut sebagai `Fruit_Sorting_Project`. Folder ini akan memegang fail kod Python, fail model, dan persekitaran maya (`venv`) anda.
3. Salin fail `buahaiv4.eim` yang telah dimuat turun di laptop tadi ke dalam sebuah pendrive.
4. Cucuk pendrive pada port USB Raspberry Pi 4, salin fail `buahaiv4.eim` tersebut, dan tampal (*paste*) di dalam folder `/home/pi/Fruit_Sorting_Project/`.

### Langkah 6: Bina dan Aktifkan Persekitaran Maya (venv)
Sistem operasi Raspberry Pi yang baharu (Debian Bookworm ke atas) mewajibkan penggunaan *Virtual Environment* (`venv`) untuk mengelakkan ralat sistem *externally-managed-environment* semasa anda memasang pustaka luar menggunakan perintah `pip`.

1. Buka **Terminal** di Raspberry Pi.
2. Navigasi masuk ke dalam folder projek yang baru dicipta tadi menggunakan arahan:
   ```bash
   cd /home/pi/Fruit_Sorting_Project
