import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ArthaWise · Jul–Des 2025",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Design System  ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;500;600;700;800&family=JetBrains+Mono:wght=300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── App Background ── */
.stApp {
    background-color: #F8F9FA;
    color: #2D3142;
}

/* ── Sidebar Style & Typography ── */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E9ECEF;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
[data-testid="stSidebar"] * {
    color: #495057 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── PROFESSIONAL FIX: Desain Tag Filter Multi-Select Premium ── */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #2A5298 !important; /* Menggunakan warna brand utama */
    border-radius: 6px;
    padding: 4px 8px;
    border: 1px solid #1A365D !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span {
    color: #FFFFFF !important; /* Teks filter putih bersih, kontras tinggi */
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] svg {
    fill: #FFFFFF !important; /* Icon silang (x) putih bersih */
    transition: transform 0.2s ease;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"]:hover svg {
    transform: scale(1.15);
}

[data-testid="stSidebar"] label {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: #8A92A6 !important;
    margin-bottom: 8px !important;
}

/* ── Metric Cards ── */
.kpi-row { display: flex; gap: 20px; margin: 0 0 32px 0; }

.kpi-card {
    flex: 1;
    background: #FFFFFF;
    border: 1px solid #E9ECEF;
    border-radius: 12px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.kpi-card:hover { 
    transform: translateY(-4px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02); 
    border-color: #DDE2E5;
}

.kpi-accent {
    position: absolute;
    top: 0; left: 0; bottom: 0;
    width: 5px;
}
.kpi-card.green  .kpi-accent { background: #1E6B4B; }
.kpi-card.red    .kpi-accent { background: #A33333; }
.kpi-card.blue   .kpi-accent { background: #2A5298; }
.kpi-card.ink    .kpi-accent { background: #242424; }

.kpi-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8A92A6;
    margin-bottom: 10px;
    padding-left: 4px;
}
.kpi-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.85rem;
    font-weight: 600;
    color: #1A1D20;
    line-height: 1.15;
    letter-spacing: -0.02em;
    padding-left: 4px;
}
.kpi-value.up   { color: #1E6B4B; }
.kpi-value.down { color: #A33333; }
.kpi-sub {
    font-size: 0.8rem;
    color: #6C757D;
    margin-top: 10px;
    font-weight: 500;
    padding-left: 4px;
}

/* ── Section Headers ── */
.section-wrap {
    margin: 54px 0 24px;
    display: flex;
    align-items: center;
    gap: 14px;
    border-bottom: 2px solid #E9ECEF;
    padding-bottom: 14px;
}
.section-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    color: #495057;
    background: #E9ECEF;
    padding: 3px 8px;
    border-radius: 6px;
}
.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #1A1D20;
    margin: 0;
    letter-spacing: -0.01em;
}
.section-desc {
    font-size: 0.88rem;
    color: #8A92A6;
    margin-left: auto;
    font-weight: 500;
}

/* ── Insight Box ── */
.insight {
    background: #FFFFFF;
    border: 1px solid #E9ECEF;
    border-left: 4px solid #2A5298;
    border-radius: 8px;
    padding: 18px 24px;
    margin-top: 24px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.insight-icon {
    font-size: 1rem;
    color: #2A5298;
    flex-shrink: 0;
    margin-top: 1px;
}
.insight-body { flex-grow: 1; }
.insight-main {
    font-size: 0.9rem;
    color: #343A40;
    line-height: 1.65;
    margin: 0 0 6px;
}
.insight-main strong { color: #1A1D20; font-weight: 700; }
.insight-rec {
    font-size: 0.85rem;
    color: #495057;
    line-height: 1.6;
}
.insight-rec strong { color: #2A5298; font-weight: 700; }

/* ── Page Header ── */
.page-header {
    padding: 28px 0 20px;
    border-bottom: 2px solid #E9ECEF;
    margin-bottom: 36px;
}
.page-eyebrow {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #8A92A6;
    margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
}
.page-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.25rem;
    font-weight: 800;
    color: #1A1D20;
    margin: 0 0 8px;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.page-sub {
    font-size: 0.95rem;
    color: #6C757D;
    font-weight: 400;
}

/* ── Sidebar Header ── */
.sidebar-brand {
    padding: 36px 16px 24px;
    border-bottom: 1px solid #E9ECEF;
    margin-bottom: 28px;
}
.sidebar-brand-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #1A1D20 !important;
    margin: 0 0 4px;
}
.sidebar-brand-sub {
    font-size: 0.75rem;
    color: #8A92A6 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Hide Unnecessary Components ── */
footer { visibility: hidden; }
.stDeployButton { display: none; }

/* ── PROFESSIONAL FIX: Desain Tombol Pemicu Sidebar Premium Minimalis ── */
button[data-testid="stSidebarCollapseAction"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E9ECEF !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    display: flex !important;
    visibility: visible !important;
    position: fixed !important;
    top: 18px !important;
    left: 18px !important;
    z-index: 999999 !important;
    border-radius: 8px !important;
    padding: 6px !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* Warna ikon diatur abu-abu gelap korporat agar menyatu sempurna */
button[data-testid="stSidebarCollapseAction"] svg {
    color: #495057 !important;
    fill: #495057 !important;
    width: 18px !important;
    height: 18px !important;
}

/* Efek hover profesional (Sedikit bergeser ke kanan & berubah warna aksen) */
button[data-testid="stSidebarCollapseAction"]:hover {
    background-color: #F8F9FA !important;
    border-color: #2A5298 !important;
    transform: translateX(2px);
}
button[data-testid="stSidebarCollapseAction"]:hover svg {
    color: #2A5298 !important;
    fill: #2A5298 !important;
}
</style>
""", unsafe_allow_html=True)
# ── Chart Theme ───────────────────────────────────────────────────────────────
BG   = '#F8F9FA'
AX_BG  = '#FFFFFF'
GRID   = '#F1F3F5'
SPINE  = '#E9ECEF'
LABEL  = '#8A92A6'
TEXT   = '#2D3142'

plt.rcParams.update({
    'figure.facecolor':     BG,
    'axes.facecolor':       AX_BG,
    'axes.edgecolor':       SPINE,
    'axes.labelcolor':      LABEL,
    'axes.titlecolor':      TEXT,
    'axes.titlesize':       11,
    'axes.titleweight':     '700',
    'axes.titlepad':        16,
    'xtick.color':          LABEL,
    'ytick.color':          LABEL,
    'xtick.labelsize':      9,
    'ytick.labelsize':      9,
    'grid.color':           GRID,
    'grid.linewidth':       0.9,
    'text.color':           TEXT,
    'font.family':          'sans-serif',
    'axes.spines.top':      False,
    'axes.spines.right':    False,
    'axes.spines.left':     False,
    'axes.spines.bottom':   False,
    'figure.dpi':           140,
})

P = {
    'green':  '#1E6B4B',
    'green2': '#D2E8DD',
    'red':    '#A33333',
    'red2':   '#F7D6D6',
    'blue':   '#2A5298',
    'blue2':  '#D1DFE8',
    'ink':    '#242424',
    'sand':   '#B5B5B5',
    'muted':  '#EDEDED',
}

def fmt_rp(val, short=False):
    if short:
        if abs(val) >= 1e9:  return f"Rp {val/1e9:.1f}M"
        if abs(val) >= 1e6:  return f"Rp {val/1e6:.1f}jt"
        return f"Rp {val:,.0f}"
    return f"Rp {val:,.0f}"

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('Data_Finance_Final.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Category'] != 'Uncategorized'].reset_index(drop=True)

    for col, fn in [('Year', lambda d: d.dt.year), ('Month', lambda d: d.dt.month),
                    ('Day', lambda d: d.dt.day), ('DayOfWeek', lambda d: d.dt.dayofweek)]:
        if col not in df.columns:
            df[col] = fn(df['Date'])
    if 'IsWeekend' not in df.columns:
        df['IsWeekend'] = df['DayOfWeek'].isin([5, 6])

    month_id = {7:'Juli',8:'Agustus',9:'September',10:'Oktober',11:'November',12:'Desember'}
    df['Month_Label'] = df['Month'].map(month_id)
    return df

df_raw = load_data()

MONTH_ORDER = ['Juli','Agustus','September','Oktober','November','Desember']
MONTH_NAMES = {7:'Juli',8:'Agustus',9:'September',10:'Oktober',11:'November',12:'Desember'}
DAY_NAMES   = {0:'Sen',1:'Sel',2:'Rab',3:'Kam',4:'Jum',5:'Sab',6:'Min'}
DAY_FULL    = {0:'Senin',1:'Selasa',2:'Rabu',3:'Kamis',4:'Jumat',5:'Sabtu',6:'Minggu'}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <div class="sidebar-brand-title">◈ Arthawise </div>
      <div class="sidebar-brand-sub">Jul – Des 2025</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<p style='font-size:0.88rem; font-weight:700; margin-bottom:0px; color:#1A1D20;'>Filter Kontrol</p>", unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    all_months = [m for m in MONTH_ORDER if m in df_raw['Month_Label'].unique()]
    sel_months = st.multiselect("Bulan", all_months, default=all_months)

    all_cats = sorted(df_raw['Category'].unique().tolist())
    sel_cats = st.multiselect("Kategori", all_cats, default=all_cats)

    all_accs = sorted(df_raw['Account'].unique().tolist())
    sel_accs = st.multiselect("Metode Pembayaran", all_accs, default=all_accs)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.75rem; color:#495057; font-family:JetBrains Mono,monospace; background:#E9ECEF; padding:10px; border-radius:6px; text-align:center; font-weight:500;'>{len(df_raw):,} total transaksi termuat</div>", unsafe_allow_html=True)

# ── Filtered Data ─────────────────────────────────────────────────────────────
df = df_raw[
    df_raw['Month_Label'].isin(sel_months) &
    df_raw['Category'].isin(sel_cats) &
    df_raw['Account'].isin(sel_accs)
].copy()

expenses_df = df[df['Type'] == 'EXPENSE'].copy()
income_df   = df[df['Type'] == 'INCOME'].copy()

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div class="page-eyebrow">Capstone Project · Analisis Keuangan Pribadi</div>
  <div class="page-title">Dashboard Keuangan Pribadi</div>
  <div class="page-sub">Periode Analisis: <strong>Juli – Desember 2025</strong> &nbsp;·&nbsp; Pemantauan Arus Kas Pasca Transaksi</div>
</div>""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
total_income  = income_df['Amount'].sum()
total_expense = expenses_df['Amount'].sum()
net_cf        = total_income - total_expense
avg_exp       = expenses_df['Amount'].mean() if len(expenses_df) > 0 else 0
cf_class      = "up" if net_cf >= 0 else "down"
cf_sign       = "+" if net_cf >= 0 else "−"

col1, col2, col3, col4 = st.columns(4)
cards = [
    (col1, "green",  "Total Pemasukan",  fmt_rp(total_income, short=True), "",    f"{len(income_df)} transaksi"),
    (col2, "red",    "Total Pengeluaran", fmt_rp(total_expense, short=True), "", f"{len(expenses_df)} transaksi"),
    (col3, "blue",   "Net Cash Flow",     f"{cf_sign} {fmt_rp(abs(net_cf), short=True)}", cf_class, "Surplus" if net_cf>=0 else "Defisit"),
    (col4, "ink",    "Total Transaksi",   f"{len(df):,}", "",              f"Rata rata {fmt_rp(avg_exp, short=True)}/txn"),
 ]
for col, variant, label, value, val_class, sub in cards:
    with col:
        st.markdown(f"""
        <div class="kpi-card {variant}">
          <div class="kpi-accent"></div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-value {val_class}">{value}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def section(num, title, desc=""):
    desc_html = f'<span class="section-desc">{desc}</span>' if desc else ''
    st.markdown(f"""
    <div class="section-wrap">
      <span class="section-num">{num:02d}</span>
      <span class="section-title">{title}</span>
      {desc_html}
    </div>""", unsafe_allow_html=True)

def insight(text, rec=None):
    rec_html = f'<div class="insight-rec"><strong>💡 Rekomendasi:</strong> {rec}</div>' if rec else ''
    st.markdown(f"""
    <div class="insight">
      <div class="insight-icon">◈</div>
      <div class="insight-body">
        <div class="insight-main">{text}</div>
        {rec_html}
      </div>
    </div>""", unsafe_allow_html=True)

def rp_fmt_axis(val, _):
    if abs(val) >= 1e9: return f"{val/1e9:.1f}M"
    if abs(val) >= 1e6: return f"{val/1e6:.0f}jt"
    return f"{val/1e3:.0f}k"

# ── Q1 — Cash Flow Analysis ───────────────────────────────────────────────────
section(1, "Cash Flow Analysis", "Tren bulanan pemasukan & pengeluaran")

# Kembalikan ke logika dataframe asli milikmu
if len(income_df) > 0 and len(expenses_df) > 0:
    # 1. Agregasi Pemasukan Bulanan
    inc_m = income_df.groupby(['Year', 'Month'])['Amount'].sum().reset_index().rename(columns={'Amount': 'Income'})
    # 2. Agregasi Pengeluaran Bulanan
    exp_m = expenses_df.groupby(['Year', 'Month'])['Amount'].sum().reset_index().rename(columns={'Amount': 'Expense'})
    
    # 3. Gabungkan keduanya menjadi monthly_data
    monthly_data = pd.merge(inc_m, exp_m, on=['Year', 'Month'], how='outer').fillna(0)
    monthly_data['Label'] = monthly_data['Month'].map(MONTH_NAMES)
    monthly_data = monthly_data[monthly_data['Label'].isin(sel_months)].copy()
    monthly_data['_ord'] = monthly_data['Label'].apply(lambda x: MONTH_ORDER.index(x) if x in MONTH_ORDER else 99)
    monthly_data = monthly_data.sort_values('_ord').reset_index(drop=True)
    monthly_data['Net'] = monthly_data['Income'] - monthly_data['Expense']

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.0), gridspec_kw={'wspace': 0.16})
    fig.patch.set_facecolor(BG)

  # ── CHART KIRI: Pemasukan vs Pengeluaran (Dengan Label Angka) ──
    x = np.arange(len(monthly_data['Label']))
    width = 0.35

    bars_in  = axes[0].bar(x - width/2, monthly_data['Income'],  width, color=P['green'], label='Pemasukan', zorder=3, edgecolor='none')
    bars_out = axes[0].bar(x + width/2, monthly_data['Expense'], width, color='#F3D1D1',  label='Pengeluaran', zorder=3, edgecolor='none')

    axes[0].set_title('Pemasukan vs Pengeluaran', weight='700')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(monthly_data['Label'], fontsize=9)
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[0].grid(axis='y', zorder=0)

    # Tambahkan batas atas sumbu Y sedikit (margin 15%) agar teks angka teratas tidak terpotong header
    max_val_q1 = max(monthly_data['Income'].max(), monthly_data['Expense'].max())
    axes[0].set_ylim(0, max_val_q1 * 1.15)

    # FIX: Menambahkan label angka di atas batang Pemasukan (Hijau)
    for bar in bars_in:
        val = bar.get_height()
        if val > 0: # Hanya menampilkan jika nilainya tidak nol
            axes[0].text(bar.get_x() + bar.get_width()/2,
                         val + max_val_q1 * 0.02,
                         fmt_rp(val, short=True), ha='center', va='bottom',
                         fontsize=8.5, color=TEXT, weight='600')

    # FIX: Menambahkan label angka di atas batang Pengeluaran (Pink)
    for bar in bars_out:
        val = bar.get_height()
        if val > 0:
            axes[0].text(bar.get_x() + bar.get_width()/2,
                         val + max_val_q1 * 0.02,
                         fmt_rp(val, short=True), ha='center', va='bottom',
                         fontsize=8.5, color=TEXT, weight='600')

    # Kotak legend tetap aman berada di bawah luar plot grafik
    axes[0].legend(frameon=False, fontsize=9, labelcolor=LABEL,
                  loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

    # ── CHART KANAN: Net Cash Flow Bulanan ──
    bars_net = axes[1].bar(monthly_data['Label'], monthly_data['Net'], color='#3B7A57', width=0.42, zorder=3, edgecolor='none')
    
    axes[1].set_title('Net Cash Flow Bulanan', weight='700')
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[1].grid(axis='y', zorder=0)

    for bar, val in zip(bars_net, monthly_data['Net']):
        axes[1].text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + monthly_data['Net'].max()*0.02,
                     fmt_rp(val, short=True), ha='center', va='bottom',
                     fontsize=9, color=TEXT, weight='600')

    plt.tight_layout(pad=1.0)
    st.pyplot(fig); plt.close()   
   # ── CARI BARIS INI TEPAT DI BAWAH PLT.CLOSE() ──
    # Ubah semua 'monthly_cf' menjadi 'monthly_data' agar sinkron dengan data grafik

    avg_ncf    = monthly_data['Net'].mean() # <── Perbaikan variabel dari monthly_cf['NCF']
    max_ncf    = monthly_data.loc[monthly_data['Net'].idxmax()]
    min_ncf    = monthly_data.loc[monthly_data['Net'].idxmin()]
    
    # Ambil label bulan tertinggi dan terendah
    max_cf_lbl = max_ncf['Label']
    min_cf_lbl = min_ncf['Label']

    # Pastikan variabel di dalam fungsi insight juga menggunakan monthly_data
    insight(
        f"Rata-rata net cash flow bulanan berada di angka <strong>{fmt_rp(avg_ncf, short=True)}</strong>. "
        f"Akumulasi surplus tertinggi diamankan pada bulan <strong>{max_cf_lbl}</strong> ({fmt_rp(max_ncf['Net'], short=True)}), "
        f"sedangkan titik selisih paling tipis terjadi di bulan <strong>{min_cf_lbl}</strong> ({fmt_rp(min_ncf['Net'], short=True)}).",
        rec="Pertahankan konsistensi net cash flow positif ini dengan menerapkan alokasi auto-debit tabungan di awal bulan, sesaat setelah alokasi pemasukan utama masuk."
    )

# ── Q2 — Spending per Category ────────────────────────────────────────────────
section(2, "Spending per Category", "Proporsi & rata-rata pengeluaran bulanan")

if len(expenses_df) > 0:
    expense_by_cat  = expenses_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    monthly_exp_cat = expenses_df.groupby(['Month','Category'])['Amount'].sum().reset_index()
    avg_monthly_cat = monthly_exp_cat.groupby('Category')['Amount'].mean().sort_values(ascending=False)
    top_cat = expense_by_cat.idxmax()
    top_pct = expense_by_cat.max() / expense_by_cat.sum() * 100

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.4), gridspec_kw={'wspace':0.18})
    fig.patch.set_facecolor(BG)

    # Donut Chart 
    n = len(expense_by_cat)
    custom_colors = ['#2A5298', '#4A7BB0', '#72A1C6', '#9EC5DC', '#CBE5F0', '#EAF4F8']
    if n > len(custom_colors):
        custom_colors = custom_colors * (n // len(custom_colors) + 1)
    colors_donut = custom_colors[:n]

    wedges, texts, autotexts = axes[0].pie(
        expense_by_cat.values,
        labels=expense_by_cat.index,
        autopct='%1.0f%%',
        startangle=90,
        colors=colors_donut,
        pctdistance=0.75,
        wedgeprops={'linewidth': 2, 'edgecolor': 'white', 'width': 0.55},
        textprops={'fontsize': 9, 'color': TEXT}
    )
    for at in autotexts: at.set_color(TEXT); at.set_fontsize(8.5); at.set_fontweight('700')
    axes[0].set_title('Proporsi Alokasi Total Pengeluaran', weight='700')

    # Horizontal bar — avg monthly
    bars = axes[1].barh(avg_monthly_cat.index, avg_monthly_cat.values,
                        color='#4A7BB0', height=0.52, zorder=3, edgecolor='none')
    axes[1].invert_yaxis()
    axes[1].set_title('Rata rata Pengeluaran Bulanan per Kategori', weight='700')
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[1].grid(axis='x', zorder=0)
    for bar, val in zip(bars, avg_monthly_cat.values):
        axes[1].text(val + avg_monthly_cat.max()*0.02,
                     bar.get_y() + bar.get_height()/2,
                     fmt_rp(val, short=True), va='center', fontsize=8.5, color=TEXT, weight='600')

    plt.tight_layout(pad=1.0)
    st.pyplot(fig); plt.close()

    insight(
        f"Alokasi pos <strong>{top_cat}</strong> teridentifikasi mendominasi struktur belanja dengan porsi sebesar <strong>{top_pct:.1f}%</strong> "
        f"dari total belanja keseluruhan, dengan rerata bulanan mencapai <strong>{fmt_rp(avg_monthly_cat.max(), short=True)}</strong>.",
        rec="Kunci batas aman (capping) lewat sistem budgeting ketat di awal bulan khusus untuk kategori penyerap dana terbesar ini."
    )

# ── Q3 — Weekday vs Weekend ───────────────────────────────────────────────────
section(3, "Weekday vs Weekend", "Pola tren pengeluaran berdasarkan tipe hari")

if len(expenses_df) > 0:
    exp_copy = expenses_df.copy()
    exp_copy['IsWeekend_flag'] = exp_copy['DayOfWeek'].isin([5, 6])
    wkd_avg = exp_copy.groupby('IsWeekend_flag')['Amount'].mean()
    wkd_avg.index = wkd_avg.index.map({False: 'Hari Kerja (Weekday)', True: 'Akhir Pekan (Weekend)'})
    weekday_val = wkd_avg.get('Hari Kerja (Weekday)', 0)
    weekend_val = wkd_avg.get('Akhir Pekan (Weekend)', 0)
    selisih_pct = ((weekend_val - weekday_val) / weekday_val * 100) if weekday_val != 0 else 0

    exp_copy['DayShort'] = exp_copy['DayOfWeek'].map(DAY_NAMES)
    exp_copy['DayFull']  = exp_copy['DayOfWeek'].map(DAY_FULL)
    day_avg = exp_copy.groupby(['DayOfWeek','DayShort'])['Amount'].mean().reset_index().sort_values('DayOfWeek')

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.0), gridspec_kw={'wspace':0.14})
    fig.patch.set_facecolor(BG)

    # ── CHART KIRI: Perbandingan Rerata Nilai (Rapat & Proporsional) ──
    x_pos = [0.3, 0.7] # Mengatur koordinat posisi batang agar berdekatan
    bar_colors_wk = ['#2A5298', '#A33333']
    bars = axes[0].bar(x_pos, wkd_avg.values, color=bar_colors_wk, width=0.18, zorder=3, edgecolor='none')
    
    # Menentukan teks label sumbu X tepat di bawah masing-masing batang
    axes[0].set_xticks(x_pos)
    axes[0].set_xticklabels(wkd_avg.index, fontsize=9)
    
    # FIX: Membatasi ruang kosong sumbu X agar batang kiri & kanan tidak renggang jauh
    axes[0].set_xlim(0.0, 1.0) 
    
    axes[0].set_title('Perbandingan Rata rata Nilai: Weekday vs Weekend', weight='700')
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[0].grid(axis='y', zorder=0)
    
    for bar, val in zip(bars, wkd_avg.values):
        axes[0].text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + wkd_avg.max()*0.02,
                     fmt_rp(val, short=True), ha='center', fontsize=9, color=TEXT, fontweight='700')

 # ── CHART KANAN: Per-day bar (Ditambahkan Label Angka di Atas Batang) ──
    day_colors = [P['red'] if d in [5,6] else '#4A7BB0' for d in day_avg['DayOfWeek']]
    bars2 = axes[1].bar(day_avg['DayShort'], day_avg['Amount'], color=day_colors, width=0.48, zorder=3, edgecolor='none')
    
    # Perbaikan Judul (Memakai Rata-rata)
    axes[1].set_title('Rata-rata Nilai Pengeluaran Harian', weight='700')
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[1].grid(axis='y', zorder=0)

    # Tambahkan batas atas sumbu Y sedikit (margin 15%) agar teks angka tidak mentok/terpotong
    max_val_q3_right = day_avg['Amount'].max()
    axes[1].set_ylim(0, max_val_q3_right * 1.15)

    # FIX: Loop untuk memunculkan angka nominal di atas setiap batang harian
    for bar in bars2:
        val = bar.get_height()
        if val > 0:
            axes[1].text(bar.get_x() + bar.get_width()/2,
                         val + max_val_q3_right * 0.02, # Jarak teks di atas batang
                         fmt_rp(val, short=True), ha='center', va='bottom',
                         fontsize=8.5, color=TEXT, weight='600')

    # Memindahkan posisi legend ke bawah sumbu X secara horizontal
    wkend_p = mpatches.Patch(color=P['red'],  label='Weekend')
    wkday_p = mpatches.Patch(color='#4A7BB0', label='Weekday')
    axes[1].legend(handles=[wkday_p, wkend_p], frameon=False, fontsize=9, labelcolor=LABEL, 
                  loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

    # Menyesuaikan pad agar legend di bawah tidak terpotong saat dirender
    plt.tight_layout(pad=1.0)
    st.pyplot(fig); plt.close()

    direction = "lebih tinggi" if selisih_pct > 0 else "lebih rendah"
    insight(
        f"Secara statistik transaksi, rata-rata nominal pengeluaran di Akhir Pekan (Weekend) berjalan <strong>{abs(selisih_pct):.1f}% {direction}</strong> "
        f"dibandingkan Hari Kerja (<strong>{fmt_rp(weekday_val, short=True)}</strong> vs <strong>{fmt_rp(weekend_val, short=True)}</strong>).",
        rec="Gunakan alokasi dana mandiri (khusus weekend wallet) demi mengunci agar kegiatan rekreasi sabtu-minggu tidak mengambil jatah pos wajib harian."
    )

# ── Q4 — Income Stability ─────────────────────────────────────────────────────
section(4, "Income Stability", "Tingkat konsistensi distribusi pemasukan bulanan")

if len(income_df) > 0:
    monthly_inc = income_df.groupby(['Year','Month'])['Amount'].sum().reset_index()
    monthly_inc['Label'] = monthly_inc['Month'].map(MONTH_NAMES)
    monthly_inc = monthly_inc[monthly_inc['Label'].isin(sel_months)].copy()
    monthly_inc['_ord'] = monthly_inc['Label'].apply(lambda x: MONTH_ORDER.index(x) if x in MONTH_ORDER else 99)
    monthly_inc = monthly_inc.sort_values('_ord').reset_index(drop=True)

    max_inc = monthly_inc.loc[monthly_inc['Amount'].idxmax()]
    min_inc = monthly_inc.loc[monthly_inc['Amount'].idxmin()]
    selisih = max_inc['Amount'] - min_inc['Amount']
    avg_inc = monthly_inc['Amount'].mean()

    fig, ax = plt.subplots(figsize=(13, 4.0))
    fig.patch.set_facecolor(BG)

    bar_cols = []
    for v in monthly_inc['Amount']:
        if v == monthly_inc['Amount'].max():   bar_cols.append(P['green'])
        elif v == monthly_inc['Amount'].min(): bar_cols.append('#D98888')
        else:                                  bar_cols.append('#B3C9DB')

    bars = ax.bar(monthly_inc['Label'], monthly_inc['Amount'],
                  color=bar_cols, width=0.42, zorder=3, edgecolor='none')
    ax.axhline(avg_inc, color='#8C8C8C', linewidth=1.2, linestyle='--', zorder=4, label=f'Garis Rerata ({fmt_rp(avg_inc, short=True)})')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    ax.grid(axis='y', zorder=0)
    ax.set_title('Volatilitas Total Pemasukan Bulanan', weight='700')

    for bar, val in zip(bars, monthly_inc['Amount']):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + monthly_inc['Amount'].max()*0.02,
                fmt_rp(val, short=True), ha='center', va='bottom',
                fontsize=9, color=TEXT, weight='600')

   # FIX: Pindahkan legend ke bawah grafik agar tidak tumpang tindih
    hi_p  = mpatches.Patch(color=P['green'], label=f"Pemasukan Tertinggi — {max_inc['Label']}")
    lo_p  = mpatches.Patch(color='#D98888',  label=f"Pemasukan Terendah — {min_inc['Label']}")
    mid_p = mpatches.Patch(color='#B3C9DB', label='Normal')
    
    # loc='upper center' dan bbox_to_anchor membuat legend berada di bawah sumbu X
    ax.legend(handles=[hi_p, lo_p, mid_p], frameon=False, fontsize=9, labelcolor=LABEL, 
              loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

    # Tambahkan pad sedikit di bawah agar legend tidak terpotong
    plt.tight_layout(pad=1.0)
    st.pyplot(fig); plt.close()

    # REVISI TEKS INSIGHT BOX: Mengubah istilah agar sinkron
    insight(
        f"Inflow **tertinggi** diperoleh pada bulan <strong>{max_inc['Label']} 2025</strong> ({fmt_rp(max_inc['Amount'], short=True)}) "
        f"sedangkan titik **terendah** ada pada <strong>{min_inc['Label']} 2025</strong> ({fmt_rp(min_inc['Amount'], short=True)}). "
        f"Rentang deviasi gap pencapaian senilai <strong>{fmt_rp(selisih, short=True)}</strong>.",
        rec="Saat pemasukan berada di atas garis rata-rata bulanan, segera amankan surplus tersebut ke dalam instrumen likuid sebagai penyeimbang cash flow bulanan berikutnya."
    )
# ── Q5 — Payment Method ───────────────────────────────────────────────────────
section(5, "Payment Method Analysis", "Analisis preferensi intensitas instrumen pembayaran")

if len(expenses_df) > 0:
    pmt = expenses_df.groupby('Account')['Amount'].agg(
        Frekuensi='count', Total='sum', Rata_rata='mean'
    ).sort_values('Frekuensi', ascending=False).reset_index()

    top_acc = pmt.iloc[0]
    n_acc   = len(pmt)

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.0), gridspec_kw={'wspace':0.14})
    fig.patch.set_facecolor(BG)

    # Frequency
    bars1 = axes[0].bar(pmt['Account'], pmt['Frekuensi'], color='#2A5298', width=0.42, zorder=3, edgecolor='none')
    axes[0].set_title('Frekuensi Intensitas Penggunaan', weight='700')
    axes[0].set_ylabel('Jumlah Transaksi', color=LABEL, fontsize=9)
    axes[0].grid(axis='y', zorder=0)
    for bar, val in zip(bars1, pmt['Frekuensi']):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(pmt['Frekuensi'])*0.02,
                     str(int(val)), ha='center', fontsize=9, color=TEXT, fontweight='700')

    # Avg value
    bars2 = axes[1].bar(pmt['Account'], pmt['Rata_rata'], color='#E6A15C', width=0.42, zorder=3, edgecolor='none')
    axes[1].set_title('Rata rata Nilai Nominal per Transaksi', weight='700')
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[1].grid(axis='y', zorder=0)
    for bar, val in zip(bars2, pmt['Rata_rata']):
        axes[1].text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + pmt['Rata_rata'].max()*0.02,
                     fmt_rp(val, short=True), ha='center', fontsize=8.5, color=TEXT, weight='600')

    plt.tight_layout(pad=1.0)
    st.pyplot(fig); plt.close()

    insight(
        f"Metode transaksi utama dengan akumulasi muatan tertinggi dipegang oleh <strong>{top_acc['Account']}</strong> "
        f"(berjumlah <strong>{int(top_acc['Frekuensi'])} transaksi</strong>, dengan rata-rata spend sebesar <strong>{fmt_rp(top_acc['Rata_rata'], short=True)}</strong> setiap kali digunakan).",
        rec="Pasang fitur notifikasi pengeluaran seketika (real-time alert) dan batasi saldo auto-top-up bulanan pada dompet digital/rekening aktif tersebut."
    )

