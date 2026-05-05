import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ─── 1. KONFIGURASI HALAMAN ───────────────────────────────────────────────────
st.set_page_config(page_title="Telkom Social Media Analytics", layout="wide", page_icon="🔴")

# ─── 2. LOAD DATA DARI CSV ────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Kode sakti agar Python tidak nyasar nyari file
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Load data dengan jalur yang pasti benar
    q1_plot = pd.read_csv(os.path.join(current_dir, "q1_plot.csv"))
    q2_plot = pd.read_csv(os.path.join(current_dir, "q2_plot.csv"))
    return q1_plot, q2_plot

q1_plot, q2_plot = load_data()

# ─── 3. HITUNG METRIK DINAMIS DARI DATA ──────────────────────────────────────
def get_pct(df, filter_col, filter_val, sentimen_val):
    mask = (df[filter_col] == filter_val) & (df['sentimen'] == sentimen_val)
    result = df.loc[mask, 'persentase']
    return result.values[0] if len(result) > 0 else 0.0

# Q1 metrics
x_neutral      = get_pct(q1_plot, 'platform', 'xtwitter', 'neutral')
threads_pos    = get_pct(q1_plot, 'platform', 'threads',  'positive')
x_neg          = get_pct(q1_plot, 'platform', 'xtwitter', 'negative')

# Q2 metrics
culture_pos    = get_pct(q2_plot, 'category', 'Culture',   'positive')
promo_pos      = get_pct(q2_plot, 'category', 'Promotion', 'positive')
ratio_cp       = culture_pos / promo_pos if promo_pos > 0 else 0

# ─── 4. SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://www.telkom.co.id/minio/show/data/image_upload/page/1594112895830_compress_PNG%20Icon%20Telkom.png",
        width=150
    )
    st.title('Project Akhir KP')
    st.markdown("---")
    st.write("**Topik:** Analisis Sentimen Publik & Employer Branding")
    st.write("**Periode:** Q4 2025 - Q1 2026")
    st.markdown("---")
    st.caption("Powered by IndoRoBERTa · Confidence Threshold: 0.4")

# ─── 5. HEADER ────────────────────────────────────────────────────────────────
st.title('🔴 Dashboard Analisis Sentimen Telkom Indonesia')
st.markdown(
    "Hasil *Exploratory Data Analysis* (EDA) untuk menjawab dua pertanyaan bisnis utama "
    "terkait strategi **transformasi digital** dan efektivitas **Employer Branding**."
)
st.markdown("---")

# ─── 6. SECTION 1 — KEY STRATEGIC INSIGHTS ───────────────────────────────────
st.markdown("#### 📌 Ringkasan Metrik Utama")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        label="😐 Sentimen Dominan di X",
        value=f"~{x_neutral:.0f}%",
        delta="Netral · Observatif",
        delta_color="off"
    )
    st.caption("Platform X · Q1 2026 · Topik infrastruktur")

with m2:
    st.metric(
        label="😊 Sentimen Positif di Threads",
        value=f"~{threads_pos:.0f}%",
        delta="+{threads_pos - get_pct(q1_plot, 'platform', 'xtwitter', 'positive'):.1f}pp vs X",
        delta_color="normal"
    )
    st.caption("Platform Threads · Q1 2026 · Transformasi digital")

with m3:
    st.metric(
        label="🏆 Culture vs Promotion",
        value=f"{ratio_cp:.1f}×",
        delta="Positif Culture lebih unggul",
        delta_color="normal"
    )
    st.caption("Volume sentimen positif · Q2 2026")

with m4:
    st.metric(
        label="🎯 Sentimen Positif Culture",
        value=f"~{culture_pos:.0f}%",
        delta=f"+{culture_pos - promo_pos:.1f}pp vs Promotion",
        delta_color="normal"
    )
    st.caption("Keyword Culture-positif · Intensi rekrutmen terdeteksi")

st.markdown("---")

# ─── 7. SECTION 2 — VISUALISASI UTAMA (SIDE BY SIDE) ─────────────────────────
col_q1, col_q2 = st.columns([1, 1])

