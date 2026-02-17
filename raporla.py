import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması (SABİT)
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

# --- CSS: FB TASARIMI (DOKUNULMAZ) ---
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

# --- ÜST METRİKLER (SABİT) ---
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

# --- NİTELİK KARTLARI (SABİT) ---
st.markdown("""
    <div class="nitelik-container">
        <div class="nitelik-card"><span class="n-val">128</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">48</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">10</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">4</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- GÜNDEM SAYILARI (KESİN FİLTRELEME) ---
if df_gundem is not None:
    df_g_work = df_gundem.copy()
    
    # Sayıları temizle
    for col in ['Başvuru', 'Düzeltme', 'Dilekçe', 'Toplam']:
        if col in df_g_work.columns:
            df_g_work[col] = pd.to_numeric(df_g_work[col], errors='coerce').fillna(0).astype(int)
    
    # Tarihleri GG.AA.YYYY yap (Boşları NaN yap ki süzebilelim)
    df_g_work['Gündem Tarihleri'] = pd.to_datetime(df_g_work['Gündem Tarihleri'], errors='coerce')
    
    # FİLTRE: Tarihi olanları veya S.NO'su "TOPLAM" olanı al
    df_g_final = df_g_work[
        (df_g_work['Gündem Tarihleri'].notna()) | 
        (df_g_work['S.NO'].astype(str).str.contains("TOPLAM", case=False, na=False))
    ].copy()
    
    # Tarihleri metne çevir (Artık GG.AA.YYYY görünecek)
    df_g_final['Gündem Tarihleri'] = df_g_final['Gündem Tarihleri'].dt.strftime('%d.%m.%Y').fillna("-")

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

with tab2:
    st.write("#### 👥 Raportör Detaylı Analizi")
    if df_raportor is not None:
        r_clean = df_raportor[df_raportor.iloc[:, 1].notna() & (df_raportor.iloc[:, 1] != "Adı Soyadı")].copy()
        r_list = [x for x in r_clean.iloc[:, 1].unique().tolist() if "TOPLAM" not in str(x)]
        sec_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = r_clean[r_clean.iloc[:, 1] == sec_r].iloc[0]
        rc1, rc2, rc3 = st.columns(3)
        dosya = int(pd.to_numeric(r_row.iloc[2], errors='coerce') or 0)
        karar = int(pd.to_numeric(r_row.iloc[-1], errors='coerce') or 0)
        rc1.metric("📌 Atanan Dosya", dosya)
        rc2.metric("✅ Karar Verilen", karar)
        rc3.metric("⏳ Bekleyen", dosya - karar)

with tab3:
    st.write("#### 🏢 Birim Analizi")
    if df_pivot is not None:
        birim_df = df_pivot.iloc[:, [0, 1]].dropna()
        birim_df = birim_df[~birim_df.iloc[:, 0].str.contains("Satır Etiketleri|Genel Toplam", na=False)]
        birim_df.columns = ["Birim Adı", "Dosya Sayısı"]
        birim_df["Dosya Sayısı"] = birim_df["Dosya Sayısı"].astype(int)
        birim_df.index = range(1, len(birim_df) + 1)
        st.table(birim_df)

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Analizi")
    if df_pivot is not None:
        sorumlu_df = df_pivot.iloc[:, [3, 4]].dropna()
        sorumlu_df = sorumlu_df[~sorumlu_df.iloc[:, 0].str.contains("Satır Etiketleri|Genel Toplam", na=False)]
        sorumlu_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        sorumlu_df["Dosya Sayısı"] = sorumlu_df["Dosya Sayısı"].astype(int)
        sorumlu_df.index = range(1, len(sorumlu_df) + 1)
        st.table(sorumlu_df)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
