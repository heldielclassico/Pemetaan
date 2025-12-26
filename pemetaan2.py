import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Peta UMKM Sambas", layout="wide")

st.title("📍 Pemetaan UMKM Kabupaten Sambas")

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
    'Wilayah': ['Sambas Kota', 'Pemangkat', 'Tebas', 'Sambas Kota', 'Sambas Kota'],
    'Lat': [1.3621, 1.1758, 1.2585, 1.3650, 1.3610],
    'Lon': [109.3105, 108.9722, 109.1824, 109.3150, 109.3080],
}
df = pd.DataFrame(data)

# --- LOGIKA NAVIGASI PETA ---
# Posisi awal (Kabupaten Sambas)
map_center = [1.3621, 109.3105]
zoom_level = 10

# 3. Bagian Tabel (Diletakkan sebelum peta agar user bisa pilih dulu)
st.subheader("Daftar UMKM")
st.markdown("Pilih baris pada tabel untuk melihat detail lokasi di peta:")

# Fitur seleksi baris pada dataframe
selected_event = st.dataframe(
    df, 
    use_container_width=True, 
    hide_index=True,
    on_select="rerun",  
    selection_mode="single_row",
    column_config={
        "Lat": None, 
        "Lon": None
    }
)

# Cek seleksi user
selected_rows = selected_event.selection.rows
if selected_rows:
    row_idx = selected_rows[0]
    map_center = [df.iloc[row_idx]['Lat'], df.iloc[row_idx]['Lon']]
    zoom_level = 16
    st.success(f"📍 Menampilkan Lokasi: **{df.iloc[row_idx]['Nama_UMKM']}**")

# 4. Bagian Peta
st.subheader("Peta Interaktif")
m = folium.Map(location=map_center, zoom_start=zoom_level)

# Tambahkan semua marker
for i, row in df.iterrows():
    # Beri warna merah jika baris dipilih
    is_selected = (selected_rows and i == selected_rows[0])
    marker_color = "red" if is_selected else "blue"
    
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        popup=f"<b>{row['Nama_UMKM']}</b><br>{row['Produk']}",
        tooltip=row['Nama_UMKM'],
        icon=folium.Icon(color=marker_color, icon='shop', prefix='fa')
    ).add_to(m)

# Tampilkan peta ke UI
st_folium(m, width="100%", height=500, key="map_sambas_full")