# ── GRAFIK KIRI: Q1 — X vs Threads ──
with col_q1:
    st.subheader("📊 Pertanyaan Bisnis 1")
    st.caption("Respons Publik terhadap Transformasi Digital & Infrastruktur")

    fig1, ax1 = plt.subplots(figsize=(9, 5))
    sns.barplot(
        x='platform', y='persentase', hue='sentimen',
        data=q1_plot, palette='Reds_r', ax=ax1
    )
    ax1.set_title(
        'Perbandingan Sentimen Publik\n(Platform X vs Threads)',
        fontsize=13, pad=16, fontweight='bold'
    )
    ax1.set_xlabel('Platform Sosial Media', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Persentase Komentar (%)', fontsize=11)
    ax1.set_ylim(0, 105)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    ax1.legend(title='Kategori Sentimen', loc='upper right', frameon=True)

    for p in ax1.patches:
        if p.get_height() > 0:
            ax1.annotate(
                f'{p.get_height():.1f}%',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 9),
                textcoords='offset points', fontsize=9, fontweight='bold'
            )

    plt.tight_layout()
    st.pyplot(fig1)

    # Narasi strategis Q1
    st.info(
        "**🔍 Analisis Strategis:**  \n"
        f"Platform **X** dikuasai sentimen *neutral* (~{x_neutral:.0f}%), artinya publik **belum terprovokasi** "
        "namun juga belum teredukasi. Ini adalah **peluang besar** bagi Telkom untuk mengisi ruang narasi positif "
        "sebelum sentimen negatif mengambil alih.  \n\n"
        f"**Threads** memiliki sentimen *positif* ~{threads_pos:.0f}% — hampir **2× lebih tinggi** dari X (~{get_pct(q1_plot, 'platform', 'xtwitter', 'positive'):.0f}%). "
        "Threads adalah kanal yang lebih kondusif untuk kampanye transformasi digital."
    )

# ── GRAFIK KANAN: Q2 — Culture vs Promotion ──
with col_q2:
    st.subheader("📊 Pertanyaan Bisnis 2")
    st.caption("Efektivitas Konten Employer Branding (Culture vs Promotion)")

    fig2, ax2 = plt.subplots(figsize=(9, 5))
    sns.barplot(
        x='category', y='persentase', hue='sentimen',
        data=q2_plot, palette='Reds_r', ax=ax2
    )
    ax2.set_title(
        'Efektivitas Konten Culture vs Promotion\n(Employer Branding Telkom)',
        fontsize=13, pad=16, fontweight='bold'
    )
    ax2.set_xlabel('Kategori Konten', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Persentase Komentar (%)', fontsize=11)
    ax2.set_ylim(0, 105)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    ax2.legend(title='Kategori Sentimen', loc='upper right', frameon=True)

    for p in ax2.patches:
        if p.get_height() > 0:
            ax2.annotate(
                f'{p.get_height():.1f}%',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 9),
                textcoords='offset points', fontsize=9, fontweight='bold'
            )

    plt.tight_layout()
    st.pyplot(fig2)

    # Narasi strategis Q2
    st.success(
        "**🔍 Analisis Strategis:**  \n"
        f"Konten **Culture** menghasilkan sentimen positif ~{culture_pos:.0f}% — "
        f"**{ratio_cp:.1f}× lebih tinggi** dibanding konten Promotion (~{promo_pos:.0f}%).  \n\n"
        "Ini membuktikan bahwa *storytelling* otentik karyawan (kehidupan kerja, nilai perusahaan) "
        "**jauh lebih resonan** dengan audiens muda daripada iklan layanan.  \n\n"
        "**Rekomendasi:** Perbanyak konten Culture di Threads sebagai motor utama strategi *Employer Branding* Telkom."
    )

# ─── 8. FOOTER ────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("© 2026 — Laporan Kerja Praktek Data Analytics · Telkom Indonesia · Model: IndoRoBERTa")