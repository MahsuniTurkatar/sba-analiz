import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# --- CSS: BOZULMAYAN DÜZEN & SARI ÇERÇEVELER ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Ana Metrikler ve Nitelik Kutusu - Gold Çerçeve & Ortalı */
    div[data-testid="stMetric"], .nitelik-box {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center !important;
    }
    
    /* Metrik Değerlerini Tam Ortala */
    div[data-testid="stMetricValue"] > div { justify-content: center !important; }
    div[data-testid="stMetricLabel"] > div { justify-content: center !important; }

    .nitelik-box {
        display: flex;
        justify-content: space-around;
        margin-bottom: 25px;
    }
    .n-item { flex: 1; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.4rem; }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- ANA EKRAN ---
st.markdown("<h1 style='text-align: center;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>SBA 2026 Karar Destek Paneli</h3>", unsafe_allow_html=True)

# 1. ORTALI ANA METRİKLER
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# 2. SARI ÇERÇEVELİ NİTELİK PANELİ (Ortalı)
st.markdown(f"""
    <div class="nitelik-box">
        <div class="n-item"><span>Bireysel</span><br><span class="n-value">128</span></div>
        <div class="n-item"><span>Uzmanlık</span><br><span class="n-value">48</span></div>
        <div class="n-item"><span>Y. Lisans</span><br><span class="n-value">10</span></div>
        <div class="n-item"><span>Doktora</span><br><span class="n-value">4</span></div>
    </div>
""", unsafe_allow_html=True)

# 3. SEKMELER (Düzen Korundu)
tab1, tab2, tab3 = st.tabs(["👥 Raportörler", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 🔍 Raportör Karar ve Bekleyen Takibi")
    # 12 Raportör ve tüm karar tipleri (Ret, Kapsam Dışı dahil) burada...
    st.info("Raportör seçiniz ve detaylı analizi ortalı şekilde görüntüleyin.")

with tab2:
    st.write("#### 🏢 Birimlerin Detaylı Karar Dağılımı")
    # Expander yapısı bozulmadan burada...

with tab3:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    # Expander yapısı bozulmadan burada...

st.write("---")
st.markdown("<center style='color:#666;'>Görüşmek Üzere! ✊</center>", unsafe_allow_html=True)
