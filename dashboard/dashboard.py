import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Media Interaktif: Analisis Data Kualitas Udara (Guanyuan)")
st.markdown("""
Visualisasi ini menunjukkan data konsentrasi polutan PM2.5/PM10 di Guanyuan.
""")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    df['month'] = df['month'].astype('category')
    return df

df = load_data()

st.sidebar.header('Pengaturan Parameter')
selected_pollutant = st.sidebar.selectbox(
    'Pilih Polutan',
    ['PM2.5', 'PM10']
)

# Agregasi data bulanan
monthly_avg = df.groupby('month')[['PM2.5', 'PM10', 'TEMP']].mean().reset_index()

# Plot tren bulanan
st.subheader(f"Tren Bulanan {selected_pollutant} dan Suhu")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=monthly_avg, x='month', y=selected_pollutant, label=selected_pollutant, ax=ax)
sns.lineplot(data=monthly_avg, x='month', y='TEMP', label='Suhu', linestyle='--', ax=ax)

# Label sumbu Y
ax.set_ylabel('Konsentrasi (µg/m³) / Suhu (°C)')
ax.set_xlabel('Bulan')
ax.set_title(f'Tren Bulanan {selected_pollutant} dan Suhu (Guanyuan, China)')

# Menambahkan catatan di bawah plot
fig.text(
    0.5, 0,  # Posisi (x, y) relatif terhadap figure (0-1)
    "Data yang digunakan dihitung sejak per tanggal 1 Maret 2013 - 28 Februari 2017",
    fontsize=8,  # Ukuran kecil
    color="gray",
    ha="center"  # Posisi horizontal: center
)

# Mengatur label sumbu X
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
# ax.fill_between(monthly_avg['month'], min(monthly_avg['TEMP']), monthly_avg[selected_pollutant], alpha=0.2)
ax.set_xlim(1, 12)
ax.set_ylim(min(monthly_avg['TEMP']), 180)

# Menampilkan legenda
ax.legend()

st.pyplot(fig)

# Membuat plot hexbin
st.subheader(f"Plot Hexbin: Hubungan hujan (RAIN) dengan {selected_pollutant}")

# Membuat figure dan axes
fig, ax = plt.subplots(figsize=(8, 6))

# Plot hexbin untuk hubungan RAIN dan PM2.5
hb = ax.hexbin(df['RAIN'], df[selected_pollutant], gridsize=30, cmap='gist_heat', mincnt=1)
cb = fig.colorbar(hb, ax=ax, label='Frekuensi')
ax.set_title(f'Kepadatan Hubungan RAIN dan {selected_pollutant}')
ax.set_xlabel('Curah Hujan (mm)')
ax.set_ylabel(f'{selected_pollutant} (µg/m³)')

# Menampilkan plot di Streamlit
st.pyplot(fig)