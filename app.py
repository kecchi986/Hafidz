from flask import Flask, jsonify, render_template, request
import mysql.connector
import random

app = Flask(__name__)

# Konfigurasi MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'prediksi_emas'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

from flask import Flask, jsonify, render_template, request
import mysql.connector
import random

app = Flask(__name__)

# Konfigurasi MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'prediksi_emas'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Fungsi untuk menghitung interval berdasarkan data historis
def calculate_intervals(produksi_data):
    total_emas = sum([item['total'] for item in produksi_data])
    intervals = []
    kumulatif = 0
    for item in produksi_data:
        probabilitas = item['total'] / total_emas
        kumulatif += probabilitas
        intervals.append({
            'tahun': item['tahun'],
            'jumlah_emas': item['total'],
            'probabilitas': probabilitas,
            'kumulatif': kumulatif,
            'interval': (kumulatif - probabilitas, kumulatif)
        })
    return intervals



# Fungsi untuk menghitung bilangan acak menggunakan RNG
def generate_rng(intervals, a=1664525, c=1013904223, m=2**32, seed=42):
    rng_data = []
    zi = seed
    for interval in intervals:
        next_zi = (a * zi + c) % m
        angka_tiga_digit = next_zi // (m // 1000)  # Mengambil 3 digit pertama
        rng_data.append({
            'zi': zi,
            'calculated': (a * zi + c),
            'mod': next_zi,
            'angka_tiga_digit': angka_tiga_digit
        })
        zi = next_zi  # Update Zi untuk iterasi berikutnya
    print(rng_data)  # Debug: Cek apakah rng_data berubah
    return rng_data



# Fungsi untuk menghitung hasil prediksi berdasarkan RNG
def predict_emas(intervals, rng_data, start_year=2023):
    predictions = []
    current_year = start_year  # Mulai dari tahun 2023
    for i, rng in enumerate(rng_data):
        rng_value = rng['angka_tiga_digit'] / 1000  # Menggunakan angka tiga digit sebagai proporsi
        for interval in intervals:
            # Cek apakah rng_value berada dalam interval kumulatif yang sesuai
            if interval['interval'][0] <= rng_value < interval['interval'][1]:
                # Pastikan hasil prediksi yang sesuai diambil
                predictions.append({
                    'tahun': current_year,  # Tahun bertambah mulai dari 2023
                    'prediksi_emas': interval['jumlah_emas']  # Ambil jumlah emas berdasarkan interval
                })
                current_year += 1  # Tambahkan tahun untuk prediksi berikutnya
                break  # Keluar dari loop setelah menemukan interval yang sesuai
    return predictions




@app.route('/')
def home():
    # Koneksi ke database dan mengambil data produksi
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT tahun, total FROM tambang_emas')
    produksi_data = cursor.fetchall()
    conn.close()
    
    # Menghitung interval dan RNG
    intervals = calculate_intervals(produksi_data)
    rng_data = generate_rng(intervals)
    predictions = predict_emas(intervals, rng_data)
    
    # Debug untuk memeriksa data yang dikirim
    print("Predictions:", predictions)  # Cek output prediksi

    return render_template('web.html', 
                           produksi_data=produksi_data,
                           intervals=intervals,
                           rng_data=rng_data,
                           predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True)
