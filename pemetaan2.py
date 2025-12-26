import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Peta UMKM Sambas", layout="wide")

st.title("📍 Pemetaan UMKM Kabupaten Sambas")
st.info("Pilih baris pada tabel di bawah untuk melihat lokasinya di peta.")

# 2. Dataset UMKM Sambas
data = {
    'Nama_UMKM': [
        'Tenun Songket Sambas Indah', 
        'Kerupuk Ikan Pemangkat', 
        'Jeruk Tebas Super', 
        'Lempok Durian Sambas',
        'Warkop Bang Long'
    ],
    'Produk': ['Kain Tenun', 'Camilan', 'Buah Segar', 'Makanan Khas', 'Minuman'],
    'Lat': [1.3621, 1.1758, 1.2585, 1.3650, 1.3610],
    'Lon': [109.3105, 108.9722, 109.1824, 109.3150, 109.3080],
}
df = pd.DataFrame(data)

# 3. Menampilkan Tabel dengan Fitur Seleksi Baris
# Kita menggunakan column_config untuk menyembunyikan kolom koordinat agar tabel rapi
st.subheader("Daftar UMKM")
event = st.dataframe(
    df, 
    use_container_width=True, 
    hide_index=True,
    on_select="rerun",  # Memicu refresh saat baris diklik
    selection_mode="single_row", # Hanya bisa pilih satu baris
    column_config={
        "Lat": None, # Sembunyikan kolom Lat
        "Lon": None  # Sembunyikan kolom Lon
    }
)

# 4. Logika Penentuan Fokus Peta
# Default: Berfokus di Sambas
map_center = [1.3621, 109.3105]
zoom_level = 10

# Cek apakah ada baris yang dipilih di tabel
selected_rows = event.selection.rows
if selected_rows:
    # Ambil index baris yang diklik
    row_idx = selected_rows[0]
    # Ambil data koordinat dari baris tersebut
    selected_lat = df.iloc[row_idx]['Lat']
    selected_lon = df.iloc[row_idx]['Lon']
    selected_name = df.iloc[row_idx]['Nama_UMKM']
    
    # Update posisi peta ke lokasi yang dipilih
    map_center = [selected_lat, selected_lon]
    zoom_level = 16 # Zoom dekat ke lokasi
    st.success(f"Menampilkan lokasi: **{selected_name}**")

# 5. Render Peta
st.subheader("Peta Lokasi")
m = folium.Map(location=map_center, zoom_start=zoom_level)

# Tambahkan semua marker UMKM
for i, row in df.iterrows():
    # Jika baris ini yang sedang dipilih, beri warna berbeda (misal merah)
    is_selected = (selected_rows and i == selected_rows[0])
    color = "red" if is_selected else "blue"
    
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        popup=f"<b>{row['Nama_UMKM']}</b>",
        tooltip=row['Nama_UMKM'],
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# Tampilkan peta
st_folium(m, width="100%", height=500, key="map_sambas")