# ── Q6 — Daily Spending Pattern ───────────────────────────────────────────────
section(6, "Daily Spending Pattern", "Akumulasi volume kapital pengeluaran harian")

if len(expenses_df) > 0:
    exp_day = expenses_df.copy()
    exp_day['DayShort'] = exp_day['DayOfWeek'].map(DAY_NAMES)
    exp_day['DayFull']  = exp_day['DayOfWeek'].map(DAY_FULL)
    daily   = exp_day.groupby(['DayOfWeek','DayShort'])['Amount'].sum().reset_index().sort_values('DayOfWeek')

    max_day = daily.loc[daily['Amount'].idxmax()]
    min_day = daily.loc[daily['Amount'].idxmin()]
    selisih = max_day['Amount'] - min_day['Amount']

    fig, ax = plt.subplots(figsize=(13, 4.0))
    fig.patch.set_facecolor(BG)

    # FIX LOGIKA WARNA: Hanya bedakan warna untuk nilai tertinggi dan terendah
    day_cols = []
    for i, row in daily.iterrows():
        if row['Amount'] == daily['Amount'].max():
            day_cols.append(P['red'])        # Warna merah untuk Puncak Pengeluaran
        elif row['Amount'] == daily['Amount'].min():
            day_cols.append(P['green2'])     # Warna hijau soft untuk Titik Hemat
        else:
            day_cols.append('#4A7BB0')       # Warna biru netral untuk semua hari biasa lainnya

    bars = ax.bar(daily['DayShort'], daily['Amount'], color=day_cols, width=0.48, zorder=3, edgecolor='none')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    ax.grid(axis='y', zorder=0)
    ax.set_title('Akumulasi Beban Kapital Pengeluaran Berdasarkan Hari', weight='700')

    for bar, val in zip(bars, daily['Amount']):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + daily['Amount'].max()*0.02,
                fmt_rp(val, short=True), ha='center', va='bottom',
                fontsize=9, color=TEXT, weight='600')

   # ── KODE SEBELUMNYA (Bagian Bar & Batang) ──
    # ... (biarkan kode pembuatan bar tetap sama)

    # FIX: Pindahkan legend ke bawah grafik agar tidak tumpang tindih
    hi_p  = mpatches.Patch(color=P['red'],   label=f"Puncak Pengeluaran — Hari {exp_day[exp_day['DayOfWeek']==max_day['DayOfWeek']]['DayFull'].iloc[0]}")
    lo_p  = mpatches.Patch(color=P['green2'], label=f"Titik Hemat — Hari {exp_day[exp_day['DayOfWeek']==min_day['DayOfWeek']]['DayFull'].iloc[0]}")
    
    # Ditata horizontal (ncol=2) tepat di bawah grafik
    ax.legend(handles=[hi_p, lo_p], frameon=False, fontsize=9, labelcolor=LABEL, 
              loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

    # Tambahkan pad sedikit di bawah agar legend tidak terpotong
    plt.tight_layout(pad=1.0)
    st.pyplot(fig); plt.close()

    max_day_name = exp_day[exp_day['DayOfWeek']==max_day['DayOfWeek']]['DayFull'].iloc[0]
    min_day_name = exp_day[exp_day['DayOfWeek']==min_day['DayOfWeek']]['DayFull'].iloc[0]
    insight(
        f"Akumulasi pengeluaran tertinggi terkonsentrasi penuh pada hari <strong>{max_day_name}</strong> ({fmt_rp(max_day['Amount'], short=True)}) "
        f"sedangkan titik terendah harian berada di hari <strong>{min_day_name}</strong> ({fmt_rp(min_day['Amount'], short=True)}). "
        f"Deviasi pengeluaran antar kedua hari tersebut berjarak sebesar <strong>{fmt_rp(selisih, short=True)}</strong>.",
        rec=f"Jadikan siklus hari {max_day_name} sebagai checkpoint evaluasi mingguan, dan biasakan untuk menahan atau menggeser transaksi non-esensial ke hari hemat."
    )
# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:54px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='border-top:2px solid #E9ECEF; padding-top:24px; margin-bottom: 32px;
            display:flex; justify-content:between; align-items:center;
            font-size:0.75rem; color:#8A92A6; font-family:JetBrains Mono, monospace; font-weight:500;'>
  <span style='flex-grow: 1;'>◈ Personal Finance Tracker</span>
  <span>Capstone Project · Dicoding 2025</span>
</div>""", unsafe_allow_html=True)
