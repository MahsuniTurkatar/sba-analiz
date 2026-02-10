import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SBA 2026 Dashboard", layout="wide")

# --- VERİ YÖNETİMİ ---
# Bu kısım veriyi tarayıcı hafızasında tutar. 
if 'ana_veri' not in st.session_state:
    st.session_state['ana_veri'] = None

st.title("📊 SBA 2026 Analiz Sistemi")

# Sadece senin göreceğin yükleme alanı (Yükledikten sonra kapatabilirsin)
with st.sidebar:
    st.header("⚙️ Yönetici Paneli")
    yuklenen = st.file_uploader("Veriyi Güncelle (Sadece Yönetici)", type=["xlsx"])
    if yuklenen:
        df = pd.read_excel(yuklenen, sheet_name="Başvuru")
        df.columns = [str(c).strip().upper() for c in df.columns]
        st.session_state['ana_veri'] = df
        st.success("Veri başarıyla güncellendi!")

# --- ANA EKRAN ---
if st.session_state['ana_veri'] is not None:
    df = st.session_state['ana_veri']
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🔍 Filtreler")
        kategori = st.selectbox("Genel Analiz:", ["BİRİM", "SORUMLU", "RAPORTÖRLER", "GÜNCEL DURUM"])
        
        st.divider()
        
        # Raportör bazlı özel arama
        r_liste = sorted(list(set(df['RAPORTÖR 1'].dropna().unique()) | set(df['RAPORTÖR 2'].dropna().unique())))
        secilen_raportor = st.selectbox("👤 Raportör Özel Bakış:", ["Seçiniz..."] + r_liste)

    with col2:
        if secilen_raportor != "Seçiniz...":
            # Kişiye özel analiz
            kisi_verisi = df[(df['RAPORTÖR 1'] == secilen_raportor) | (df['RAPORTÖR 2'] == secilen_raportor)]
            st.info(f"📌 {secilen_raportor}: Toplam {len(kisi_verisi)} dosyada görevli.")
            ozet = kisi_verisi['GÜNCEL DURUM'].value_counts()
            baslik = f"{secilen_raportor} - İş Durumu"
        else:
            # Genel analizler
            if kategori == "RAPORTÖRLER":
                data = pd.concat([df['RAPORTÖR 1'], df['RAPORTÖR 2']]).dropna()
            elif kategori == "BİRİM":
                data = df['BİRİMİ'].dropna()
            elif kategori == "SORUMLU":
                data = df['SORUMLUSU'].dropna()
            else:
                data = df['GÜNCEL DURUM'].dropna()
            
            ozet = data.value_counts().head(15)
            baslik = f"{kategori} Dağılımı"

        # Grafik Çizimi
        fig, ax = plt.subplots(figsize=(10, 6))
        ozet.plot(kind='barh', ax=ax, color='skyblue')
        ax.set_title(baslik)
        ax.invert_yaxis()
        for i, v in enumerate(ozet.values):
            ax.text(v + 0.1, i, str(v), va='center', fontweight='bold')
        st.pyplot(fig)

else:
    st.warning("⚠️ Sistemde yüklü veri bulunmamaktadır. Lütfen sol taraftan Excel yükleyiniz.")
