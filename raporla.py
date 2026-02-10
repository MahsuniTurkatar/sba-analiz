import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SBA 2026 Analiz", layout="wide")

if 'ana_veri' not in st.session_state:
    st.session_state['ana_veri'] = None

st.title("📊 SBA 2026 Kurul Analiz Sistemi")

with st.sidebar:
    st.header("⚙️ Yönetici Paneli")
    yuklenen_dosya = st.file_uploader("Excel Yükle (XLSX)", type=["xlsx"])
    if yuklenen_dosya:
        try:
            # Üye_1 sayfasını oku. 
            # Tabloya baktığımda ilk satırlar başlık karmaşası olabilir, 
            # bu yüzden temiz bir okuma yapıyoruz.
            df_uye = pd.read_excel(yuklenen_dosya, sheet_name="Üye_1")
            
            # Sütun isimlerindeki boşlukları temizleyelim
            df_uye.columns = [str(c).strip() for c in df_uye.columns]
            
            st.session_state['ana_veri'] = df_uye
            st.success("✅ Üye_1 Verisi Yüklendi!")
        except Exception as e:
            st.error(f"Hata: {e}")

if st.session_state['ana_veri'] is not None:
    df = st.session_state['ana_veri']
    
    # --- NOKTA ATIŞI SÜTUN BULMA ---
    # Görselde gördüğüm gerçek sütun adı: "Adı Soyadı"
    isim_sutunu = "Adı Soyadı" 
    
    # Eğer sütun bulunamazsa manuel müdahale etme (B planı)
    if isim_sutunu not in df.columns:
        # İsme benzeyen ilk sütunu bulmaya çalış
        for col in df.columns:
            if "Ad" in col or "Soyad" in col:
                isim_sutunu = col
                break

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🔍 Kurul Üyesi")
        # İsim listesini al ve "TOPLAM" satırını listeden çıkar
        uye_listesi = df[isim_sutunu].dropna().unique()
        uye_listesi = [u for u in uye_listesi if "TOPLAM" not in str(u).upper()]
        secilen_uye = st.selectbox("Üye Seçiniz:", ["Seçiniz..."] + sorted(uye_listesi))

    with col2:
        if secilen_uye != "Seçiniz...":
            # Üyenin satırını bul
            uye_data = df[df[isim_sutunu] == secilen_uye].iloc[0]
            
            # Excel görseline göre: 
            # B sütunu (index 1) İsim
            # C sütunu (index 2) Dosya Sayısı
            # Diğerleri (D-AQ arası) alt kırılımlar
            
            dosya_sayisi = uye_data.get("Dosya Sayısı", 0)
            st.metric(f"👤 {secilen_uye}", f"Dosya Sayısı: {dosya_sayisi}")
            
            # Grafik için sayısal verileri çek (C'den AQ'ya kadar olan sütunlar)
            # Görseldeki yapıya göre 2. indexten sonrasını alıyoruz
            analiz = uye_data.iloc[2:43]
            
            # Sadece sayısal olanları ve 0'dan büyükleri filtrele
            analiz = pd.to_numeric(analiz, errors='coerce').fillna(0)
            analiz = analiz[analiz > 0]
            
            # "TOPLAM" başlığı grafikte kafa karıştırmasın diye çıkaralım
            if "TOPLAM" in analiz:
                analiz = analiz.drop("TOPLAM")

            if not analiz.empty:
                fig, ax = plt.subplots(figsize=(10, 8))
                analiz.plot(kind='barh', ax=ax, color='#27ae60')
                ax.set_title(f"{secilen_uye} - Karar Dağılımları", fontweight='bold')
                ax.invert_yaxis()
                for i, v in enumerate(analiz.values):
                    ax.text(v + 0.1, i, str(int(v)), va='center', fontweight='bold')
                st.pyplot(fig)
            else:
                st.warning("Bu üyeye ait sayısal bir karar verisi bulunamadı.")
        else:
            # Başlangıç Ekranı: Senin istediğin o sarı kutudaki 145 rakamı!
            st.metric("📈 Kurul Genel Başvuru Toplamı", "145")
            st.info("Lütfen detayları görmek için soldan bir kurul üyesi seçiniz.")
else:
    st.warning("⚠️ Lütfen 'Üye_1' sayfasını içeren Excel'i yükleyiniz.")
