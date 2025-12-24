import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Peta Sebaran UMKM", layout="wide")

st.title("📍 Dashboard Pemetaan Sebaran UMKM")
st.markdown("Aplikasi ini menampilkan lokasi UMKM berdasarkan kategori usaha.")

# 2. Data Simulasi (Nanti bisa diganti dengan pd.read_csv('data_kamu.csv'))
data = {
    'Nama_UMKM': ['Kopi Kenangan Rakyat', 'Batik Solo Indah', 'Keripik Tempe Barokah', 'Bengkel Maju', 'Catering Sehat'],
    'Kategori': ['Kuliner', 'Kriya', 'Kuliner', 'Jasa', 'Kuliner'],
    'Lat': [-6.2088, -6.2146, -6.1751, -6.1900, -6.2200],
    'Lon': [106.8456, 106.8451, 106.8272, 106.8100, 106.8300],
    'Pendapatan': [500, 300, 150, 400, 600] # Dalam juta
}
df = pd.DataFrame(data)

# 3. Sidebar untuk Filter
st.sidebar.header("Filter Data")
kategori_pilihan = st.sidebar.multiselect(
    "Pilih Kategori UMKM:",
    options=df['Kategori'].unique(),
    default=df['Kategori'].unique()
)

# Filter dataframe berdasarkan pilihan
df_filtered = df[df['Kategori'].isin(kategori_pilihan)]

# 4. Statistik Singkat
col1, col2 = st.columns(2)
col1.metric("Total UMKM Ditampilkan", len(df_filtered))
col2.metric("Rata-rata Pendapatan", f"Rp {df_filtered['Pendapatan'].mean():.1f} jt")

# 5. Pembuatan Peta
st.subheader("Peta Lokasi")
# Titik tengah peta (diambil dari rata-rata koordinat)
map_center = [df_filtered['Lat'].mean(), df_filtered['Lon'].mean()]
m = folium.Map(location=map_center, zoom_start=13, control_scale=True)

# Menggunakan MarkerCluster agar titik yang berdekatan mengelompok
marker_cluster = MarkerCluster().add_to(m)

for i, row in df_filtered.iterrows():
    ikona = 'orange' if row['Kategori'] == 'Kuliner' else 'blue'
    
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        popup=f"<b>{row['Nama_UMKM']}</b><br>Kategori: {row['Kategori']}",
        tooltip=row['Nama_UMKM'],
        icon=folium.Icon(color=ikona, icon='info-sign')
    ).add_to(marker_cluster)

# Menampilkan peta di Streamlit
st_folium(m, width=1100, height=500)

# 6. Tabel Data
st.subheader("Detail Data UMKM")
st.dataframe(df_filtered, use_container_width=True)
