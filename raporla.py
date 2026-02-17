import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: FB SARISI (#FEDD00) VE TAM DÜZELTME ---
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
    
    /* TABLO DÜZENİ: BAŞLIKLAR VE HÜCRELER TAM ORTALI */
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 85% !important; border-collapse: collapse; color: white; margin: auto; }
    .styled-table th { 
        background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; 
        padding: 12px; text-align: center !important; 
    }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px; text-align: center !important; }
    
    /* Sekme ve Başlık Renkleri */
    h1, h2, h3, h4, label { color: #FEDD00 !important; }
    .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #001d3d; border-radius: 10px; }
    
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ ---

# 1. Gündem Tablosu (17.02 Dilekçe 6'ya düşürüldü)
df_gundem = pd.DataFrame({
    "S.NO": ["1.", "2.", "3.", "4.", "TOPLAM"],
    "Gündem Tarihleri": ["06.01.2026", "20.01.2026", "04.02.2026", "17.02.2026", "-"],
    "Başvuru": [55, 45, 45, 45, 190],
    "Düzeltme": [16, 13, 12, 17, 58],
    "Dilekçe": [9, 11, 15, 6, 41], # 6 olarak güncellendi
    "Toplam": [80, 69, 72, 68, 289]
})

# 2. Raportör Verileri
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

# --- ANA PANEL ---
st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# Üst Metrikler
c_main1, c_main2 = st.columns(2)
c_main1.metric("📌 Toplam Başvuru", "190")
c_main2.metric("🗓️ Kurul Sayısı", "4")

# Nitelik Kartları
st.markdown("""
    <div class="nitelik-container">
        <div class="nitelik-card"><span class="n-val">128</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">48</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">10</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">4</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# Gündem Tablosu
st.write("### 📅 2026 Gündem Sayıları")
st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.markdown(df_gundem.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER (ÇALIŞIR HALE GETİRİLDİ) ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.write("#### 📋 Kurul Karar Çizelgesi")
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info("Kurul Karar Çizelgesi PNG dosyası bekleniyor...")

with tab2:
    st.write("#### 👥 Raportör Detaylı Analizi")
    sec_r = st.selectbox("Analiz edilecek raportörü seçin:", df_r["Adı Soyadı"].tolist())
    row = df_r[df_r["Adı Soyadı"] == sec_r].iloc[0]
    
    rc1, rc2, rc3 = st.columns(3)
    k_verilen = int(row["Onay"] + row["Düzeltme"] + row["Ret"] + row["KAEK"] + row["Kapsam Dışı"] + row["Geri Çekildi"])
    rc1.metric("📌 Atanan Dosya", row["Dosya"])
    rc2.metric("✅ Karar Verilen", k_verilen)
    rc3.metric("⏳ Bekleyen", int(row["Dosya"] - k_verilen))
    
    st.markdown(f"""
    <div style="background-color:#001d3d; border:1px solid #FEDD00; border-radius:10px; padding:20px; text-align:center;">
        <span style="color:#FEDD00;">✅ ONAY: {row['Onay']}</span> | 
        <span style="color:#FEDD00;">⚠️ DÜZELTME: {row['Düzeltme']}</span> | 
        <span style="color:#FEDD00;">📂 KAEK: {row['KAEK']}</span> | 
        <span style="color:#FEDD00;">📝 GÖRÜŞ: {row['Görüş']}</span> <br><br>
        <span style="color:#FEDD00;">❌ RET: {row['Ret']}</span> | 
        <span style="color:#FEDD00;">🚫 KAPSAM DIŞI: {row['Kapsam Dışı']}</span> | 
        <span style="color:#FEDD00;">🔄 GERİ ÇEKİLDİ: {row['Geri Çekildi']}</span>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.write("#### 🏢 Birim Bazlı Başvuru Dağılımı")
    birimler = [
        {"Ad": "İç Hastalıkları Anabilim Dalı", "T": 27, "B": 18, "U": 6, "Y": 3},
        {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "T": 23, "B": 12, "U": 9, "Y": 2},
        {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "T": 9, "B": 6, "U": 3, "Y": 0},
        {"Ad": "Klinik Eczacılık Anabilim Dalı", "T": 9, "B": 4, "U": 4, "Y": 1},
        {"Ad": "Göğüs Hastalıkları Anabilim Dalı", "T": 9, "B": 7, "U": 2, "Y": 0}
    ]
    for b in birimler:
        with st.expander(f"📌 {b['Ad']} ({b['T']} Dosya)"):
            b1, b2, b3 = st.columns(3)
            b1.metric("Bireysel", b['B'])
            b2.metric("Uzmanlık", b['U'])
            b3.metric("Tez (Y.L/Doktora)", b['Y'])

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü")
    hocalar = [
        {"Ad": "Prof. Dr. Meltem Gülhan HALİL", "Birim": "İç Hastalıkları A.D.", "T": 6, "B": 4, "U": 2},
        {"Ad": "Prof. Dr. Yasemin ÖZSÜREKCİ", "Birim": "Çocuk Sağlığı A.D.", "T": 5, "B": 2, "U": 3},
        {"Ad": "Dr. Öğr. Üyesi Gonca ÖZTEN", "Birim": "Kadın Hastalıkları A.D.", "T": 4, "B": 4, "U": 0},
        {"Ad": "Doç. Dr. Süleyman Nahit ŞENDUR", "Birim": "İç Hastalıkları A.D.", "T": 4, "B": 3, "U": 1}
    ]
    for h in hocalar:
        with st.expander(f"👤 {h['Ad']} ({h['T']} Dosya)"):
            st.write(f"**Birim:** {h['Birim']}")
            h1, h2 = st.columns(2)
            h1.metric("Bireysel", h['B'])
            h2.metric("Uzmanlık", h['U'])

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
