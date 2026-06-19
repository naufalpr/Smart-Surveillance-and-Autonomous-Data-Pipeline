import boto3
import time
import os

# Inisialisasi S3 client
s3 = boto3.client('s3')

# Konfigurasi bucket dan file
bucket_name = 'smart-surveillance-bucket'
file_name = 'test-image.jpg'

def kirim_gambar():
    print("Sistem CCTV aktif. Mengirim gambar setiap 2 detik...")

    no = 1

    while True:
        # Nama file unik berbasis timestamp
        nama_file = f"cctv_capture_{time.strftime('%Y%m%d_%H%M%S')}_{no}.jpg"

        if os.path.exists(file_name):
            try:
                s3.upload_file(file_name, bucket_name, nama_file)
                print(f"[{time.strftime('%H:%M:%S')}] Foto berhasil dikirim: {nama_file}")
                no += 1

            except Exception as e:
                print(f"Gagal mengirim foto. Error: {e}")

        else:
            print(f"File '{file_name}' tidak ditemukan. Pastikan file ada di direktori yang sama.")

        time.sleep(2)

if __name__ == "__main__":
    kirim_gambar()
