import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# 1. Konfigurasi Halaman
st.set_page_config(page_title="UMKM Sambas", layout="wide")

st.title("📍 Peta Sebaran UMKM Kabupaten Sambas")
st.markdown("Pencarian produk dan lokasi UMKM unggulan di wilayah Sambas.")

# 2. Data Simulasi UMKM Kabupaten Sambas
# (Silakan ganti bagian ini dengan df = pd.read_csv('data_sambas.csv') jika ada file-nya)
data = {
    'Nama_UMKM': [
        'Tenun Songket Sambas Indah', 'Kerupuk Ikan Pemangkat', 'Jeruk Tebas Super', 
        'Kopi Aming Sambas', 'Lempok Durian Sambas', 'Kain Benang Emas Terigas',
        'Terasi Bubuk Selakau', 'Warkop Bang Long'
    ],
    'Kategori': ['Kriya', 'Kuliner', 'Pertanian', 'Kuliner', 'Kuliner', 'Kriya', 'Kuliner', 'Kuliner'],
    'Wilayah': ['Sambas Kota', 'Pemangkat', 'Tebas', 'Sambas Kota', 'Sambas Kota', 'Terigas', 'Selakau', 'Sambas Kota'],
    'Lat': [1.3621, 1.1758, 1.2585, 1.3605, 1.3650, 1.3550, 1.0833, 1.3610],
    'Lon': [109.3105, 108.9722, 109.1824, 109.3050, 109.3150, 109.3000, 108.9833, 109.3080],
    'Produk_Utama': ['Kain Songket', 'Kerupuk Ikan', 'Jeruk Siam', 'Kopi Bubuk', 'Lempok Durian', 'Tenun', 'Terasi', 'Minuman']
}
df = pd.DataFrame(data)

# 3. Sidebar Menu
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/2e/Logo_Kabupaten_Sambas.png", width=100)
st.sidebar.header("Opsi Pencarian")

# Cari berdasarkan Nama atau Produk
keyword = st.sidebar.text_input("Cari UMKM atau Produk (misal: Tenun, Kopi, Jeruk):", placeholder="Ketik di sini...")

# Filter berdasarkan Wilayah (Kecamatan)
wilayah_pilihan = st.sidebar.multiselect(
    "Filter Wilayah:",
    options=df['Wilayah'].unique(),
    default=df['Wilayah'].unique()
)

# 4. Logika Filter
df_filtered = df[
    (df['Nama_UMKM'].str.contains(keyword, case=False) | df['Produk_Utama'].str.contains(keyword, case=False)) &
    (df['Wilayah'].isin(wilayah_pilihan))
]

# 5. Visualisasi
if not df_filtered.empty:
    st.info(f"Ditemukan {len(df_filtered)} UMKM di {', '.join(wilayah_pilihan)}")
    
    # Koordinat pusat Sambas: 1.3621, 109.3105
    m = folium.Map(location=[1.3621, 109.3105], zoom_start=10)
    marker_cluster = MarkerCluster().add_to(m)

    for i, row in df_filtered.iterrows():
        # Memberikan warna berbeda untuk Kriya dan Kuliner
        warna = 'red' if row['Kategori'] == 'Kriya' else 'green'
        
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=f"<b>{row['Nama_UMKM']}</b><br>Produk: {row['Produk_Utama']}<br>Wilayah: {row['Wilayah']}",
            tooltip=row['Nama_UMKM'],
            icon=folium.Icon(color=warna, icon='shopping-cart')
        ).add_to(marker_cluster)

    st_folium(m, width=1200, height=550)
    
    # Tabel Data
    st.subheader("Daftar Detail UMKM")
    st.table(df_filtered[['Nama_UMKM', 'Produk_Utama', 'Wilayah', 'Kategori']])

else:
    st.warning("Data tidak ditemukan. Silakan gunakan kata kunci lain.")

# 6. Tombol Download Data
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Data Hasil Pencarian (CSV)",
    data=csv,
    file_name='umkm_sambas_filtered.csv',
    mime='text/csv',
)
