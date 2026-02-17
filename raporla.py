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
    except:
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
    .nitelik-container { display: flex; justify-content: space-between; gap: 10px; margin: 20px 0; }
    .nitelik-card {
        flex: 1; background-color: #001d3d; border: 1px solid #FEDD00;
        border-radius: 8px; padding: 15px; text-align: center;
    }
    .n-val { color: #FEDD00; font-size: 1.5rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.9rem; }
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 100% !important; border-collapse: collapse; color: white; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 10px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. İSKELET: ÜST METRİKLER (GERİ GELDİ) ---
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# --- 2. İSKELET: NİTELİK KARTLARI (GERİ GELDİ) ---
st.markdown("""
    <div class="nitelik-container">
        <div class="nitelik-card"><span class="n-val">128</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">48</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">10</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">4</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 3. GÜNDEM SAYILARI (45.0 DÜZELTİLDİ) ---
if df_gundem is not None:
    for col in ['Başvuru', 'Düzeltme', 'Dilekçe', 'Toplam']:
        if col in df_gundem.columns:
            df_gundem[col] = pd.to_numeric(df_gundem[col], errors='coerce').fillna(0).astype(int)
    
    # Sadece S.NO dolu olanları ve TOPLAM satırını göster
    df_g_filtered = df_gundem[df_gundem['S.NO'].notna()].copy()
    # 0 olan boş satırları (5-23 arası) temizle ama TOPLAM'ı tut
    df_g_final = df_g_filtered[(df_g_filtered['Toplam'] > 0) | (df_g_filtered['S.NO'] == 'TOPLAM')]
    
    st.write("### 📅 2026 Gündem Sayıları")
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.markdown(df_g_final.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SEKMELER VE ANALİZLER ---
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
        
        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("📌 Atanan Dosya", int(r_row["Dosya Sayısı"]))
        rc2.metric("✅ Karar Verilen", int(r_row.iloc[-1])) 
        rc3.metric("⏳ Bekleyen", int(r_row["Dosya Sayısı"] - r_row.iloc[-1]))

with tab3:
    st.write("#### 🏢 Birim Analizi")
    if df_pivot is not None:
        # Pivot sayfasındaki Birim Sütunları (A ve B)
        birim_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        birim_df.columns = ["Birim Adı", "Dosya Sayısı"]
        birim_df["Dosya Sayısı"] = birim_df["Dosya Sayısı"].astype(int)
        st.table(birim_df)

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Analizi")
    if df_pivot is not None:
        # Pivot sayfasındaki Sorumlu Sütunları (D ve E)
        sorumlu_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        sorumlu_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        sorumlu_df["Dosya Sayısı"] = sorumlu_df["Dosya Sayısı"].astype(int)
        st.table(sorumlu_df)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
