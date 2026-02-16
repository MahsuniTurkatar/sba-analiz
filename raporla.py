import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
    }
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 75% !important; border-collapse: collapse; color: white; }
    .styled-table th, .styled-table td { border: 1px solid #ffc300; padding: 8px; text-align: center !important; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    .footer { text-align: center; color: #ffc300; padding: 20px; border-top: 1px solid #ffc300; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ ---
# Gündem Tablosu
df_gundem = pd.DataFrame({
    "S.NO": ["1.", "2.", "3.", "4.", "TOPLAM"],
    "Gündem Tarihleri": ["06.01.2026", "20.01.2026", "04.02.2026", "17.02.2026", "-"],
    "Başvuru": [55, 45, 45, 45, 190],
    "Düzeltme": [16, 13, 12, 17, 58],
    "Dilekçe": [9, 11, 15, 7, 42],
    "Toplam": [80, 69, 72, 69, 290]
})

# Raportör Analizi (TAM LİSTE - 7 KALEM)
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
df_raportor = pd.DataFrame(raportor_data)

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
col1.metric("📌 Toplam Başvuru", "190")
col2.metric("🗓️ Kurul Sayısı", "4")

st.write("### 📅 2026 Gündem Sayıları")
st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.markdown(df_gundem.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi (5 Adet)", "👨‍🏫 Sorumlu Analizi (5 Adet)"])

# ... (tab1 ve tab2 bölümleri öncekiyle aynı, raportörde tüm 7 kalem var) ...

with tab2:
    st.write("#### 🔍 Raportör Detaylı Karar Takibi")
    sec_r = st.selectbox("Raportör Seçiniz:", df_raportor["Adı Soyadı"].tolist())
    r = df_raportor[df_raportor["Adı Soyadı"] == sec_r].iloc[0]
    st.markdown(f"""
    <div style="background-color:#001d3d; border:1px solid #ffc300; border-radius:10px; padding:15px;">
        ✅ <b>ONAY:</b> {r['Onay']} | ⚠️ <b>DÜZELTME:</b> {r['Düzeltme']} | 📂 <b>KAEK:</b> {r['KAEK']} | 📝 <b>GÖRÜŞ:</b> {r['Görüş']} <br>
        ❌ <b>RET:</b> {r['Ret']} | 🚫 <b>KAPSAM DIŞI:</b> {r['Kapsam Dışı']} | 🔄 <b>GERİ ÇEKİLDİ:</b> {r['Geri Çekildi']}
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.write("#### 🏢 En Çok Başvuru Yapan İlk 5 Birim (Detaylı Dağılım)")
    # Detaylı birim verisi
    birim_detay = [
        {"Ad": "İç Hastalıkları Anabilim Dalı", "S": 27, "B": 18, "U": 6, "Y": 3},
        {"Ad": "Çocuk Sağlığı ve Hastalıkları A.D.", "S": 23, "B": 12, "U": 9, "Y": 2},
        {"Ad": "Kadın Hastalıkları ve Doğum A.D.", "S": 9, "B": 6, "U": 3, "Y": 0},
        {"Ad": "Klinik Eczacılık Anabilim Dalı", "S": 9, "B": 4, "U": 4, "Y": 1},
        {"Ad": "Göğüs Hastalıkları Anabilim Dalı", "S": 9, "B": 7, "U": 2, "Y": 0}
    ]
    
    for b in birim_detay:
        with st.expander(f"📌 {b['Ad']} (Toplam: {b['S']} Dosya)"):
            c_a, c_b, c_c = st.columns(3)
            c_a.metric("Bireysel", b['B'])
            c_b.metric("Uzmanlık", b['U'])
            c_c.metric("Y. Lisans/Doktora", b['Y'])
            st.write(f"📈 **Kurul Genelindeki Payı:** %{round((b['S']/190)*100, 1)}")

with tab4:
    st.write("#### 👨‍🏫 En Çok Başvuru Yapan İlk 5 Sorumlu")
    sorumlular = [
        {"H": "Prof. Dr. Meltem Gülhan HALİL", "B": 4, "U": 2, "T": 6},
        {"H": "Prof. Dr. Yasemin ÖZSÜREKCİ", "B": 2, "U": 3, "T": 5},
        {"H": "Dr. Öğr. Üyesi Gonca ÖZTEN", "B": 4, "U": 0, "T": 4},
        {"H": "Doç. Dr. Süleyman Nahit ŞENDUR", "B": 3, "U": 1, "T": 4},
        {"H": "Prof. Dr. Ali Fuat KALYONCU", "B": 4, "U": 0, "T": 4}
    ]
    for s in sorumlular:
        with st.expander(f"{s['H']} (Toplam: {s['T']} Dosya)"):
            st.write(f"📊 Bireysel: {s['B']} | 🎓 Uzmanlık: {s['U']}")

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
