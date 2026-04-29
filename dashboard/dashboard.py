import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    day = pd.read_csv(os.path.join(BASE_DIR, 'main_data.csv'))
    day['dteday'] = pd.to_datetime(day['dteday'])
    season_map  = {1:'Spring', 2:'Summer', 3:'Fall', 4:'Winter'}
    weather_map = {1:'Clear/Partly Cloudy', 2:'Mist/Cloudy', 3:'Light Rain/Snow', 4:'Heavy Rain/Snow'}
    yr_map      = {0:'2011', 1:'2012'}
    day['season_label']  = day['season'].map(season_map)
    day['weather_label'] = day['weathersit'].map(weather_map)
    day['year_label']    = day['yr'].map(yr_map)
    day['year_month']    = day['dteday'].dt.to_period('M').astype(str)
    day['temp_actual']   = day['temp'] * 41
    return day

day_df = load_data()

# Header
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis data peminjaman sepeda **Capital Bikeshare, Washington D.C. (2011–2012)**")
st.markdown("---")

# Sidebar
st.sidebar.header("🔍 Filter")
years = ['Semua'] + sorted(day_df['year_label'].unique().tolist())
selected_year = st.sidebar.selectbox("Tahun", years)
seasons = ['Semua'] + sorted(day_df['season_label'].unique().tolist())
selected_season = st.sidebar.selectbox("Musim", seasons)

df = day_df.copy()
if selected_year != 'Semua':
    df = df[df['year_label'] == selected_year]
if selected_season != 'Semua':
    df = df[df['season_label'] == selected_season]

# KPI
c1, c2, c3, c4 = st.columns(4)
c1.metric("🚲 Total Peminjaman",  f"{df['cnt'].sum():,}")
c2.metric("📅 Rata-rata Harian",  f"{df['cnt'].mean():,.0f}")
c3.metric("👤 Casual Users",      f"{df['casual'].sum():,}")
c4.metric("🎫 Registered Users",  f"{df['registered'].sum():,}")
st.markdown("---")

# ── Pertanyaan 1 ──────────────────────────────────────────────────────────────
st.subheader("📈 Pertanyaan 1: Tren Total Peminjaman Sepeda Bulanan")
monthly = day_df.groupby(['year_label','year_month'])['cnt'].sum().reset_index().sort_values('year_month').reset_index(drop=True)

fig1, ax1 = plt.subplots(figsize=(14, 5))
sns.set_theme(style='whitegrid')
colors = ['#4C72B0' if y == '2011' else '#55A868' for y in monthly['year_label']]
bars = ax1.bar(range(len(monthly)), monthly['cnt'], color=colors, edgecolor='white')
peak_idx = int(monthly['cnt'].idxmax())
bars[peak_idx].set_color('#E84040')
ax1.annotate(
    f"Puncak: {monthly.loc[peak_idx,'cnt']:,}",
    xy=(peak_idx, monthly.loc[peak_idx,'cnt']),
    xytext=(max(0, peak_idx-4), monthly.loc[peak_idx,'cnt']*0.9),
    arrowprops=dict(arrowstyle='->', color='#E84040'),
    color='#E84040', fontsize=9, fontweight='bold'
)
ax1.set_xticks(range(len(monthly)))
ax1.set_xticklabels(monthly['year_month'].tolist(), rotation=45, ha='right', fontsize=8)
ax1.set_ylabel('Total Peminjaman', fontsize=11)
ax1.set_title('Tren Total Peminjaman Sepeda Bulanan (2011–2012)', fontsize=13, fontweight='bold')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x):,}'))
legend_els = [mpatches.Patch(facecolor='#4C72B0', label='2011'),
              mpatches.Patch(facecolor='#55A868', label='2012'),
              mpatches.Patch(facecolor='#E84040', label='Puncak')]
ax1.legend(handles=legend_els, loc='upper left')
plt.tight_layout()
st.pyplot(fig1)

with st.expander("💡 Insight Pertanyaan 1"):
    st.markdown("""
    - Tren peminjaman menunjukkan **pertumbuhan signifikan** dari 2011 ke 2012.
    - **Puncak peminjaman terjadi pada September 2012** dengan 218.573 peminjaman.
    - Pola musiman konsisten: tinggi di pertengahan tahun, rendah di awal tahun.
    """)

st.markdown("---")

# ── Pertanyaan 2 ──────────────────────────────────────────────────────────────
st.subheader("🌤️ Pertanyaan 2: Pengaruh Musim dan Cuaca terhadap Peminjaman")
fig2, (ax2, ax3) = plt.subplots(1, 2, figsize=(14, 5))

season_avg = df.groupby('season_label')['cnt'].mean().reset_index().sort_values('cnt', ascending=False)
colors_s = ['#E84040' if i==0 else '#A8C0D6' if i<len(season_avg)-1 else '#4C72B0' for i in range(len(season_avg))]
bars2 = ax2.bar(season_avg['season_label'], season_avg['cnt'], color=colors_s, edgecolor='white')
for bar, val in zip(bars2, season_avg['cnt']):
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+30, f'{val:,.0f}', ha='center', fontsize=9, fontweight='bold')
ax2.set_title('Rata-rata Peminjaman per Musim', fontsize=12, fontweight='bold')
ax2.set_ylabel('Rata-rata Peminjaman Harian')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x):,}'))

