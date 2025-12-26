import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. Konfigurasi Halaman agar lebar penuh
st.set_page_config(page_title="Peta UMKM Sambas", layout="wide")

st.title("📍 Pemetaan UMKM Kabupaten Sambas")
st.markdown("---")

# 2. Dataset UMKM Sambas (Simulasi)
# Koordinat disesuaikan dengan wilayah Kabupaten Sambas
data = {
    'Nama_UMKM': [
        'Tenun Songket Sambas Indah', 
        'Kerupuk Ikan Pemangkat', 
        'Jeruk Tebas Super', 
        'Lempok Durian Sambas',
        'Warkop Bang Long Sambas',
        'Terasi Bubuk Selakau'
    ],
    'Produk': ['Kain Tenun', 'Camilan', 'Buah Segar', 'Makanan Khas', 'Minuman', 'Bumbu Dapur'],
    'Wilayah': ['Sambas Kota', 'Pemangkat', 'Tebas', 'Sambas Kota', 'Sambas Kota', 'Selakau'],
    'Lat': [1.3621, 1.1758, 1.2585, 1.3650, 1.3610, 1.0833],
    'Lon': [109.3105, 108.9722, 109.1824, 109.3150, 109.3080, 108.9833],
}
df = pd.DataFrame(data)

# --- LOGIKA NAVIGASI PETA ---
# Inisialisasi posisi awal peta (Kabupaten Sambas)
map_center = [1.3621, 109.3105]
zoom_level = 10

# 3. Bagian Tabel (Sebagai Pengendali Peta)
st.subheader("Daftar UMKM")
st.write("Klik baris pada tabel di bawah ini untuk memfokuskan lokasi pada peta:")

# Fitur seleksi baris (Update: menggunakan 'single-row')
selected_event = st.dataframe(
    df, 
    use_container_width=True, 
    hide_index=True,
    on_select="rerun",  
    selection_mode="single-row", # Perbaikan dari single_row ke single-row
    column_config={
        "Lat": None, # Sembunyikan kolom koordinat agar tabel bersih
        "Lon": None
    }
)

# Cek apakah ada baris yang diklik oleh user
selected_rows = selected_event.selection.rows
if selected_rows:
    row_idx = selected_rows[0]
    map_center = [df.iloc[row_idx]['Lat'], df.iloc[row_idx]['Lon']]
    zoom_level = 16 # Zoom otomatis ke lokasi toko
    st.success(f"📍 Menampilkan: **{df.iloc[row_idx]['Nama_UMKM']}** ({df.iloc[row_idx]['Wilayah']})")

# 4. Bagian Peta Interaktif
st.subheader("Peta Interaktif")
m = folium.Map(location=map_center, zoom_start=zoom_level)

# Tambahkan semua marker UMKM ke peta
for i, row in df.iterrows():
    # Jika baris ini yang sedang dipilih, beri warna merah
    is_selected = (selected_rows and i == selected_rows[0])
    marker_color = "red" if is_selected else "blue"
    
    folium.Marker(
        location=[row['Lat'], row['Lon']],
        popup=f"<b>{row['Nama_UMKM']}</b><br>{row['Produk']}<br>{row['Wilayah']}",
        tooltip=row['Nama_UMKM'],
        icon=folium.Icon(color=marker_color, icon='shop', prefix='fa')
    ).add_to(m)

# Tampilkan peta ke aplikasi Streamlit
st_folium(m, width="100%", height=500, key="map_sambas_final")

# 5. Footer Tambahan
st.markdown("---")
st.caption("Data ini adalah simulasi untuk pengembangan sistem informasi UMKM Kabupaten Sambas.")
