import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: DARALTILMIŞ VE SARI ÇERÇEVELİ ÜST PANEL ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Genel Kutu Tasarımı */
    .ozet-kutu {
        background-color: #001d3d;
        border: 2px solid #ffc300;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .k-label { color: #ffffff; font-size: 0.85rem; display: block; margin-bottom: 5px; }
    .k-value { color: #ffc300; font-weight: bold; font-size: 1.3rem; }
    .k-sub-value { color: #00b4d8; font-weight: bold; font-size: 1.1rem; }

    /* Başlıklar ve Sekmeler */
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    
    /* Alt Bilgi */
    .footer {
        width: 100%;
        background-color: #000814;
        color: #ffc300;
        text-align: center;
        padding: 20px 0;
        font-weight: bold;
        border-top: 1px solid #ffc300;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ (MEVCUT YAPI KORUNDU) ---
gundem_toplamlar = {"Başvuru": 190, "Düzeltme": 58, "Dilekçe": 42, "Kurul": 4}
nitelikler = {"Bireysel": 128, "Uzmanlık": 48, "Y. Lisans": 10, "Doktora": 4}

# --- ÜST PANEL (DARALTILMIŞ DÜZEN) ---
st.markdown("<h1 style='text-align: center; margin-bottom:0;'>Sağlık Bilimleri Araştırma Etik Kurulu</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-top:0;'>2026 Analiz Raporu</h3>", unsafe_allow_html=True)

# 1. Satır: Ana Metrikler ve Nitelikler (Daraltılmış)
col_m1, col_m2, col_n1, col_n2, col_n3, col_n4 = st.columns([1.2, 1, 1, 1, 1, 1])

with col_m1:
    st.markdown(f'<div class="ozet-kutu"><span class="k-label">📌 Toplam Başvuru</span><span class="k-value">{gundem_toplamlar["Başvuru"]}</span></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="ozet-kutu"><span class="k-label">🗓️ Kurul Sayısı</span><span class="k-value">{gundem_toplamlar["Kurul"]}</span></div>', unsafe_allow_html=True)
with col_n1:
    st.markdown(f'<div class="ozet-kutu"><span class="k-label">Bireysel</span><span class="k-sub-value">{nitelikler["Bireysel"]}</span></div>', unsafe_allow_html=True)
with col_n2:
    st.markdown(f'<div class="ozet-kutu"><span class="k-label">Uzmanlık</span><span class="k-sub-value">{nitelikler["Uzmanlık"]}</span></div>', unsafe_allow_html=True)
with col_n3:
    st.markdown(f'<div class="ozet-kutu"><span class="k-label">Y. Lisans</span><span class="k-sub-value">{nitelikler["Y. Lisans"]}</span></div>', unsafe_allow_html=True)
with col_n4:
    st.markdown(f'<div class="ozet-kutu"><span class="k-label">Doktora</span><span class="k-sub-value">{nitelikler["Doktora"]}</span></div>', unsafe_allow_html=True)

# 2. Satır: Gündem Detay Sayıları (Sarı Çerçeveli Devamı)
st.markdown("<p style='text-align: center; font-size: 0.9rem; color: #ffc300; margin-top: 10px;'>📊 Gündem İşlem Hacmi</p>", unsafe_allow_html=True)
col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    st.markdown(f'<div class="ozet-kutu"><span class="k-label">Toplam Yeni Başvuru</span><span class="k-value">{gundem_toplamlar["Başvuru"]}</span></div>', unsafe_allow_html=True)
with col_g2:
    st.markdown(f'<div class="ozet-kutu"><span class="k-label">Gelen Düzeltme Dosyası</span><span class="k-value">{gundem_toplamlar["Düzeltme"]}</span></div>', unsafe_allow_html=True)
with col_g3:
    st.markdown(f'<div class="ozet-kutu"><span class="k-label">Gelen Dilekçe/Görüş</span><span class="k-value">{gundem_toplamlar["Dilekçe"]}</span></div>', unsafe_allow_html=True)

# --- SEKMELER (DÜZEN KORUNDU) ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Genel Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 📋 Kurul Üye_1 Genel Karar Çizelgesi")
    try:
        # Resim dosyasının adını image_4b8c07.png veya genel_tablo_ekran_goruntusu.png olarak kontrol et
        st.image("genel_tablo_ekran_goruntusu.png", use_column_width=True)
    except:
        st.error("Görsel bulunamadı! Lütfen dosya adını kontrol edin.")

with tab2:
    # Raportör Analizi Kodları (df_raportor üzerinden devam eder)
    st.info("Raportör bazlı detaylı kararlar bu sekmede incelenebilir.")

with tab3:
    st.write("#### 🏢 Birim Analizi (İlk 5)")
    # Birim expander yapısı buraya...

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü (İlk 5)")
    # Sorumlu expander yapısı buraya... (Gonca Hoca düzeltmesi dahil)

# --- ALT BİLGİ ---
st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