weather_avg = df.groupby('weather_label')['cnt'].mean().reset_index().sort_values('cnt', ascending=False)
colors_w = ['#E84040' if i==0 else '#A8C0D6' if i<len(weather_avg)-1 else '#4C72B0' for i in range(len(weather_avg))]
bars3 = ax3.bar(weather_avg['weather_label'], weather_avg['cnt'], color=colors_w, edgecolor='white')
for bar, val in zip(bars3, weather_avg['cnt']):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+30, f'{val:,.0f}', ha='center', fontsize=9, fontweight='bold')
ax3.set_title('Rata-rata Peminjaman per Kondisi Cuaca', fontsize=12, fontweight='bold')
ax3.set_ylabel('Rata-rata Peminjaman Harian')
ax3.set_xticklabels(weather_avg['weather_label'], rotation=15, ha='right', fontsize=9)
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x):,}'))
plt.tight_layout()
st.pyplot(fig2)

with st.expander("💡 Insight Pertanyaan 2"):
    st.markdown("""
    - **Fall (Gugur)** adalah musim dengan peminjaman tertinggi, **Spring (Semi)** terendah.
    - **Cuaca cerah** menghasilkan peminjaman tertinggi, **hujan/salju** turun hingga ~63%.
    - Cuaca adalah faktor terbesar yang mempengaruhi keputusan meminjam sepeda.
    """)

st.markdown("---")

# ── Analisis Lanjutan ─────────────────────────────────────────────────────────
st.subheader("🔬 Korelasi Suhu dan Peminjaman")

fig3, (ax4, ax5) = plt.subplots(1, 2, figsize=(14, 5))

# Scatter suhu vs peminjaman
ax4.scatter(df['temp_actual'], df['cnt'], alpha=0.4, color='#4C72B0', edgecolors='none')
ax4.set_xlabel('Suhu Aktual (°C)', fontsize=11)
ax4.set_ylabel('Total Peminjaman', fontsize=11)
ax4.set_title('Hubungan Suhu dengan Jumlah Peminjaman', fontsize=12, fontweight='bold')
z = np.polyfit(df['temp_actual'], df['cnt'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['temp_actual'].min(), df['temp_actual'].max(), 100)
ax4.plot(x_line, p(x_line), color='#E84040', linewidth=2, label='Tren')
corr = df['temp_actual'].corr(df['cnt'])
ax4.legend()
ax4.text(0.05, 0.92, f'r = {corr:.3f}', transform=ax4.transAxes,
         fontsize=10, color='#E84040', fontweight='bold')
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x):,}'))

# Workingday vs Weekend
workday_avg = df.groupby('workingday')['cnt'].mean().reset_index()
workday_avg['label'] = workday_avg['workingday'].map({0:'Weekend/Holiday', 1:'Hari Kerja'})
bars4 = ax5.bar(workday_avg['label'], workday_avg['cnt'], color=['#55A868','#4C72B0'], edgecolor='white')
for bar, val in zip(bars4, workday_avg['cnt']):
    ax5.text(bar.get_x()+bar.get_width()/2, bar.get_height()+30,
             f'{val:,.0f}', ha='center', fontsize=10, fontweight='bold')
ax5.set_ylabel('Rata-rata Peminjaman Harian', fontsize=11)
ax5.set_title('Peminjaman: Hari Kerja vs Weekend/Holiday', fontsize=12, fontweight='bold')
ax5.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'{int(x):,}'))

plt.tight_layout()
st.pyplot(fig3)

with st.expander("💡 Insight Analisis Lanjutan"):
    corr_val = day_df['temp_actual'].corr(day_df['cnt'])
    st.markdown(f"""
    - Terdapat **korelasi positif** antara suhu dan jumlah peminjaman (r = {corr_val:.3f}),
      artinya semakin hangat cuaca semakin banyak orang meminjam sepeda.
    - Rata-rata peminjaman di **hari kerja dan weekend tidak berbeda signifikan**,
      menunjukkan sepeda digunakan untuk commuting maupun rekreasi.
    """)

st.markdown("---")
st.subheader("📋 Data Harian")
st.dataframe(
    df[['dteday','season_label','weather_label','year_label','casual','registered','cnt']]
    .rename(columns={'dteday':'Tanggal','season_label':'Musim','weather_label':'Cuaca',
                     'year_label':'Tahun','casual':'Casual','registered':'Registered','cnt':'Total'})
    .reset_index(drop=True),
    use_container_width=True
)
st.caption("Dashboard dibuat menggunakan Streamlit | Data: Bike Sharing Dataset (Capital Bikeshare, Washington D.C.)")
