import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="centered")

# CSS: Dark Navy Blue & Hacettepe Gold + Hata Giderilmiş Stil
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .block-container { max-width: 800px; padding-top: 1rem; }
    
    /* Metrik Kartları (Sabit) */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 1px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: center;
    }
    
    /* Expander ve Kart Tasarımı */
    .stExpander {
        background-color: #001d3d !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
        margin-bottom: 10px;
    }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    .status-text { font-weight: bold; color: #ffc300; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ (Excel ile Birebir) ---
toplam_basvuru = 190 #
kurul_sayisi = 4     #

# Birimler ve Karar Detayları
birim_verileri = [
    {"Birim": "İç Hastalıkları Anabilim Dalı", "Sayi": 27, "Bireysel": 20, "Uzmanlık": 7, "Onay": 18, "Düzeltme": 7, "KAEK": 2},
    {"Birim": "Çocuk Sağlığı ve Hastalıkları A.D.", "Sayi": 23, "Bireysel": 11, "Uzmanlık": 12, "Onay": 15, "Düzeltme": 6, "KAEK": 2},
    {"Birim": "Kadın Hastalıkları ve Doğum A.D.", "Sayi": 9, "Bireysel": 7, "Uzmanlık": 2, "Onay": 6, "Düzeltme": 3, "KAEK": 0},
    {"Birim": "Klinik Eczacılık Anabilim Dalı", "Sayi": 9, "Bireysel": 6, "Uzmanlık": 3, "Onay": 5, "Düzeltme": 4, "KAEK": 0},
    {"Birim": "Göğüs Hastalıkları Anabilim Dalı", "Sayi": 9, "Bireysel": 8, "Uzmanlık": 1, "Onay": 7, "Düzeltme": 2, "KAEK": 0}
]

# Sorumlu Hocalar ve Detaylar
sorumlu_verileri = [
    {"Sorumlu": "Prof. Dr. Meltem Gülhan HALİL", "Birim": "İç Hastalıkları A.D.", "Sayi": 6, "Bireysel": 4, "Uzmanlık": 2},
    {"Sorumlu": "Prof. Dr. Yasemin ÖZSÜREKCİ", "Birim": "Çocuk Sağlığı ve Hastalıkları A.D.", "Sayi": 5, "Bireysel": 2, "Uzmanlık": 3},
    {"Sorumlu": "Dr. Öğr. Üyesi Gonca ÖZTEN", "Birim": "Kadın Hastalıkları ve Doğum A.D.", "Sayi": 4, "Bireysel": 4, "Uzmanlık": 0},
    {"Sorumlu": "Doç. Dr. Süleyman Nahit ŞENDUR", "Birim": "İç Hastalıkları A.D.", "Sayi": 4, "Bireysel": 4, "Uzmanlık": 0},
    {"Sorumlu": "Prof. Dr. Ali Fuat KALYONCU", "Birim": "Göğüs Hastalıkları A.D.", "Sayi": 4, "Bireysel": 4, "Uzmanlık": 0}
]

# --- BAŞLIK VE ANA ÖZET (SABİT) ---
st.markdown("<h1 style='text-align: center; margin-bottom:0;'>🏛️ Hacettepe Üniversitesi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-top:0;'>SBA 2026 Karar Destek Sistemi</h3>", unsafe_allow_html=True)

# İstediğin Ana Özet Paneli - Her daim görünür
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", f"{toplam_basvuru}")
c2.metric("🗓️ Kurul Sayısı", f"{kurul_sayisi}")
st.write("---")

# --- SEKMELER ---
tab1, tab2, tab3 = st.tabs(["🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi", "👥 Raportörler"])

with tab1:
    st.write("#### 🏢 En Çok Başvuran İlk 5 Birim (Detaylı)")
    for b in birim_verileri:
        with st.expander(f"{b['Birim']} — {b['Sayi']} Dosya"):
            colA, colB = st.columns(2)
            with colA:
                st.markdown("**Nitelik Dağılımı:**")
                st.write(f"📝 Bireysel Araştırma: {b['Bireysel']}")
                st.write(f"🎓 Uzmanlık Tezi: {b['Uzmanlık']}")
            with colB:
                st.markdown("**Karar Durumu:**")
                st.write(f"✅ ONAY: {b['Onay']}")
                st.write(f"⚠️ DÜZELTME: {b['Düzeltme']}")
                st.write(f"🚫 KAEK: {b['KAEK']}")
            st.progress(b['Onay'] / b['Sayi'])

with tab2:
    st.write("#### 👨‍🏫 En Çok Başvuran İlk 5 Sorumlu (Detaylı)")
    for s in sorumlu_verileri:
        with st.expander(f"{s['Sorumlu']} — {s['Sayi']} Dosya"):
            st.markdown(f"**Bağlı Olduğu Birim:** <span class='status-text'>{s['Birim']}</span>", unsafe_allow_html=True)
            st.write(f"📄 Bireysel Araştırma: {s['Bireysel']}")
            st.write(f"🎓 Uzmanlık Tezi: {s['Uzmanlık']}")
            st.progress(s['Bireysel'] / s['Sayi'] if s['Sayi'] > 0 else 0)

with tab3:
    st.info("Raportör verileri sistemde kayıtlıdır. Kod içerisinden aktif edilebilir.")
    # Önceki kodlardaki raportör seçici buraya eklenebilir.

st.write("---")
st.markdown("<center style='color:#555;'>Hacettepe SBA Karar Destek Sistemi © 2026</center>", unsafe_allow_html=True)
