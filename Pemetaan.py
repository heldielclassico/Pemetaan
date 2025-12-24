import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Peta Sebaran UMKM", layout="wide")

st.title("📍 Dashboard Pemetaan Sebaran UMKM")

# 2. Data Simulasi (Pastikan kolom Nama_UMKM ada)
data = {
    'Nama_UMKM': ['Kopi Kenangan Rakyat', 'Batik Solo Indah', 'Keripik Tempe Barokah', 'Bengkel Maju', 'Catering Sehat'],
    'Kategori': ['Kuliner', 'Kriya', 'Kuliner', 'Jasa', 'Kuliner'],
    'Lat': [-6.2088, -6.2146, -6.1751, -6.1900, -6.2200],
    'Lon': [106.8456, 106.8451, 106.8272, 106.8100, 106.8300],
    'Alamat': ['Jl. Merdeka No. 1', 'Jl. Batik No. 5', 'Jl. Tempe No. 10', 'Jl. Otomotif No. 2', 'Jl. Sayur No. 3']
}
df = pd.DataFrame(data)

# --- BAGIAN MENU CARI ---
st.sidebar.header("🔍 Menu Pencarian")

# Input Pencarian Nama
search_query = st.sidebar.text_input("Cari Nama UMKM:", placeholder="Ketik nama UMKM...")

# Filter Kategori
kategori_pilihan = st.sidebar.multiselect(
    "Filter Kategori:",
    options=df['Kategori'].unique(),
    default=df['Kategori'].unique()
)

# Logika Filter: Berdasarkan Nama DAN Kategori
df_filtered = df[
    (df['Nama_UMKM'].str.contains(search_query, case=False)) & 
    (df['Kategori'].isin(kategori_pilihan))
]
# -------------------------

# 4. Statistik Singkat
if not df_filtered.empty:
    st.success(f"Ditemukan {len(df_filtered)} UMKM")
    
    # 5. Pembuatan Peta
    map_center = [df_filtered['Lat'].mean(), df_filtered['Lon'].mean()]
    m = folium.Map(location=map_center, zoom_start=13)
    marker_cluster = MarkerCluster().add_to(m)

    for i, row in df_filtered.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=f"<b>{row['Nama_UMKM']}</b><br>{row['Alamat']}",
            tooltip=row['Nama_UMKM'],
            icon=folium.Icon(color='blue', icon='shop', prefix='fa')
        ).add_to(marker_cluster)

    st_folium(m, width=1100, height=500)

    # 6. Tabel Data Hasil Cari
    st.subheader("Hasil Pencarian")
    st.write(df_filtered[['Nama_UMKM', 'Kategori', 'Alamat']])
else:
    st.warning("UMKM tidak ditemukan. Coba kata kunci lain.")
