import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: KURUMSAL TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center !important;
    }
    /* Nitelik Kutuları */
    .nitelik-container { display: flex; justify-content: space-between; gap: 10px; margin: 20px 0; }
    .nitelik-card {
        flex: 1; background-color: #001d3d; border: 1px solid #ffc300;
        border-radius: 8px; padding: 15px; text-align: center;
    }
    .n-val { color: #ffc300; font-size: 1.5rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.9rem; }
    
    /* Tablo Tasarımı */
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 80% !important; border-collapse: collapse; color: white; }
    .styled-table th { background-color: #001d3d; color: #ffc300; border: 1px solid #ffc300; padding: 10px; }
    .styled-table td { border: 1px solid #ffc300; padding: 8px; text-align: center !important; }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    .footer { text-align: center; color: #ffc300; padding: 20px; border-top: 1px solid #ffc300; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ ---

# 1. Gündem Verisi
df_gundem = pd.DataFrame({
    "S.NO": ["1.", "2.", "3.", "4.", "TOPLAM"],
    "Gündem Tarihleri": ["06.01.2026", "20.01.2026", "04.02.2026", "17.02.2026", "-"],
    "Başvuru": [55, 45, 45, 45, 190],
    "Düzeltme": [16, 13, 12, 17, 58],
    "Dilekçe": [9, 11, 15, 7, 42],
    "Toplam": [80, 69, 72, 69, 290]
})

# 2. Raportör Analizi (7 Karar Kalemi)
raportor_data = {
    "Adı Soyadı": ["Prof. Dr. Ayşe Nurten AKARSU", "Prof. Dr. M. Özgür UYANIK", "Prof. Dr. Melih Önder BABAOĞLU", "Prof. Dr. Ayşe KİN İŞLER", "Prof. Dr. Yavuz AYHAN", "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY", "Prof. Dr. Gözde GİRGİN", "Doç. Dr. Kübra AYKAÇ", "Doç. Dr. Tolga ÇAKMAK", "Doç. Dr. Burcu ERSÖZ ALAN", "Doç. Dr. Ekim GÜMELER", "Dr. Öğr. Üyesi Müge DEMİR"],
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

# --- ÜST PANEL ---
st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

m_a, m_b = st.columns(2)
m_a.metric("📌 Toplam Başvuru", "190")
m_b.metric("🗓️ Kurul Sayısı", "4")

# Nitelikler (Geri Geldi)
st.markdown("""
    <div class="nitelik-container">
        <div class="nitelik-card"><span class="n-val">128</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">48</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">10</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">4</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

st.write("### 📅 2026 Gündem Sayıları")
st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.markdown(df_gundem.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER ---
t1, t2, t3, t4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with t1:
    st.write("#### 📋 Kurul Üye_1 Genel Karar Çizelgesi")
    # PNG Dosyası (Geri Geldi)
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info("Kurul Karar Çizelgesi (PNG) sisteme yükleniyor...")

with t2:
    st.write("#### 👥 Raportör Detaylı Karar Dağılımı")
    sec_r = st.selectbox("Raportör Seçiniz:", df_r["Adı Soyadı"].tolist())
    r = df_r[df_r["Adı Soyadı"] == sec_r].iloc[0]
    
    # Görsel detay tasarımı
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Dosya", r["Dosya"])
    c2.metric("Karar Verilen", int(r["Onay"] + r["Düzeltme"] + r["Ret"]))
    c3.metric("Fark (İşlemde)", int(r["Dosya"] - (r["Onay"] + r["Düzeltme"] + r["Ret"])))
    
    st.markdown(f"""
    <div style="background-color:#001d3d; border:1px solid #ffc300; border-radius:10px; padding:20px; text-align:center;">
        <span style="color:#ffc300; font-size:1.1rem;">✅ <b>ONAY:</b> {r['Onay']}</span> | 
        <span style="color:#ffc300; font-size:1.1rem;">⚠️ <b>DÜZELTME:</b> {r['Düzeltme']}</span> | 
        <span style="color:#ffc300; font-size:1.1rem;">📂 <b>KAEK:</b> {r['KAEK']}</span> | 
        <span style="color:#ffc300; font-size:1.1rem;">📝 <b>GÖRÜŞ:</b> {r['Görüş']}</span> <br><br>
        <span style="color:#ffc300; font-size:1.1rem;">❌ <b>RET:</b> {r['Ret']}</span> | 
        <span style="color:#ffc300; font-size:1.1rem;">🚫 <b>KAPSAM DIŞI:</b> {r['Kapsam Dışı']}</span> | 
        <span style="color:#ffc300; font-size:1.1rem;">🔄 <b>GERİ ÇEKİLDİ:</b> {r['Geri Çekildi']}</span>
    </div>
    """, unsafe_allow_html=True)

with t3:
    st.write("#### 🏢 En Çok Başvuru Yapan İlk 5 Birim (Detaylı Dağılım)")
    birimler = [
        {"Ad": "İç Hastalıkları Anabilim Dalı", "S": 27, "B": 18, "U": 6, "Y": 3},
        {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "S": 23, "B": 12, "U": 9, "Y": 2},
        {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "S": 9, "B": 6, "U": 3, "Y": 0},
        {"Ad": "Klinik Eczacılık Anabilim Dalı", "S": 9, "B": 4, "U": 4, "Y": 1},
        {"Ad": "Göğüs Hastalıkları Anabilim Dalı", "S": 9, "B": 7, "U": 2, "Y": 0}
    ]
    for b in birimler:
        with st.expander(f"📌 {b['Ad']} (Toplam: {b['S']} Dosya)"):
            ca, cb, cc = st.columns(3)
            ca.metric("Bireysel", b['B'])
            cb.metric("Uzmanlık", b['U'])
            cc.metric("Y. Lisans/Doktora", b['Y'])
            st.write(f"📈 **Kurul Genelindeki Payı:** %{round((b['S']/190)*100, 1)}")

with t4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Portföyü (İlk 5)")
    sorumlular = [
        {"H": "Prof. Dr. Meltem Gülhan HALİL", "Birim": "İç Hastalıkları A.D.", "B": 4, "U": 2, "T": 6},
        {"H": "Prof. Dr. Yasemin ÖZSÜREKCİ", "Birim": "Çocuk Sağlığı A.D.", "B": 2, "U": 3, "T": 5},
        {"H": "Dr. Öğr. Üyesi Gonca ÖZTEN", "Birim": "Kadın Hastalıkları ve Doğum A.D.", "B": 4, "U": 0, "T": 4},
        {"H": "Doç. Dr. Süleyman Nahit ŞENDUR", "Birim": "İç Hastalıkları A.D.", "B": 3, "U": 1, "T": 4},
        {"H": "Prof. Dr. Ali Fuat KALYONCU", "Birim": "Göğüs Hastalıkları A.D.", "B": 4, "U": 0, "T": 4}
    ]
    for s in sorumlular:
        with st.expander(f"👤 {s['H']} ({s['T']} Dosya)"):
            st.markdown(f"**🏢 Birim:** {s['Birim']}")
            colx, coly = st.columns(2)
            colx.metric("Bireysel Araştırma", s['B'])
            coly.metric("Uzmanlık Tezi", s['U'])

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
