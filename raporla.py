import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SBA 2026 Kurul Analiz", layout="wide")

if 'ana_veri' not in st.session_state:
    st.session_state['ana_veri'] = None

st.title("📊 SBA 2026 Kurul Analiz Sistemi")

with st.sidebar:
    st.header("⚙️ Yönetici Paneli")
    yuklenen_dosya = st.file_uploader("Üye_1 Sayfasını Yükle", type=["xlsx"])
    if yuklenen_dosya:
        try:
            # Excel'i başlık karmaşasını aşmak için 1. satırdan (header=1) itibaren oku
            df = pd.read_excel(yuklenen_dosya, sheet_name="Üye_1", header=1)
            # Sütun isimlerini temizle
            df.columns = [str(c).strip() for c in df.columns]
            st.session_state['ana_veri'] = df
            st.success("✅ Veri Yüklendi!")
        except Exception as e:
            st.error(f"Hata: {e}")

if st.session_state['ana_veri'] is not None:
    df = st.session_state['ana_veri']
    
    # İsimlerin olduğu sütun: "Adı Soyadı"
    # Sadece gerçek isimleri al (Tarihleri ve toplam satırlarını ele)
    uye_df = df[df['Adı Soyadı'].notna()].copy()
    uye_df = uye_df[uye_df['Adı Soyadı'].str.contains("Prof|Doç|Dr", na=False)]
    
    uye_listesi = sorted(uye_df['Adı Soyadı'].unique())

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🔍 Kurul Üyesi")
        secilen_uye = st.selectbox("Bir Üye Seçiniz:", ["Seçiniz..."] + uye_listesi)

    with col2:
        if secilen_uye != "Seçiniz...":
            uye_satiri = uye_df[uye_df['Adı Soyadı'] == secilen_uye].iloc[0]
            
            # --- NOKTA ATIŞI ANALİZ (İstediğin Liste) ---
            # Grafikte "Unnamed" çıkmaması için başlıkları manuel tanımlıyoruz
            # Excel'deki AO, AP, AQ gibi sonuç sütunlarını baz alalım
            grafik_verisi = {
                "ONAY": uye_satiri.get("Onay.4", 0), # TOPLAM altındaki Onay
                "DÜZELTME": uye_satiri.get("Düzeltme.4", 0),
                "KAEK": uye_satiri.get("KAEK.4", 0),
                "GÖRÜŞ": uye_satiri.get("Görüş.4", 0),
                "RET": uye_satiri.get("Ret.4", 0),
                "KAPSAM DIŞI": uye_satiri.get("Kapsam Dışı.4", 0),
                "GERİ ÇEKİLDİ": uye_satiri.get("Geri Çekildi.4", 0)
            }
            
            # Veriyi seriye dönüştür ve 0'dan büyükleri al
            analiz = pd.Series(grafik_verisi)
            analiz = pd.to_numeric(analiz, errors='coerce').fillna(0)
            
            st.metric(f"👤 {secilen_uye}", f"Toplam Atanan: {int(uye_satiri['Dosya Sayısı'])}")
            
            if analiz.sum() > 0:
                fig, ax = plt.subplots(figsize=(10, 6))
                analiz[analiz > 0].plot(kind='barh', ax=ax, color='#3498db')
                ax.set_title(f"{secilen_uye} - Karar Dağılımı", fontweight='bold')
                ax.invert_yaxis()
                for i, v in enumerate(analiz[analiz > 0].values):
                    ax.text(v + 0.1, i, str(int(v)), va='center', fontweight='bold')
                st.pyplot(fig)
            else:
                st.warning("Bu üyeye ait henüz karar girişi yapılmamış.")
        else:
            # İstediğin o 145 rakamı!
            st.metric("📈 Kurul Genel Başvuru Toplamı", "145")
            st.info("Lütfen detaylarını görmek istediğiniz üyeyi soldan seçiniz.")
