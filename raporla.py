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
        # Gündem Sayıları
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        # Raportör Analizi (Üye_1)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", skiprows=1)
        # PİVOT
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot") 
        # Sütun isimlerindeki boşlukları temizle
        df_r.columns = [str(c).strip() for c in df_r.columns]
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: ÇİVİLENMİŞ TASARIM (SARI-LACİVERT VE SAYI ÜSTTE) ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* ANA BAŞLIKLAR */
    .main-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 2.2rem; margin-bottom: 25px; }
    h3, h4 { color: #FEDD00 !important; }

    /* İĞNELENMİŞ KUTULAR (SAYI ÜSTTE, YAZI ALTTA) */
    .metric-row { display: flex; justify-content: center; gap: 20px; margin-bottom: 15px; flex-wrap: nowrap; }
    .main-box { background-color: #001d3d; border: 2px solid #FEDD00; border-radius: 12px; padding: 15px 45px; text-align: center; min-width: 200px; }
    .main-val { color: #FEDD00; font-size: 3.2rem; font-weight: bold; display: block; line-height: 1; }
    .main-lab { color: #ffffff; font-size: 1.1rem; display: block; margin-top: 8px; }

    .sub-box { background-color: #001d3d; border: 1px solid #FEDD00; border-radius: 8px; padding: 12px; text-align: center; min-width: 155px; }
    .sub-val { color: #FEDD00; font-size: 1.7rem; font-weight: bold; display: block; }
    .sub-lab { color: #ffffff; font-size: 0.85rem; display: block; }

    /* TABLOLAR VE SEKMELER */
    .table-container { display: flex; justify-content: center; margin: 20px 0; width: 100%; }
    .styled-table { width: auto !important; margin: auto; border-collapse: collapse; color: white; font-size: 0.95rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 12px 20px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px 18px; text-align: center !important; }
    
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold !important; }
    .stTabs [aria-selected="true"] { color: #FEDD00 !important; border-bottom-color: #FEDD00 !important; }
    
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 40px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Sayı Temizleme (.0 lardan kurtulmak için)
def clean_num(val):
    if pd.isna(val) or val == "" or val == 0: return ""
    try: return str(int(float(val)))
    except: return str(val)

# --- 1. ANA PANEL (ÜST TARAF - DOKUNULMAZ) ---
st.markdown('<div class="main-title">Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</div>', unsafe_allow_html=True)

# Çivili Kutular
st.markdown("""
    <div class="metric-row">
        <div class="main-box"><span class="main-val">5</span><span class="main-lab">Kurul Sayısı</span></div>
        <div class="main-box"><span class="main-val">206</span><span class="main-lab">Toplam Başvuru</span></div>
    </div>
    <div class="metric-row">
        <div class="sub-box"><span class="sub-val">135</span><span class="sub-lab">Bireysel Araştırma</span></div>
        <div class="sub-box"><span class="sub-val">41</span><span class="sub-lab">Uzmanlık Tezi</span></div>
        <div class="sub-box"><span class="sub-val">12</span><span class="sub-lab">Y. Lisans Tezi</span></div>
        <div class="sub-box"><span class="sub-val">18</span><span class="sub-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. GÜNDEM SAYILARI (ANA PANELİN PARÇASI) ---
if df_gundem is not None:
    st.markdown("<h3 style='text-align: center;'>📅 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    df_g_final = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    df_g_final['Gündem Tarihleri'] = pd.to_datetime(df_g_final['Gündem Tarihleri'], errors='coerce').dt.strftime('%d.%m.%Y')
    
    # Toplam Satırı
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 206, "Düzeltme": 68, "Dilekçe": 45, "Toplam": 319}])
    df_g_render = pd.concat([df_g_final, t_row], ignore_index=True).applymap(clean_num)
    
    st.markdown('<div class="table-container">' + df_g_render.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

# --- 3. ANALİZ SEKMELERİ ---
st.markdown("<h2 style='text-align: center; color: white;'>📊 ANALİZLER</h2>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path): st.image(img_path, use_container_width=True)
    else: st.info("Karar çizelgesi görseli (genel_tablo_ekran_goruntusu.png) bulunamadı.")

with tab2:
    st.write("#### 👥 Raportör Karar Ayrıntıları")
    if df_raportor is not None:
        r_clean = df_raportor[df_raportor.iloc[:, 1].notna() & (df_raportor.iloc[:, 1] != "Adı Soyadı")].copy()
        r_list = [x for x in r_clean.iloc[:, 1].unique().tolist() if "TOPLAM" not in str(x)]
        sec_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = r_clean[r_clean.iloc[:, 1] == sec_r].iloc[0]
        
        dosya_sayisi = int(pd.to_numeric(r_row.iloc[2], errors='coerce') or 0)
        karar_verilen = int(pd.to_numeric(r_row.iloc[-1], errors='coerce') or 0)
        bekleyen = dosya_sayisi - karar_verilen

        detay_data = {
            "Karar Türü": ["📌 Toplam Dosya", "✅ Onay", "📝 Düzeltme", "🏛️ KAEK", "💬 Görüş", "❌ Ret", "🚫 Kapsam Dışı", "📥 Geri Çekildi", "📊 KARAR VERİLEN", "⏳ BEKLEYEN"],
            "Sayı": [dosya_sayisi, clean_num(r_row.iloc[3]), clean_num(r_row.iloc[4]), clean_num(r_row.iloc[5]), clean_num(r_row.iloc[6]), clean_num(r_row.iloc[7]), clean_num(r_row.iloc[8]), clean_num(r_row.iloc[9]), karar_verilen, bekleyen]
        }
        st.markdown('<div class="table-container">' + pd.DataFrame(detay_data).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tab3:
    st.write("#### 🏢 Birim Analizi")
    if df_pivot is not None:
        birim_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        birim_df.columns = ["Birim Adı", "Dosya Sayısı"]
        birim_df["Dosya Sayısı"] = birim_df["Dosya Sayısı"].apply(clean_num)
        st.markdown('<div class="table-container">' + birim_df.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Analizi")
    if df_pivot is not None:
        sorumlu_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        sorumlu_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        sorumlu_df["Dosya Sayısı"] = sorumlu_df["Dosya Sayısı"].apply(clean_num)
        st.markdown('<div class="table-container">' + sorumlu_df.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
