import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_all_data():
    try:
        # Sayfaları oku
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", header=0) 
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot")
        
        # Sütun isimlerini temizle (Gizli boşlukları ve NaN değerleri engellemek için)
        df_r.columns = [str(c).strip() for c in df_r.columns]
        return df_g, df_r, df_p
    except Exception as e:
        st.error(f"Veri Okuma Hatası: {e}")
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: GÜNCELLENMİŞ TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .centered-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 2.2rem; margin: 30px 0; }
    .section-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 1.8rem; margin: 25px 0; display: block; }
    
    /* GÖSTERGELER (İKONLAR KALDIRILDI) */
    .metric-row { display: flex; justify-content: center; gap: 20px; margin-bottom: 25px; flex-wrap: wrap; }
    .main-box { background-color: #001d3d; border: 2px solid #FEDD00; border-radius: 12px; padding: 20px 45px; text-align: center; min-width: 200px; }
    .main-val { color: #FEDD00; font-size: 3.2rem; font-weight: bold; display: block; line-height: 1; }
    .main-lab { color: #ffffff; font-size: 1.1rem; display: block; margin-top: 8px; }

    .sub-box { background-color: #001d3d; border: 1px solid #FEDD00; border-radius: 8px; padding: 12px; text-align: center; min-width: 155px; }
    .sub-val { color: #FEDD00; font-size: 1.7rem; font-weight: bold; display: block; }
    .sub-lab { color: #ffffff; font-size: 0.85rem; display: block; }

    /* TABLO TASARIMI */
    .table-wrapper { display: flex; justify-content: center; width: 100%; overflow-x: auto; padding: 10px; }
    .styled-table { border-collapse: collapse; color: #ffffff !important; font-size: 0.85rem; width: auto !important; margin: auto; }
    .styled-table th { background-color: #001d3d !important; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px 15px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px 12px; text-align: center !important; background-color: #001d3d; color: white !important; }
    
    .wide-table-wrapper { width: 100%; overflow-x: scroll; border: 1px solid #FEDD00; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold !important; }
    .stTabs [aria-selected="true"] { color: #FEDD00 !important; border-bottom: 3px solid #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 40px; }
    </style>
    """, unsafe_allow_html=True)

def clean_num(val):
    if pd.isna(val) or val == "" or str(val).strip() in ["0", "0.0", "nan"]: return ""
    try: return str(int(float(val)))
    except: return str(val)

# --- 1. ÜST PANEL ---
st.markdown('<div class="centered-title">Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="metric-row">
        <div class="main-box"><span class="main-val">5</span><span class="main-lab">Kurul Sayısı</span></div>
        <div class="main-box"><span class="main-val">225</span><span class="main-lab">Toplam Başvuru</span></div>
    </div>
    <div class="metric-row">
        <div class="sub-box"><span class="sub-val">135</span><span class="sub-lab">Bireysel Araştırma</span></div>
        <div class="sub-box"><span class="sub-val">41</span><span class="sub-lab">Uzmanlık Tezi</span></div>
        <div class="sub-box"><span class="sub-val">12</span><span class="sub-lab">Y. Lisans Tezi</span></div>
        <div class="sub-box"><span class="sub-val">18</span><span class="sub-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. GÜNDEM SAYILARI ---
st.markdown('<div class="section-title">🗓️ 2026 Gündem Sayıları</div>', unsafe_allow_html=True)
if df_gundem is not None:
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri'], errors='coerce').dt.strftime('%d.%m.%Y')
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 225, "Düzeltme": 68, "Dilekçe": 45, "Toplam": 338}])
    st.markdown('<div class="table-wrapper">' + pd.concat([dg, t_row], ignore_index=True).applymap(clean_num).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

# --- 3. ANALİZLER ---
st.markdown('<div class="centered-title">📊 ANALİZLER</div>', unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Araştırmacı Analizi"])

with tab1:
    st.markdown('<div class="section-title">📄 Genel Karar Çizelgesi</div>', unsafe_allow_html=True)
    if df_raportor is not None:
        # TOPLAM sütununu ve Bekleyen sütununu Excel'deki yeni haline göre göster
        df_render = df_raportor.applymap(clean_num)
        st.markdown('<div class="wide-table-wrapper">' + df_render.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">👥 Raportör Karar Ayrıntıları</div>', unsafe_allow_html=True)
    if df_raportor is not None:
        r_list = df_raportor.iloc[:, 1].dropna().unique().tolist()
        sec_r = st.selectbox("Raportör Seçin:", r_list)
        
        # Seçilen raportörün satırını bul
        r_row = df_raportor[df_raportor.iloc[:, 1] == sec_r].iloc[0]
        
        # Excel Sütun Adlarını kullanarak veriyi çek (Index hatasını önlemek için)
        # Sütun isimleri "Onay.4" veya "TOPLAM.4" gibi gelmiş olabilir (pandas birden fazla aynı isimli sütunu böyle numaralandırır)
        try:
            atanan = r_row["Dosya Sayısı"]
            onay = r_row["Onay.4"] if "Onay.4" in r_row else r_row.iloc[-11]
            karar_toplam = r_row["TOPLAM.4"] if "TOPLAM.4" in r_row else r_row.iloc[-1]
            bekleyen = float(atanan) - float(karar_toplam)
        except:
            atanan, onay, karar_toplam, bekleyen = 0, 0, 0, 0

        ik_detay = pd.DataFrame({
            "Karar Türü": ["📌 Atanan Dosya", "✅ Onay Toplam", "📊 Karar Verilen", "⏳ Bekleyen Dosya Sayısı", "📉 Bekleyen / 2"],
            "Sayı": [clean_num(atanan), clean_num(onay), clean_num(karar_toplam), clean_num(bekleyen), clean_num(bekleyen/2)]
        })
        st.markdown('<div class="table-wrapper">' + ik_detay.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title">🏢 Birim Analizi</div>', unsafe_allow_html=True)
    if df_pivot is not None:
        birim_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        birim_df.columns = ["Birim Adı", "Dosya Sayısı"]
        st.markdown('<div class="table-wrapper">' + birim_df[birim_df["Birim Adı"] != "Satır Etiketleri"].applymap(clean_num).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-title">👨‍🏫 Sorumlu Araştırmacı Analizi</div>', unsafe_allow_html=True)
    if df_pivot is not None:
        sorumlu_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        sorumlu_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        st.markdown('<div class="table-wrapper">' + sorumlu_df[sorumlu_df["Sorumlu Araştırmacı"] != "Satır Etiketleri"].applymap(clean_num).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
