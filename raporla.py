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
        # 1. Gündem Sayıları
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_g = df_g[df_g['S.NO'].notna()] # Boş satırları at
        
        # 2. Raportör Analizi (Üye_1)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", skiprows=1)
        df_r = df_r.dropna(subset=['Adı Soyadı']) # Boş isimleri at
        
        # 3. Birim ve Sorumlu Analizi (Pivot Sayfası)
        # Pivot sayfasındaki düzenine göre sütunları alıyoruz
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot", skiprows=2)
        
        return df_g, df_r, df_p
    except Exception as e:
        st.error(f"Excel Okuma Hatası: {e}")
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: FB TASARIM VE TABLO ---
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

# --- 1. GÜNDEM SAYILARI (Dinamik Toplam ve Tam Sayı) ---
st.write("### 📅 2026 Gündem Sayıları")
if df_gundem is not None:
    # Sayıları tam sayıya çevir (NaN'ları 0 yaparak)
    cols_to_fix = ['Başvuru', 'Düzeltme', 'Dilekçe', 'Toplam']
    for col in cols_to_fix:
        df_gundem[col] = pd.to_numeric(df_gundem[col], errors='coerce').fillna(0).astype(int)
    
    # Sadece verisi olanları göster + TOPLAM satırı
    actual_data = df_gundem[df_gundem['Gündem Tarihleri'].notna() & (df_gundem['S.NO'] != 'TOPLAM')]
    toplam_row = df_gundem[df_gundem['S.NO'] == 'TOPLAM']
    df_display = pd.concat([actual_data, toplam_row])

    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.markdown(df_display.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.write("#### 📋 Kurul Karar Çizelgesi")
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning(f"⚠️ '{img_path}' dosyası bulunamadı. Lütfen GitHub'a bu isimle yüklediğinizden emin olun.")

with tab2:
    st.write("#### 👥 Raportör Detaylı Analizi")
    if df_raportor is not None:
        r_list = df_raportor["Adı Soyadı"].unique().tolist()
        sec_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = df_raportor[df_raportor["Adı Soyadı"] == sec_r].iloc[0]
        
        c1, c2, c3 = st.columns(3)
        atanan = int(r_row["Dosya Sayısı"])
        # Toplam Onay (Üye_1 sayfasındaki son sütundan veya Onay sütunlarından biri)
        onay_toplam = int(r_row["TOPLAM"] if "TOPLAM" in r_row else r_row.iloc[-1]) 
        
        c1.metric("📌 Atanan Dosya", atanan)
        c2.metric("✅ Karar Verilen", onay_toplam)
        c3.metric("⏳ Bekleyen", atanan - onay_toplam)

with tab3:
    st.write("#### 🏢 Birim Analizi (Pivot)")
    if df_pivot is not None:
        # Excel Pivot sayfasındaki ilk iki sütunu (Birim ve Sayı) alıyoruz
        birim_df = df_pivot.iloc[:, [0, 1]].dropna().head(10)
        birim_df.columns = ["Birim Adı", "Dosya Sayısı"]
        st.table(birim_df)

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Analizi")
    if df_pivot is not None:
        # Excel Pivot sayfasındaki Sorumlu Araştırmacı sütunlarını (genelde 3. ve 4. sütunlar) alıyoruz
        sorumlu_df = df_pivot.iloc[:, [3, 4]].dropna().head(10)
        sorumlu_df.columns = ["Araştırmacı", "Toplam Dosya"]
        st.table(sorumlu_df)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
