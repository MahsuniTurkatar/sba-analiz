import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME (HATASIZ VE NET) ---
EXCEL_FILE = "2026_SBA.xlsx"

@st.cache_data
def load_all_data():
    try:
        # 1. Gündem Sayıları (Sayılar sekmesi)
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        
        # 2. Raportör Analizi (Üye_1 sekmesi)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", skiprows=1)
        
        # 3. Birim ve Sorumlu (Pivot sekmesi)
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot", skiprows=2)
        
        return df_g, df_r, df_p
    except Exception as e:
        st.error(f"Excel'e ulaşılamadı: {e}")
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: FB TASARIMI (ASLA BOZULMAZ) ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
    }
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 90% !important; border-collapse: collapse; color: white; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 10px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. GÜNDEM SAYILARI (45.0 DÜZELTİLDİ) ---
st.write("### 📅 2026 Gündem Sayıları")
if df_gundem is not None:
    # Sayıları temizle: NaN'ları 0 yap ve Tam Sayı (Integer) yap
    for col in ['Başvuru', 'Düzeltme', 'Dilekçe', 'Toplam']:
        if col in df_gundem.columns:
            df_gundem[col] = pd.to_numeric(df_gundem[col], errors='coerce').fillna(0).astype(int)
    
    # Sadece S.NO dolu olanları ve "TOPLAM" satırını al
    # Boş tarihler ve 0 olan gereksiz satırları eliyoruz
    df_g_clean = df_gundem[((df_gundem['Toplam'] > 0) | (df_gundem['S.NO'] == "TOPLAM"))].copy()
    
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.markdown(df_g_clean.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.write("#### 📋 Kurul Karar Çizelgesi")
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info("Kurul Karar Çizelgesi görseli aranıyor...")

with tab2:
    st.write("#### 👥 Raportör Detaylı Analizi")
    if df_raportor is not None:
        r_list = df_raportor["Adı Soyadı"].dropna().unique().tolist()
        sec_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = df_raportor[df_raportor["Adı Soyadı"] == sec_r].iloc[0]
        
        c1, c2, c3 = st.columns(3)
        dosya_sayisi = int(r_row["Dosya Sayısı"])
        # Üye_1 sayfasındaki en sondaki "TOPLAM" (Karar verilenlerin toplamı)
        karar_toplam = int(r_row.iloc[-1]) 
        
        c1.metric("📌 Atanan Dosya", dosya_sayisi)
        c2.metric("✅ Karar Verilen", karar_toplam)
        c3.metric("⏳ Bekleyen", dosya_sayisi - karar_toplam)

with tab3:
    st.write("#### 🏢 Birim Analizi")
    if df_pivot is not None:
        # Pivot sayfasındaki ilk iki sütun: Birim ve Sayısı
        birim_ozet = df_pivot.iloc[:, [0, 1]].dropna()
        birim_ozet.columns = ["Birim Adı", "Dosya Sayısı"]
        st.dataframe(birim_ozet, use_container_width=True, hide_index=True)

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Analizi")
    if df_pivot is not None:
        # Pivot sayfasındaki 4. ve 5. sütunlar: Sorumlu ve Sayısı
        sorumlu_ozet = df_pivot.iloc[:, [3, 4]].dropna()
        sorumlu_ozet.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        st.dataframe(sorumlu_ozet, use_container_width=True, hide_index=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
