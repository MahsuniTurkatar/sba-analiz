import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SBA 2026 Analiz", layout="wide")

if 'ana_veri' not in st.session_state:
    st.session_state['ana_veri'] = None

st.title("📊 SBA 2026 Kurul Analiz Sistemi")

# --- SOL PANEL ---
with st.sidebar:
    st.header("⚙️ Yönetici Paneli")
    yuklenen_dosya = st.file_uploader("Excel Yükle (XLSX)", type=["xlsx"])
    if yuklenen_dosya:
        try:
            # "Üye_1" sayfasını oku
            df_uye = pd.read_excel(yuklenen_dosya, sheet_name="Üye_1")
            # Sütun isimlerini temizle (Başındaki/sonundaki boşlukları sil)
            df_uye.columns = [str(c).strip() for c in df_uye.columns]
            st.session_state['ana_veri'] = df_uye
            st.success("✅ Üye_1 Verisi Yüklendi!")
        except Exception as e:
            st.error(f"Sayfa Okuma Hatası: {e}. Lütfen sayfa adının 'Üye_1' olduğundan emin olun.")

# --- ANA EKRAN ---
if st.session_state['ana_veri'] is not None:
    df = st.session_state['ana_veri']
    
    # --- AKILLI SÜTUN BULUCU ---
    # İsimlerin olduğu sütunu otomatik bulmaya çalışalım
    olasi_isimler = ['AD-SOYAD', 'AD SOYAD', 'ADI SOYADI', 'AD_SOYAD', 'ÜYE ADI']
    isim_sutunu = None
    
    for olasi in olasi_isimler:
        if olasi in df.columns:
            isim_sutunu = olasi
            break
    
    # Eğer yukarıdakilerden hiçbiri yoksa, ilk sütunu isim sütunu kabul et
    if not isim_sutunu:
        isim_sutunu = df.columns[1] # Genellikle B sütunu (index 1) isimdir

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🔍 Kurul Üyesi")
        uye_listesi = sorted(df[isim_sutunu].dropna().unique())
        secilen_uye = st.selectbox("Üye Seçiniz:", ["Seçiniz..."] + uye_listesi)

    with col2:
        if secilen_uye != "Seçiniz...":
            # Seçilen üyenin satırını bul
            uye_satiri = df[df[isim_sutunu] == secilen_uye].iloc[0]
            
            # C (index 2) ile AQ (index 43) arasını alıyoruz.
            # Sayısal verileri çek ve başlıklarıyla eşleştir
            analiz_verisi = uye_satiri.iloc[2:43] 
            
            # Sadece sayısal ve 0'dan büyük verileri al
            analiz_verisi = pd.to_numeric(analiz_verisi, errors='coerce').fillna(0)
            analiz_verisi = analiz_verisi[analiz_verisi > 0]
            
            # Toplamı hesapla
            toplam_is = int(analiz_verisi.sum())
            
            st.metric(f"👤 {secilen_uye}", f"Toplam {toplam_is} Karar / Görev")
            
            if not analiz_verisi.empty:
                fig, ax = plt.subplots(figsize=(10, 8))
                analiz_verisi.plot(kind='barh', ax=ax, color='#2ecc71')
                ax.set_title(f"{secilen_uye} - Detaylı Analiz (C-AQ Arası)", fontweight='bold')
                ax.invert_yaxis()
                # Sayıları barların üzerine yaz
                for i, v in enumerate(analiz_verisi.values):
                    ax.text(v + 0.1, i, str(int(v)), va='center', fontweight='bold')
                st.pyplot(fig)
            else:
                st.warning("Bu üyeye ait sayısal bir veri bulunamadı.")
        else:
            # Başlangıç ekranı metrikleri
            st.metric("📈 Toplam Başvuru", "145")
            st.info("Detayları görmek için soldan bir kurul üyesi seçiniz.")
else:
    st.warning("⚠️ Lütfen 'Üye_1' sayfasını içeren Excel'i sol taraftan yükleyiniz.")
