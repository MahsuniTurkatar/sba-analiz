import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: FB SARISI (#FEDD00) VE TABLO DÜZENİ ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Fenerbahçe Sarısı Metrikler */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 2px solid #FEDD00 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center !important;
    }
    
    /* Nitelik Kartları */
    .nitelik-container { display: flex; justify-content: space-between; gap: 10px; margin: 20px 0; }
    .nitelik-card {
        flex: 1; background-color: #001d3d; border: 1px solid #FEDD00;
        border-radius: 8px; padding: 15px; text-align: center;
    }
    .n-val { color: #FEDD00; font-size: 1.5rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.9rem; }
    
    /* GÜNDEM TABLOSU: BAŞLIKLAR VE HÜCRELER TAM ORTALI */
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 85% !important; border-collapse: collapse; color: white; margin-left: auto; margin-right: auto; }
    .styled-table th { 
        background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; 
        padding: 12px; text-align: center !important; 
    }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px; text-align: center !important; }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ (Excel Son Hali) ---

# Gündem Tablosu Verileri
df_gundem = pd.DataFrame({
    "S.NO": ["1.", "2.", "3.", "4.", "TOPLAM"],
    "Gündem Tarihleri": ["06.01.2026", "20.01.2026", "04.02.2026", "17.02.2026", "-"],
    "Başvuru": [55, 45, 45, 45, 190],
    "Düzeltme": [16, 13, 12, 17, 58],
    "Dilekçe": [9, 11, 15, 7, 42],
    "Toplam": [80, 69, 72, 69, 290]
})

# Raportör Analizi Verileri
raportor_data = {
    "Adı Soyadı": [
        "Prof. Dr. Ayşe Nurten AKARSU", "Prof. Dr. M. Özgür UYANIK", "Prof. Dr. Melih Önder BABAOĞLU", 
        "Prof. Dr. Ayşe KİN İŞLER", "Prof. Dr. Yavuz AYHAN", "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY", 
        "Prof. Dr. Gözde GİRGİN", "Doç. Dr. Kübra AYKAÇ", "Doç. Dr. Tolga ÇAKMAK", 
        "Doç. Dr. Burcu ERSÖZ ALAN", "Doç. Dr. Ekim GÜMELER", "Dr. Öğr. Üyesi Müge DEMİR"
    ],
    "Dosya": [31, 35, 28, 25, 25, 36, 36, 38, 25, 36, 26, 39],
    "Onay": [11, 17, 12, 12, 9, 17, 18, 14, 9, 18, 11, 18],
    "Düzeltme": [11, 7, 13, 3, 8, 8, 9, 15, 5, 10, 4, 11],
    "KAEK": [2, 1, 0, 2, 1, 1, 2, 1, 1, 2, 1, 2],
    "Görüş": [1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2],
    "Ret": [1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    "Kapsam Dışı": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0],
    "Geri Çekildi": [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1]
}
df_r = pd.DataFrame(raportor_data)

# --- ANA GÖVDE ---
st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# 190 ve 4 Kurul Sabitlendi
col_main1, col_main2 = st.columns(2)
col_main1.metric("📌 Toplam Başvuru", "190")
col_main2.metric("🗓️ Kurul Sayısı", "4")

# Nitelik Dağılım Kartları
st.markdown("""
    <div class="nitelik-container">
        <div class="nitelik-card"><span class="n-val">128</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">48</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">10</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">4</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# GÜNDEM SAYILARI TABLOSU (Geri Geldi ve Ortalandı)
st.write("### 📅 2026 Gündem Sayıları")
st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.markdown(df_gundem.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- ALT SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 📋 Kurul Karar Çizelgesi (Genel Tablo)")
