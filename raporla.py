import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx"

@st.cache_data
def load_all_data():
    try:
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", skiprows=1)
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot", skiprows=2)
        return df_g, df_r, df_p
    except Exception as e:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: FB TASARIMI ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
    }
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 95% !important; border-collapse: collapse; color: white; margin: auto; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 10px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. GÜNDEM SAYILARI ---
if df_gundem is not None:
    # Sayısal sütunları tam sayıya çevir
    target_cols = ['Başvuru', 'Düzeltme', 'Dilekçe', 'Toplam']
    for col in target_cols:
        if col in df_gundem.columns:
            df_gundem[col] = pd.to_numeric(df_gundem[col], errors='coerce').fillna(0).astype(int)
    
    # Boş olmayanları ve TOPLAM satırını süz
    df_g_final = df_gundem[(df_gundem['S.NO'].notna()) & (df_gundem['Gündem Tarihleri'].notna() | (df_gundem['S.NO'] == 'TOPLAM'))].copy()
    
    st.write("### 📅 2026 Gündem Sayıları")
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.markdown(df_g_final.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.write("#### 📋 Kurul Karar Çizelgesi")
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.info("ℹ️ Karar Çizelgesi görseli bekleniyor...")

with tab2:
    st.write("#### 👥 Raportör Detaylı Analizi")
    if df_raportor is not None:
        r_list = df_raportor["Adı Soyadı"].dropna().unique().tolist()
        sec_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = df_raportor[df_raportor["Adı Soyadı"] == sec_r].iloc[0]
        
        c1, c2, c3 = st.columns(3)
        # Sütunları isimle değil, yerinden buluyoruz (Hata payını silmek için)
        dosya_sayisi = int(r_row[2]) # Dosya Sayısı genelde 3. sütun (index 2)
        karar_toplam = int(r_row.iloc[-1]) # En son sütun her zaman Genel TOPLAM
        
        c1.metric("📌 Atanan Dosya", dosya_sayisi)
        c2.metric("✅ Karar Verilen", karar_toplam)
        c3.metric("⏳ Bekleyen", dosya_sayisi - karar_toplam)

with tab3:
    st.write("#### 🏢 Birim Analizi")
    if df_pivot is not None:
        # Pivot sayfasındaki Birim Analizi (A ve B sütunu)
        birim_ozet = df_pivot.iloc[:, [0, 1]].dropna().copy()
        birim_ozet.columns = ["Birim Adı", "Dosya Sayısı"]
        # Sayıyı tam sayı yap
        birim_ozet["Dosya Sayısı"] = birim_ozet["Dosya Sayısı"].astype(int)
        st.table(birim_ozet)

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Analizi")
    if df_pivot is not None:
        # Pivot sayfasındaki Sorumlu Analizi (D ve E sütunu - yani index 3 ve 4)
        sorumlu_ozet = df_pivot.iloc[:, [3, 4]].dropna().copy()
        sorumlu_ozet.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        sorumlu_ozet["Dosya Sayısı"] = sorumlu_ozet["Dosya Sayısı"].astype(int)
        st.table(sorumlu_ozet)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
