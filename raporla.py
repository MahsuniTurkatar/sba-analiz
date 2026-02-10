import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sayfa Genişliği
st.set_page_config(page_title="SBA 2026 Analiz", layout="wide")

# Veri Hafızası Kontrolü
if 'ana_veri' not in st.session_state:
    st.session_state['ana_veri'] = None

st.title("📊 SBA 2026 Analiz Sistemi")

# --- SOL PANEL (YÖNETİCİ) ---
with st.sidebar:
    st.header("⚙️ Yönetici Paneli")
    yuklenen_dosya = st.file_uploader("Excel Yükle (XLSX)", type=["xlsx"])
    if yuklenen_dosya:
        try:
            df = pd.read_excel(yuklenen_dosya, sheet_name="Başvuru")
            df.columns = [str(c).strip().upper() for c in df.columns]
            st.session_state['ana_veri'] = df
            st.success("✅ Veri Yüklendi!")
        except Exception as e:
            st.error(f"Hata: {e}")

# --- ANA EKRAN ---
if st.session_state['ana_veri'] is not None:
    df = st.session_state['ana_veri']
    
    # Üst Bilgi Kartları
    c1, c2 = st.columns(2)
    with c1:
        st.metric("📈 Toplam Başvuru", len(df))
    with c2:
        onay_sayisi = len(df[df['GÜNCEL DURUM'] == 'ONAY']) if 'GÜNCEL DURUM' in df.columns else 0
        st.metric("✅ Toplam Onay", onay_sayisi)

    st.divider()

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🔍 Filtreler")
        kategori = st.selectbox("Genel Analiz:", ["BİRİM", "SORUMLU", "RAPORTÖRLER", "GÜNCEL DURUM"])
        
        # Raportör Listesi
        r1 = df['RAPORTÖR 1'].dropna().unique() if 'RAPORTÖR 1' in df.columns else []
        r2 = df['RAPORTÖR 2'].dropna().unique() if 'RAPORTÖR 2' in df.columns else []
        r_liste = sorted(list(set(r1) | set(r2)))
        secilen_raportor = st.selectbox("👤 Raportör Seç:", ["Seçiniz..."] + r_liste)

    with col2:
        if secilen_raportor != "Seçiniz...":
            # Raportör Filtresi
            kisi_verisi = df[(df['RAPORTÖR 1'] == secilen_raportor) | (df['RAPORTÖR 2'] == secilen_raportor)]
            st.info(f"📂 **{secilen_raportor}** için toplam **{len(kisi_verisi)}** dosya bulundu.")
            plot_data = kisi_verisi['GÜNCEL DURUM'].value_counts()
            baslik = f"{secilen_raportor} - İş Durumu"
        else:
            # Genel Filtreler
            if kategori == "RAPORTÖRLER":
                plot_data = pd.concat([df['RAPORTÖR 1'], df['RAPORTÖR 2']]).dropna().value_counts().head(20)
            elif kategori == "BİRİM":
                plot_data = df['BİRİMİ'].dropna().value_counts().head(20)
            elif kategori == "SORUMLU":
                plot_data = df['SORUMLUSU'].dropna().value_counts().head(20)
            else:
                plot_data = df['GÜNCEL DURUM'].dropna().value_counts()
            baslik = f"{kategori} Dağılımı"

        # Grafik
        if not plot_data.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_data.plot(kind='barh', ax=ax, color='#3498db')
            ax.set_title(baslik, fontweight='bold')
            ax.invert_yaxis()
            for i, v in enumerate(plot_data.values):
                ax.text(v + 0.1, i, str(v), va='center', fontweight='bold')
            st.pyplot(fig)
else:
    st.warning("⚠️ Lütfen sol panelden Excel yükleyiniz.")
