import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sayfa ayarlarını yapalım
st.set_page_config(page_title="SBA 2026 Analiz Portalı", layout="wide")

# --- VERİ HAFIZASI ---
# Veriyi oturum süresince akılda tutmak için session_state kullanıyoruz
if 'ana_veri' not in st.session_state:
    st.session_state['ana_veri'] = None

st.title("📊 SBA 2026 Analiz Sistemi")

# --- YÖNETİCİ PANELİ (SOL TARAF) ---
with st.sidebar:
    st.header("⚙️ Yönetici Paneli")
    st.write("Excel dosyanızı buradan yükleyerek sistemi güncelleyebilirsiniz.")
    yuklenen_dosya = st.file_uploader("Dosya Seç (XLSX)", type=["xlsx"])
    
    if yuklenen_dosya:
        # Excel'i oku (Sayfa adı 'Başvuru' olarak varsayıldı)
        df = pd.read_excel(yuklenen_dosya, sheet_name="Başvuru")
        # Sütun isimlerini standart hale getirelim (Boşlukları sil, BÜYÜK HARF yap)
        df.columns = [str(c).strip().upper() for c in df.columns]
        st.session_state['ana_veri'] = df
        st.success("✅ Veri başarıyla yüklendi ve analiz edildi!")

# --- ANA EKRAN ANALİZLERİ ---
if st.session_state['ana_veri'] is not None:
    df = st.session_state['ana_veri']
    
    # Filtre sütunları
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🔍 Filtreler")
        # İstediğin sadeleşmiş menü isimleri
        kategori = st
