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
    df = pd.read_csv('https://raw.githubusercontent.com/phanorama/analisisdata/refs/heads/main/dashboard/main_data.csv')
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
st.subheader(f"Konsentrasi polutan {selected_pollutant} dalam musim dingin")
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

######################

musim_avg = df.groupby('musim')[['PM2.5', 'PM10']].mean().reset_index()

# Buat bar plot
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=musim_avg, x='musim', y=selected_pollutant, palette='pastel', ax=ax)
ax.set_title(f'Rata-Rata {selected_pollutant} per Musim', fontsize=12)
ax.set_xlabel('Musim', fontsize=10)
ax.set_ylabel(f'Konsentrasi {selected_pollutant} (µg/m³)', fontsize=10)

for p in ax.patches:
    ax.annotate(
        f"{p.get_height():.1f}", 
        (p.get_x() + p.get_width() / 2, p.get_height()),
        ha='center', 
        va='bottom',
        fontsize=10
    )

# Tampilkan plot di Streamlit
st.pyplot(fig)

######################

corr_matrix = df[['RAIN', selected_pollutant, 'TEMP']].corr()
# Buat heatmap
st.write("### Heatmap Korelasi")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
plt.title(f'Korelasi konsentrasi {selected_pollutant}')
st.pyplot(fig)

######################

# Membuat plot hexbin
st.subheader(f"Konsentrasi polutan {selected_pollutant} pada saat hujan")
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

agg_data = df.groupby('hujan')[['PM2.5', 'PM10']].mean().reset_index()
agg_data['hujan'] = agg_data['hujan'].map({True: 'Hujan', False: 'Tidak Hujan'})

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=agg_data, x='hujan', y='PM2.5', ax=ax, palette='pastel')
ax.set_title('Rata-Rata PM2.5', fontsize=12)
ax.set_xlabel('')
ax.set_ylabel('Konsentrasi PM2.5 (µg/m³)')

# Tambahkan nilai di atas bar
for p in ax.patches:
    ax.annotate(
        f"{p.get_height():.1f}", 
        (p.get_x() + p.get_width() / 2, p.get_height()),
        ha='center', 
        va='bottom',
        fontsize=10
    )
st.pyplot(fig)
