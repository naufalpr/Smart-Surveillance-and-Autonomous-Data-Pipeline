# Smart Surveillance & Autonomous Data Pipeline

Sistem pengawasan cerdas berbasis cloud yang memanfaatkan layanan Amazon Web Services (AWS) untuk mendeteksi objek berbahaya secara otomatis dan mengirimkan notifikasi keamanan secara real-time.

## Deskripsi Proyek

Proyek ini mengimplementasikan arsitektur *event-driven* dan *serverless* menggunakan layanan AWS untuk membangun sistem pengawasan otomatis. Citra yang dikirim oleh perangkat edge akan disimpan pada Amazon S3, dianalisis menggunakan Amazon Rekognition melalui AWS Lambda, kemudian hasil analisis disimpan ke Amazon DynamoDB. Jika terdeteksi objek yang berpotensi berbahaya, sistem akan mengirimkan notifikasi melalui Amazon SNS.

Objek yang dipantau meliputi:

- Weapon
- Fire
- Knife
- Gun
- Weaponry

---

## Arsitektur Sistem

```text
Edge Device (Python)
        │
        ▼
   Amazon S3
        │
        ▼
 AWS Lambda
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
Rekognition DynamoDB SNS
                │
                ▼
         Email Alert
```

---

## Fitur

- Pengiriman gambar otomatis setiap 2 detik.
- Penyimpanan citra menggunakan Amazon S3.
- Analisis objek menggunakan Amazon Rekognition.
- Penyimpanan hasil deteksi ke Amazon DynamoDB.
- Pengiriman notifikasi melalui Amazon SNS.
- Implementasi berbasis serverless architecture.
- Integrasi layanan AWS secara event-driven.

---

## Struktur Proyek

```text
.
├── lambda.py
├── simulasi_cctv_periodik.py
├── test-image.jpg
└── README.md
```

---

## Teknologi yang Digunakan

- Python 3.12
- Amazon S3
- AWS Lambda
- Amazon Rekognition
- Amazon DynamoDB
- Amazon SNS
- Boto3

---

## Persyaratan

Pastikan telah memiliki:

- Akun AWS atau AWS Academy Learner Lab
- Python 3.12 atau versi yang kompatibel
- Paket Boto3

Instalasi dependensi:

```bash
pip install boto3
```

---

## Konfigurasi AWS

### 1. Amazon DynamoDB

Buat tabel dengan konfigurasi berikut:

| Parameter | Nilai |
|------------|--------|
| Table Name | SurveillanceLog |
| Partition Key | image_id |
| Sort Key | timestamp |

---

### 2. Amazon SNS

Buat topik SNS:

| Parameter | Nilai |
|------------|--------|
| Topic Name | SecurityAlerts |
| Type | Standard |

Tambahkan subscription menggunakan email dan lakukan konfirmasi melalui email yang dikirim AWS.

---

### 3. Amazon S3

Buat bucket:

```text
smart-surveillance-bucket
```

---

### 4. AWS Lambda

Buat fungsi Lambda dengan konfigurasi berikut:

| Parameter | Nilai |
|------------|--------|
| Runtime | Python 3.12 |
| Role | LabRole |

Salin isi file `lambda.py` ke editor AWS Lambda.

Kemudian ganti ARN SNS:

```python
SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"
```

Contoh:

```python
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:SecurityAlerts"
```

---

## Menjalankan Simulasi CCTV

Letakkan file gambar uji pada direktori proyek:

```text
test-image.jpg
```

Jalankan program:

```bash
python simulasi_cctv_periodik.py
```

Program akan:

1. Membaca file gambar lokal.
2. Mengunggah gambar ke Amazon S3 setiap 2 detik.
3. Memicu AWS Lambda secara otomatis.
4. Menjalankan analisis menggunakan Amazon Rekognition.
5. Menyimpan hasil ke DynamoDB.
6. Mengirim email jika terdeteksi objek berbahaya.

---

## Pengujian

### Skenario Aman

Gunakan gambar:

- Ruangan kosong
- Pemandangan
- Area tanpa objek berbahaya

Hasil yang diharapkan:

```text
Status : SAFE
Email  : Tidak dikirim
```

### Skenario Berbahaya

Gunakan gambar yang mengandung:

- Knife
- Weapon
- Gun
- Fire

Hasil yang diharapkan:

```text
Status : CRITICAL
Email  : Dikirim otomatis
```

---

## Alur Kerja Sistem

1. Perangkat edge mengirimkan gambar ke Amazon S3.
2. Amazon S3 memicu AWS Lambda melalui Event Notification.
3. AWS Lambda memanggil Amazon Rekognition untuk mendeteksi objek.
4. Hasil analisis disimpan ke Amazon DynamoDB.
5. Jika objek berbahaya terdeteksi, AWS Lambda mengirim notifikasi melalui Amazon SNS.
6. Petugas keamanan menerima email peringatan.

---

## Hasil Implementasi

Sistem berhasil mengintegrasikan layanan Amazon S3, AWS Lambda, Amazon Rekognition, Amazon DynamoDB, dan Amazon SNS untuk membangun pipeline pemantauan otomatis berbasis cloud.

Implementasi ini memungkinkan proses pengiriman gambar, analisis objek, penyimpanan data, dan pengiriman notifikasi berjalan secara otomatis tanpa intervensi pengguna.

---
