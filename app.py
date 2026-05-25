import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finance Tracker · Jul–Des 2025",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Design System ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── App Background ── */
.stApp {
    background-color: #F7F5F0;
    color: #1A1A1A;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E8E4DC;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
[data-testid="stSidebar"] * {
    color: #3D3D3D !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #1A1A1A !important;
    color: #F7F5F0 !important;
}
[data-testid="stSidebar"] label {
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: #9E9B94 !important;
}

/* ── Metric Cards ── */
.kpi-row { display: flex; gap: 16px; margin: 0 0 40px 0; }

.kpi-card {
    flex: 1;
    background: #FFFFFF;
    border: 1px solid #E8E4DC;
    border-radius: 4px;
    padding: 28px 24px 24px;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s;
}
.kpi-card:hover { box-shadow: 0 8px 32px rgba(0,0,0,0.06); }

.kpi-accent {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.kpi-card.green  .kpi-accent { background: #2D9B6F; }
.kpi-card.red    .kpi-accent { background: #C94040; }
.kpi-card.blue   .kpi-accent { background: #3A6BC4; }
.kpi-card.ink    .kpi-accent { background: #1A1A1A; }

.kpi-label {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #9E9B94;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.55rem;
    font-weight: 400;
    color: #1A1A1A;
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.kpi-value.up   { color: #2D9B6F; }
.kpi-value.down { color: #C94040; }
.kpi-sub {
    font-size: 0.72rem;
    color: #B8B4AC;
    margin-top: 8px;
    font-weight: 400;
}

/* ── Section Headers ── */
.section-wrap {
    margin: 48px 0 24px;
    display: flex;
    align-items: baseline;
    gap: 14px;
    border-bottom: 1px solid #E8E4DC;
    padding-bottom: 14px;
}
.section-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #C0BBB0;
    letter-spacing: 0.05em;
}
.section-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #1A1A1A;
    margin: 0;
}
.section-desc {
    font-size: 0.78rem;
    color: #9E9B94;
    margin-left: auto;
}

/* ── Insight Box ── */
.insight {
    background: #FFFFFF;
    border: 1px solid #E8E4DC;
    border-left: 3px solid #1A1A1A;
    border-radius: 0 4px 4px 0;
    padding: 18px 22px;
    margin-top: 16px;
    display: flex;
    gap: 20px;
    align-items: flex-start;
}
.insight-icon {
    font-size: 1rem;
    flex-shrink: 0;
    margin-top: 1px;
}
.insight-body {}
.insight-main {
    font-size: 0.83rem;
    color: #3D3D3D;
    line-height: 1.7;
    margin: 0 0 6px;
}
.insight-main strong { color: #1A1A1A; font-weight: 600; }
.insight-rec {
    font-size: 0.77rem;
    color: #9E9B94;
    line-height: 1.6;
}
.insight-rec strong { color: #3A6BC4; font-weight: 500; }

/* ── Page Header ── */
.page-header {
    padding: 40px 0 32px;
    border-bottom: 1px solid #E8E4DC;
    margin-bottom: 40px;
}
.page-eyebrow {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #C0BBB0;
    margin-bottom: 10px;
    font-family: 'DM Mono', monospace;
}
.page-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: #1A1A1A;
    margin: 0 0 8px;
    letter-spacing: -0.03em;
    line-height: 1.1;
}
.page-sub {
    font-size: 0.88rem;
    color: #9E9B94;
    font-weight: 400;
}

/* ── Sidebar Header ── */
.sidebar-brand {
    padding: 28px 20px 20px;
    border-bottom: 1px solid #F0ECE4;
    margin-bottom: 20px;
}
.sidebar-brand-title {
    font-family: 'Sora', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #1A1A1A !important;
    margin: 0 0 2px;
}
.sidebar-brand-sub {
    font-size: 0.7rem;
    color: #C0BBB0 !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
div[data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Chart Theme ───────────────────────────────────────────────────────────────
BG     = '#FFFFFF'
AX_BG  = '#FFFFFF'
GRID   = '#F0ECE4'
SPINE  = '#E8E4DC'
LABEL  = '#9E9B94'
TEXT   = '#1A1A1A'

plt.rcParams.update({
    'figure.facecolor':     BG,
    'axes.facecolor':       AX_BG,
    'axes.edgecolor':       SPINE,
    'axes.labelcolor':      LABEL,
    'axes.titlecolor':      TEXT,
    'axes.titlesize':       11,
    'axes.titleweight':     '600',
    'axes.titlepad':        14,
    'xtick.color':          LABEL,
    'ytick.color':          LABEL,
    'xtick.labelsize':      8.5,
    'ytick.labelsize':      8.5,
    'grid.color':           GRID,
    'grid.linewidth':       0.8,
    'text.color':           TEXT,
    'font.family':          'sans-serif',
    'axes.spines.top':      False,
    'axes.spines.right':    False,
    'axes.spines.left':     False,
    'axes.spines.bottom':   False,
    'figure.dpi':           130,
})

P = {
    'green':  '#2D9B6F',
    'green2': '#A8D5C2',
    'red':    '#C94040',
    'red2':   '#F0BABA',
    'blue':   '#3A6BC4',
    'blue2':  '#B3C8EF',
    'ink':    '#1A1A1A',
    'sand':   '#C0BBB0',
    'muted':  '#E8E4DC',
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
      <div class="sidebar-brand-title">◈ Finance Tracker</div>
      <div class="sidebar-brand-sub">Jul – Des 2025</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("**Filter Data**")
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    all_months = [m for m in MONTH_ORDER if m in df_raw['Month_Label'].unique()]
    sel_months = st.multiselect("Bulan", all_months, default=all_months)

    all_cats = sorted(df_raw['Category'].unique().tolist())
    sel_cats = st.multiselect("Kategori", all_cats, default=all_cats)

    all_accs = sorted(df_raw['Account'].unique().tolist())
    sel_accs = st.multiselect("Metode Pembayaran", all_accs, default=all_accs)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.68rem;color:#C0BBB0;font-family:DM Mono,monospace'>{len(df_raw):,} total transaksi</div>", unsafe_allow_html=True)

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
  <div class="page-title">Dashboard Keuangan<br>Pribadi 2025</div>
  <div class="page-sub">Juli – Desember 2025 &nbsp;·&nbsp; Analisis transaksi harian</div>
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
    (col2, "red",    "Total Pengeluaran", fmt_rp(total_expense, short=True), "down", f"{len(expenses_df)} transaksi"),
    (col3, "blue",   "Net Cash Flow",     f"{cf_sign} {fmt_rp(abs(net_cf), short=True)}", cf_class, "Surplus" if net_cf>=0 else "Defisit"),
    (col4, "ink",    "Total Transaksi",   f"{len(df):,}", "",              f"Rata-rata {fmt_rp(avg_exp, short=True)}/txn"),
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

monthly_cf = df.groupby(['Year','Month','Type'])['Amount'].sum().unstack(fill_value=0).reset_index()
for c in ['EXPENSE','INCOME']:
    if c not in monthly_cf.columns: monthly_cf[c] = 0
monthly_cf['NCF']   = monthly_cf['INCOME'] - monthly_cf['EXPENSE']
monthly_cf['Label'] = monthly_cf['Month'].map(MONTH_NAMES)
monthly_cf = monthly_cf[monthly_cf['Label'].isin(sel_months)].copy()
monthly_cf['_ord'] = monthly_cf['Label'].apply(lambda x: MONTH_ORDER.index(x) if x in MONTH_ORDER else 99)
monthly_cf = monthly_cf.sort_values('_ord').reset_index(drop=True)

if len(monthly_cf) >= 2:
    fig, axes = plt.subplots(1, 2, figsize=(13, 4), gridspec_kw={'wspace':0.08})
    fig.patch.set_facecolor(BG)

    # Left: grouped bar
    x = np.arange(len(monthly_cf))
    w = 0.38
    axes[0].bar(x - w/2, monthly_cf['INCOME'],  width=w, color=P['green'], label='Pemasukan', zorder=3)
    axes[0].bar(x + w/2, monthly_cf['EXPENSE'], width=w, color=P['red2'],  label='Pengeluaran', zorder=3)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(monthly_cf['Label'], fontsize=8.5)
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[0].grid(axis='y', zorder=0)
    axes[0].set_title('Pemasukan vs Pengeluaran')
    axes[0].legend(frameon=False, fontsize=8, labelcolor=LABEL)

    # Right: net CF line + area
    ncf_vals = monthly_cf['NCF'].values
    colors_bar = [P['green'] if v >= 0 else P['red'] for v in ncf_vals]
    axes[1].bar(x, ncf_vals, color=colors_bar, width=0.5, zorder=3, alpha=0.85)
    axes[1].axhline(0, color=SPINE, linewidth=1, zorder=2)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(monthly_cf['Label'], fontsize=8.5)
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[1].grid(axis='y', zorder=0)
    axes[1].set_title('Net Cash Flow Bulanan')
    for xi, val in zip(x, ncf_vals):
        va = 'bottom' if val >= 0 else 'top'
        offset = max(abs(ncf_vals))*0.03 if val >= 0 else -max(abs(ncf_vals))*0.03
        axes[1].text(xi, val + offset, fmt_rp(val, short=True),
                     ha='center', va=va, fontsize=7.5, color=LABEL)

    plt.tight_layout(pad=1.5)
    st.pyplot(fig); plt.close()

    avg_ncf    = monthly_cf['NCF'].mean()
    worst_mth  = monthly_cf.loc[monthly_cf['NCF'].idxmin(), 'Label']
    pct_change = ((monthly_cf['NCF'].iloc[-1] - monthly_cf['NCF'].iloc[0]) / abs(monthly_cf['NCF'].iloc[0]) * 100
                  if monthly_cf['NCF'].iloc[0] != 0 else 0)
    insight(
        f"Rata-rata net cash flow bulanan sebesar <strong>{fmt_rp(avg_ncf, short=True)}</strong>. "
        f"Titik terendah terjadi pada <strong>{worst_mth} 2025</strong>. "
        f"Perubahan dari bulan pertama ke terakhir: <strong>{'+'if pct_change>=0 else ''}{pct_change:.1f}%</strong>.",
        rec="Siapkan sinking fund sejak pertengahan tahun agar surplus tidak merosot di bulan akhir."
    )

# ── Q2 — Spending per Category ────────────────────────────────────────────────
section(2, "Spending per Category", "Proporsi & rata-rata pengeluaran bulanan")

if len(expenses_df) > 0:
    expense_by_cat  = expenses_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    monthly_exp_cat = expenses_df.groupby(['Month','Category'])['Amount'].sum().reset_index()
    avg_monthly_cat = monthly_exp_cat.groupby('Category')['Amount'].mean().sort_values(ascending=False)
    top_cat = expense_by_cat.idxmax()
    top_pct = expense_by_cat.max() / expense_by_cat.sum() * 100

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5), gridspec_kw={'wspace':0.06})
    fig.patch.set_facecolor(BG)

    # Donut
    n = len(expense_by_cat)
    colors_donut = [plt.cm.RdYlGn(0.1 + 0.8 * i / max(n-1,1)) for i in range(n)]
    wedges, texts, autotexts = axes[0].pie(
        expense_by_cat.values,
        labels=expense_by_cat.index,
        autopct='%1.0f%%',
        startangle=90,
        colors=colors_donut,
        pctdistance=0.78,
        wedgeprops={'linewidth':2, 'edgecolor': BG, 'width':0.65},
        textprops={'fontsize':8, 'color': LABEL}
    )
    for at in autotexts: at.set_color(TEXT); at.set_fontsize(7.5); at.set_fontweight('500')
    axes[0].set_title('Proporsi Total Pengeluaran')

    # Horizontal bar — avg monthly
    colors_bar = [plt.cm.RdYlGn(0.1 + 0.8 * i / max(len(avg_monthly_cat)-1,1))
                  for i in range(len(avg_monthly_cat))]
    bars = axes[1].barh(avg_monthly_cat.index, avg_monthly_cat.values,
                        color=colors_bar, height=0.55, zorder=3)
    axes[1].invert_yaxis()
    axes[1].set_title('Rata-rata Pengeluaran Bulanan per Kategori')
    axes[1].set_xlabel('Rp', color=LABEL, fontsize=8.5)
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[1].grid(axis='x', zorder=0)
    axes[1].tick_params(axis='y', labelsize=8.5)
    for bar, val in zip(bars, avg_monthly_cat.values):
        axes[1].text(val + avg_monthly_cat.max()*0.01,
                     bar.get_y() + bar.get_height()/2,
                     fmt_rp(val, short=True), va='center', fontsize=7.5, color=LABEL)

    plt.tight_layout(pad=1.5)
    st.pyplot(fig); plt.close()

    insight(
        f"Kategori <strong>{top_cat}</strong> mendominasi dengan <strong>{top_pct:.1f}%</strong> "
        f"dari total pengeluaran. Rata-rata bulanannya mencapai <strong>{fmt_rp(avg_monthly_cat.max(), short=True)}</strong>.",
        rec="Terapkan budget per kategori dengan batas bulanan agar pengeluaran kategori dominan tetap terkontrol."
    )

# ── Q3 — Weekday vs Weekend ───────────────────────────────────────────────────
section(3, "Weekday vs Weekend", "Pola pengeluaran berdasarkan hari")

if len(expenses_df) > 0:
    exp_copy = expenses_df.copy()
    exp_copy['IsWeekend_flag'] = exp_copy['DayOfWeek'].isin([5, 6])
    wkd_avg = exp_copy.groupby('IsWeekend_flag')['Amount'].mean()
    wkd_avg.index = wkd_avg.index.map({False: 'Weekday', True: 'Weekend'})
    weekday_val = wkd_avg.get('Weekday', 0)
    weekend_val = wkd_avg.get('Weekend', 0)
    selisih_pct = ((weekend_val - weekday_val) / weekday_val * 100) if weekday_val != 0 else 0

    exp_copy['DayShort'] = exp_copy['DayOfWeek'].map(DAY_NAMES)
    exp_copy['DayFull']  = exp_copy['DayOfWeek'].map(DAY_FULL)
    day_avg = exp_copy.groupby(['DayOfWeek','DayShort'])['Amount'].mean().reset_index().sort_values('DayOfWeek')

    fig, axes = plt.subplots(1, 2, figsize=(13, 4), gridspec_kw={'wspace':0.08})
    fig.patch.set_facecolor(BG)

    # Weekday vs Weekend comparison
    bar_colors_wk = [P['blue'], P['red']]
    bars = axes[0].bar(wkd_avg.index, wkd_avg.values, color=bar_colors_wk, width=0.35, zorder=3)
    axes[0].set_title('Rata-rata: Weekday vs Weekend')
    axes[0].set_ylabel('Rp', color=LABEL, fontsize=8.5)
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[0].grid(axis='y', zorder=0)
    for bar, val in zip(bars, wkd_avg.values):
        axes[0].text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + wkd_avg.max()*0.02,
                     fmt_rp(val, short=True), ha='center', fontsize=9, color=TEXT, fontweight='500')

    # Per-day bar
    day_colors = [P['red'] if d in [5,6] else P['blue2'] for d in day_avg['DayOfWeek']]
    bars2 = axes[1].bar(day_avg['DayShort'], day_avg['Amount'], color=day_colors, width=0.55, zorder=3)
    axes[1].set_title('Rata-rata Pengeluaran per Hari')
    axes[1].set_ylabel('Rp', color=LABEL, fontsize=8.5)
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[1].grid(axis='y', zorder=0)
    wkend_p = mpatches.Patch(color=P['red'],  label='Weekend')
    wkday_p = mpatches.Patch(color=P['blue2'], label='Weekday')
    axes[1].legend(handles=[wkday_p, wkend_p], frameon=False, fontsize=8, labelcolor=LABEL)

    plt.tight_layout(pad=1.5)
    st.pyplot(fig); plt.close()

    direction = "lebih tinggi" if selisih_pct > 0 else "lebih rendah"
    insight(
        f"Rata-rata pengeluaran Weekend <strong>{direction} {abs(selisih_pct):.1f}%</strong> "
        f"dibanding Weekday (<strong>{fmt_rp(weekday_val, short=True)}</strong> vs <strong>{fmt_rp(weekend_val, short=True)}</strong>).",
        rec="Tetapkan weekend budget khusus untuk pengeluaran non-esensial di Sabtu dan Minggu."
    )

# ── Q4 — Income Stability ─────────────────────────────────────────────────────
section(4, "Income Stability", "Konsistensi pemasukan bulanan Jul–Des 2025")

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

    fig, ax = plt.subplots(figsize=(13, 4))
    fig.patch.set_facecolor(BG)

    bar_cols = []
    for v in monthly_inc['Amount']:
        if v == monthly_inc['Amount'].max():   bar_cols.append(P['green'])
        elif v == monthly_inc['Amount'].min(): bar_cols.append(P['red2'])
        else:                                   bar_cols.append(P['blue2'])

    bars = ax.bar(monthly_inc['Label'], monthly_inc['Amount'],
                  color=bar_cols, width=0.5, zorder=3)
    ax.axhline(avg_inc, color=P['sand'], linewidth=1.2, linestyle='--', zorder=4, label=f'Rata-rata ({fmt_rp(avg_inc, short=True)})')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    ax.grid(axis='y', zorder=0)
    ax.set_title('Total Pemasukan Bulanan (Jul–Des 2025)')
    ax.legend(frameon=False, fontsize=8, labelcolor=LABEL)

    for bar, val in zip(bars, monthly_inc['Amount']):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + monthly_inc['Amount'].max()*0.01,
                fmt_rp(val, short=True), ha='center', va='bottom',
                fontsize=8, color=LABEL)

    hi_p  = mpatches.Patch(color=P['green'], label=f"Tertinggi — {max_inc['Label']}")
    lo_p  = mpatches.Patch(color=P['red2'],  label=f"Terendah — {min_inc['Label']}")
    mid_p = mpatches.Patch(color=P['blue2'], label='Bulan lainnya')
    ax.legend(handles=[hi_p, lo_p, mid_p], frameon=False, fontsize=8, labelcolor=LABEL)

    plt.tight_layout(pad=1.5)
    st.pyplot(fig); plt.close()

    insight(
        f"Pemasukan tertinggi: <strong>{max_inc['Label']} 2025</strong> ({fmt_rp(max_inc['Amount'], short=True)}). "
        f"Terendah: <strong>{min_inc['Label']} 2025</strong> ({fmt_rp(min_inc['Amount'], short=True)}). "
        f"Selisih <strong>{fmt_rp(selisih, short=True)}</strong> — rata-rata {fmt_rp(avg_inc, short=True)}/bulan.",
        rec="Sisihkan kelebihan dari bulan pemasukan tinggi sebagai income buffer untuk bulan pemasukan rendah."
    )

# ── Q5 — Payment Method ───────────────────────────────────────────────────────
section(5, "Payment Method Analysis", "Frekuensi & rata-rata nilai per metode")

if len(expenses_df) > 0:
    pmt = expenses_df.groupby('Account')['Amount'].agg(
        Frekuensi='count', Total='sum', Rata_rata='mean'
    ).sort_values('Frekuensi', ascending=False).reset_index()

    top_acc = pmt.iloc[0]
    n_acc   = len(pmt)

    fig, axes = plt.subplots(1, 2, figsize=(13, 4), gridspec_kw={'wspace':0.08})
    fig.patch.set_facecolor(BG)

    colors_acc = [plt.cm.Blues(0.4 + 0.5 * i / max(n_acc-1,1)) for i in range(n_acc)]

    # Frequency
    bars1 = axes[0].bar(pmt['Account'], pmt['Frekuensi'], color=colors_acc, width=0.5, zorder=3)
    axes[0].set_title('Frekuensi Penggunaan')
    axes[0].set_ylabel('Jumlah Transaksi', color=LABEL, fontsize=8.5)
    axes[0].grid(axis='y', zorder=0)
    for bar, val in zip(bars1, pmt['Frekuensi']):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                     str(int(val)), ha='center', fontsize=9, color=TEXT, fontweight='500')

    # Avg value
    colors_acc2 = [plt.cm.Oranges(0.35 + 0.5 * i / max(n_acc-1,1)) for i in range(n_acc)]
    bars2 = axes[1].bar(pmt['Account'], pmt['Rata_rata'], color=colors_acc2, width=0.5, zorder=3)
    axes[1].set_title('Rata-rata Nilai Transaksi')
    axes[1].set_ylabel('Rp', color=LABEL, fontsize=8.5)
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    axes[1].grid(axis='y', zorder=0)
    for bar, val in zip(bars2, pmt['Rata_rata']):
        axes[1].text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + pmt['Rata_rata'].max()*0.02,
                     fmt_rp(val, short=True), ha='center', fontsize=8, color=LABEL)

    plt.tight_layout(pad=1.5)
    st.pyplot(fig); plt.close()

    insight(
        f"Metode paling sering digunakan: <strong>{top_acc['Account']}</strong> "
        f"(<strong>{int(top_acc['Frekuensi'])} transaksi</strong>, rata-rata <strong>{fmt_rp(top_acc['Rata_rata'], short=True)}</strong>/txn).",
        rec="Aktifkan notifikasi transaksi real-time dan tetapkan batas top-up bulanan pada metode yang paling sering digunakan."
    )

# ── Q6 — Daily Spending Pattern ───────────────────────────────────────────────
section(6, "Daily Spending Pattern", "Total pengeluaran per hari dalam seminggu")

if len(expenses_df) > 0:
    exp_day = expenses_df.copy()
    exp_day['DayShort'] = exp_day['DayOfWeek'].map(DAY_NAMES)
    exp_day['DayFull']  = exp_day['DayOfWeek'].map(DAY_FULL)
    daily   = exp_day.groupby(['DayOfWeek','DayShort'])['Amount'].sum().reset_index().sort_values('DayOfWeek')

    max_day = daily.loc[daily['Amount'].idxmax()]
    min_day = daily.loc[daily['Amount'].idxmin()]
    selisih = max_day['Amount'] - min_day['Amount']

    fig, ax = plt.subplots(figsize=(13, 4))
    fig.patch.set_facecolor(BG)

    day_cols = []
    for i, row in daily.iterrows():
        if row['Amount'] == daily['Amount'].max():   day_cols.append(P['red'])
        elif row['Amount'] == daily['Amount'].min(): day_cols.append(P['green2'])
        else:
            day_cols.append(P['blue2'] if row['DayOfWeek'] < 5 else P['red2'])

    bars = ax.bar(daily['DayShort'], daily['Amount'], color=day_cols, width=0.55, zorder=3)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(rp_fmt_axis))
    ax.grid(axis='y', zorder=0)
    ax.set_title('Total Pengeluaran per Hari (Jul–Des 2025)')
    ax.set_ylabel('Total Rp', color=LABEL, fontsize=8.5)

    for bar, val in zip(bars, daily['Amount']):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + daily['Amount'].max()*0.01,
                fmt_rp(val, short=True), ha='center', va='bottom',
                fontsize=8, color=LABEL)

    hi_p  = mpatches.Patch(color=P['red'],   label=f"Tertinggi — {exp_day[exp_day['DayOfWeek']==max_day['DayOfWeek']]['DayFull'].iloc[0]}")
    lo_p  = mpatches.Patch(color=P['green2'],label=f"Terendah — {exp_day[exp_day['DayOfWeek']==min_day['DayOfWeek']]['DayFull'].iloc[0]}")
    ax.legend(handles=[hi_p, lo_p], frameon=False, fontsize=8, labelcolor=LABEL)

    plt.tight_layout(pad=1.5)
    st.pyplot(fig); plt.close()

    max_day_name = exp_day[exp_day['DayOfWeek']==max_day['DayOfWeek']]['DayFull'].iloc[0]
    min_day_name = exp_day[exp_day['DayOfWeek']==min_day['DayOfWeek']]['DayFull'].iloc[0]
    insight(
        f"Pengeluaran tertinggi pada hari <strong>{max_day_name}</strong> ({fmt_rp(max_day['Amount'], short=True)}) "
        f"dan terendah pada <strong>{min_day_name}</strong> ({fmt_rp(min_day['Amount'], short=True)}). "
        f"Selisih <strong>{fmt_rp(selisih, short=True)}</strong>.",
        rec=f"Jadikan hari {max_day_name} sebagai 'review day' — tunda pembelian non-esensial ke hari dengan pengeluaran lebih rendah."
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='border-top:1px solid #E8E4DC;padding-top:20px;
            display:flex;justify-content:space-between;align-items:center;
            font-size:0.68rem;color:#C0BBB0;font-family:DM Mono,monospace'>
  <span>◈ Personal Finance Tracker</span>
  <span>Capstone Project · Dicoding 2025</span>
</div>""", unsafe_allow_html=True)
