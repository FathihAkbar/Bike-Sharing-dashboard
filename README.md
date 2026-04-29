# 🚲 Bike Sharing Dashboard

Dashboard analisis data peminjaman sepeda **Capital Bikeshare, Washington D.C. (2011–2012)** menggunakan Streamlit.

## 📁 Struktur Folder

```
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── requirements.txt
├── url.txt
└── README.md
```

## 🔧 Cara Menjalankan Dashboard

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Streamlit
```bash
streamlit run dashboard/dashboard.py
```

### 3. Buka browser
Buka `http://localhost:8501`

---

## 📊 Pertanyaan Bisnis

1. Bagaimana tren total peminjaman sepeda secara bulanan selama tahun 2011 dan 2012, dan pada bulan apa peminjaman mencapai puncaknya?

2. Pada kondisi cuaca dan musim apa rata-rata jumlah peminjaman sepeda harian paling tinggi dan paling rendah selama periode 2011–2012?

## ✅ Kesimpulan

- Puncak peminjaman terjadi pada **September 2012** dengan 218.573 peminjaman.
- **Musim Fall** dan **cuaca cerah** adalah kondisi paling favorable untuk peminjaman sepeda.
