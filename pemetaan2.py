import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Peta UMKM Sambas", layout="wide")

st.title("📍 Monitoring UMKM Kabupaten Sambas")

# 2. Data UMKM (Contoh di Sambas)
data = {
    'id': [1, 2, 3, 4],
    'Nama_UMKM': ['Tenun Songket Sambas', 'Kerupuk Ikan Pemangkat', 'Jeruk Tebas Super', 'Lempok Durian Sambas'],
    'Lat': [1.3621, 1.1758, 1.2585, 1.3650],
    'Lon': [109.3105, 108.9722, 109.1824, 109.3150],
    'Alamat': ['Sambas Kota', 'Pemangkat', 'Tebas', 'Jl. Istana Sambas']
}
df = pd.DataFrame(data)

# --- LOGIKA KLIK ---
# Inisialisasi posisi peta default (Sambas) jika belum ada di session state
if 'map_center' not in st.session_state:
    st.session_state.map_center = [1.3621, 109.3105]
    st.session_state.zoom = 10

# Fungsi untuk memperbarui lokasi peta saat tombol diklik
def update_map(lat, lon):
    st.session_state.map_center = [lat, lon]
    st.session_state.zoom = 15  # Zoom lebih dekat saat klik spesifik UMKM

# 3. Layout: Sidebar untuk Daftar dan Utama untuk Peta
col_list, col_map = st.columns([1, 3])

with col_list:
    st.subheader("Daftar UMKM")
    st.write("Klik nama untuk lihat di peta:")
    for i, row in df.iterrows():
        # Tombol untuk setiap UMKM
        if st.button(f"🔍 {row['Nama_UMKM']}", key=row['id'], use_container_width=True):
            update_map(row['Lat'], row['Lon'])

with col_map:
    # Membuat objek peta dengan lokasi dari session state
    m = folium.Map(
        location=st.session_state.map_center, 
        zoom_start=st.session_state.zoom,
        control_scale=True
    )
    
    marker_cluster = MarkerCluster().add_to(m)

    # Menambahkan semua titik UMKM
    for i, row in df.iterrows():
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=f"<b>{row['Nama_UMKM']}</b><br>{row['Alamat']}",
            tooltip=row['Nama_UMKM'],
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(marker_cluster)

    # Tampilkan peta (gunakan key agar widget ter-refresh saat data berubah)
    st_folium(m, width="100%", height=600, key="peta_sambas")

# 4. Tabel Detail di Bawah
st.divider()
st.subheader("Data Lengkap")
st.dataframe(df[['Nama_UMKM', 'Alamat']], use_container_width=True)
