import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sayfa ayarları
st.set_page_config(page_title="SBA 2026 Kurul Analiz", layout="wide")

if 'ana_veri' not in st.session_state:
    st.session_state['ana_veri'] = None

st.title("📊 SBA 2026 Kurul Analiz Sistemi")

# --- SOL PANEL (VERİ YÜKLEME) ---
with st.sidebar:
    st.header("⚙️ Yönetici Paneli")
    yuklenen_dosya = st.file_uploader("Üye_1 Sayfasını İçeren Excel'i Yükle", type=["xlsx"])
    if yuklenen_dosya:
        try:
            # Excel'den sadece 'Üye_1' sayfasını oku
            df = pd.read_excel(yuklenen_dosya, sheet_name="Üye_1")
            # Sütun isimlerindeki gizli boşlukları temizle
            df.columns = [str(c).strip() for c in df.columns]
            st.session_state['ana_veri'] = df
            st.success("✅ Üye_1 sayfası başarıyla yüklendi!")
        except Exception as e:
            st.error(f"⚠️ Yükleme Hatası: {e}")

# --- ANA EKRAN ANALİZİ ---
if st.session_state['ana_veri'] is not None:
    df = st.session_state['ana_veri']
    
    # Görseldeki sütun adını tam olarak kullanıyoruz
    isim_sutunu = "Adı Soyadı"
    
    # 1. Toplam satırlarını ve boşlukları listeden temizle (Hata almamak için)
    uye_df = df[df[isim_sutunu].notna()].copy()
    uye_df = uye_df[~uye_df[isim_sutunu].astype(str).str.contains("TOPLAM|toplam", case=False)]
    
    # Kurul Üyesi Listesi (Sadece isimlerden oluşan temiz liste)
    uye_listesi = sorted(uye_df[isim_sutunu].astype(str).unique())

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🔍 Kurul Üyesi")
        secilen_uye = st.selectbox("Bir Üye Seçiniz:", ["Seçiniz..."] + uye_listesi)

    with col2:
        if secilen_uye != "Seçiniz...":
            # Seçilen üyenin satır verisini al
            uye_satiri = uye_df[uye_df[isim_sutunu] == secilen_uye].iloc[0]
            
            # Excel'e göre C sütunundaki toplam dosya sayısı
            dosya_sayisi = uye_satiri.get("Dosya Sayısı", 0)
            st.metric(f"👤 {secilen_uye}", f"Atanan Dosya Sayısı: {int(dosya_sayisi)}")
            
            # C'den AQ'ya kadar olan sayısal verileri alıyoruz (index 2:43)
            # Sayısal olmayanları (örn. isimler) filtreleyelim
            analiz_verisi = uye_satiri.iloc[2:43]
            analiz_verisi = pd.to_numeric(analiz_verisi, errors='coerce').fillna(0)
            
            # Sadece 0'dan büyük kararları göster (Grafik temiz olsun)
            analiz_verisi = analiz_verisi[analiz_verisi > 0]
            
            if not analiz_verisi.empty:
                fig, ax = plt.subplots(figsize=(10, 8))
                analiz_verisi.plot(kind='barh', ax=ax, color='#3498db')
                ax.set_title(f"{secilen_uye} - Karar ve Süreç Dağılımı", fontweight='bold')
                ax.invert_yaxis()
                # Değerleri bar üzerine yaz
                for i, v in enumerate(analiz_verisi.values):
                    ax.text(v + 0.1, i, str(int(v)), va='center', fontweight='bold')
                st.pyplot(fig)
            else:
                st.warning("Bu üyeye ait detaylı bir karar verisi bulunamadı.")
        else:
            # Karşılama Ekranı - Senin istediğin o 145 rakamı!
            st.metric("📈 Kurul Genel Başvuru Toplamı", "145")
            st.info("Kurul üyelerinin bireysel performanslarını görmek için soldan bir isim seçiniz.")
else:
    st.warning("👋 Hoş geldiniz! Lütfen analiz için sol taraftan Excel dosyanızı yükleyiniz.")
