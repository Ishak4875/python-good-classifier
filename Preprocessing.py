import numpy as np
from PIL import Image

class Preprocessing:

    def resize(image):
        tinggi_baru = 224
        lebar_baru = 224
        tinggi_asli, lebar_asli, _ = image.shape
        gambar_baru = np.zeros((tinggi_baru, lebar_baru, 3), dtype=np.uint8)

        skala_y = tinggi_asli / tinggi_baru
        skala_x = lebar_asli / lebar_baru

        for y in range(tinggi_baru):
            for x in range(lebar_baru):
                # Hitung posisi piksel pada gambar asli yang sesuai dengan posisi pada gambar baru
                x_asli = x * skala_x
                y_asli = y * skala_y

                # Koordinat piksel sekitar yang akan digunakan untuk interpolasi
                x1 = np.int32(x_asli)
                x2 = np.minimum(x1 + 1, lebar_asli - 1)
                y1 = np.int32(y_asli)
                y2 = np.minimum(y1 + 1, tinggi_asli - 1)

                # Hitung bobot interpolasi
                tx = x_asli - x1
                ty = y_asli - y1

                # Interpolasi nilai warna RGB
                for c in range(3):
                    nilai_atas_kiri = (1 - tx) * (1 - ty) * image[y1, x1, c]
                    nilai_atas_kanan = tx * (1 - ty) * image[y1, x2, c]
                    nilai_bawah_kiri = (1 - tx) * ty * image[y2, x1, c]
                    nilai_bawah_kanan = tx * ty * image[y2, x2, c]

                    # Hitung rata-rata dari empat nilai interpolasi
                    nilai_interpolasi = np.int32(nilai_atas_kiri + nilai_atas_kanan + nilai_bawah_kiri + nilai_bawah_kanan)
                    gambar_baru[y, x, c] = nilai_interpolasi
        return gambar_baru

    def grayscale(image):
        grayscale_image = np.uint8(0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2])
        return grayscale_image
    
