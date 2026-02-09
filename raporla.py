import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Sayfa ayarları
st.set_page_config(page_title="SBA 2026 Analiz", layout="centered")

st.title("🚀 SBA 2026 Analiz & Raporlama (Web)")
st.write("Excel dosyanızı yükleyin ve anında analiz edin.")

# Dosya Yükleme
yuklenen_dosya = st.file_uploader("Excel dosyasını buraya sürükleyin", type=["xlsx"])

if yuklenen_dosya:
    try:
        # Excel'i oku
        df = pd.read_excel(yuklenen_dosya, sheet_name="Başvuru")
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # Dashboard Özeti
        toplam = len(df)
        st.info(f"📊 Toplam Başvuru Sayısı: {toplam}")

        # Analiz Seçimi
        secilen = st.selectbox("Analiz Edilecek Kategori:", 
                              ["BİRİMİ", "SORUMLUSU", "TÜM RAPORTÖRLER (BİRLEŞİK)", "GÜNCEL DURUM"])

        # Veriyi Hazırla
        if secilen == "TÜM RAPORTÖRLER (BİRLEŞİK)":
            r1 = df['RAPORTÖR 1'].dropna().astype(str).str.strip()
            r2 = df['RAPORTÖR 2'].dropna().astype(str).str.strip()
            data = pd.concat([r1, r2])
            baslik = "Toplam Raportör İş Yükü (Birleşik)"
        else:
            data = df[secilen].dropna().astype(str).str.strip()
            baslik = f"{secilen} Dağılımı"

        ozet = data.value_counts().head(15)

        # Grafik Oluşturma (Gelişmiş Rakamlı Versiyon)
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(ozet.index, ozet.values, color='skyblue')
        ax.set_title(baslik, fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        
        # Rakamları Çubukların Ucuna Yazma
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                    f'{int(width)}', va='center', fontweight='bold')

        # Grafiği Web'de Göster
        st.pyplot(fig)

        st.success("Grafiğe sağ tıklayıp 'Resmi Farklı Kaydet' diyerek bilgisayarınıza alabilirsiniz.")

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")