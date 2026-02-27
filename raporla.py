import streamlit as st
import pandas as pd

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

@st.cache_data
def load_data():
    try:
        df_g = pd.read_excel("2026_SBA.xlsx", sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel("2026_SBA.xlsx", sheet_name="Üye_1", header=0)
        df_p = pd.read_excel("2026_SBA.xlsx", sheet_name="Pivot")
        return df_g, df_r, df_p
    except Exception as e:
        st.error(f"Excel Okuma Hatası: {e}")
        return None, None, None

df_g, df_r, df_p = load_data()

# --- CSS: MÜHÜRLÜ TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .centered-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 2.2rem; margin: 30px 0; }
    .section-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 1.8rem; margin: 25px 0; display: block; }
    
    /* GÖSTERGELER (İKONSUZ) */
    .metric-row { display: flex; justify-content: center; gap: 20px; margin-bottom: 25px; flex-wrap: wrap; }
    .main-box { background-color: #001d3d; border: 2px solid #FEDD00; border-radius: 12px; padding: 20px 45px; text-align: center; min-width: 200px; }
    .main-val { color: #FEDD00; font-size: 3.5rem; font-weight: bold; display: block; line-height: 1; }
    .main-lab { color: #ffffff; font-size: 1.2rem; display: block; margin-top: 8px; }

    .sub-box { background-color: #001d3d; border: 1px solid #FEDD00; border-radius: 8px; padding: 15px; text-align: center; min-width: 160px; }
    .sub-val { color: #FEDD00; font-size: 1.8rem; font-weight: bold; }
    .sub-lab { color: #ffffff; font-size: 0.9rem; display: block; margin-top: 5px; }

    .table-wrapper { display: flex; justify-content: center; width: 100%; overflow-x: auto; padding: 10px; }
    .styled-table { border-collapse: collapse; color: white !important; font-size: 0.85rem; width: auto; margin: auto; }
    .styled-table th { background-color: #001d3d !important; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center; background-color: #001d3d; color: white !important; }
    
    .wide-table-wrapper { width: 100%; overflow-x: scroll; border: 1px solid #FEDD00; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

def fmt(val):
    if pd.isna(val) or val == "" or str(val).strip() in ["0", "0.0", "nan"]: return ""
    try: return str(int(float(val)))
    except: return str(val)

# --- ÜST PANEL (NİTELİK SAYILARI ÜYE_1'DEN ALINDI) ---
st.markdown('<div class="centered-title">Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</div>', unsafe_allow_html=True)
# Nitelik toplamlarını Excel'in alt satırlarından çekiyoruz (Verdiğin Excel'e göre: 225, 10, 30, 72)
st.markdown(f"""
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

# --- ANALİZLER ---
st.markdown('<div class="centered-title">📊 ANALİZLER</div>', unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Araştırmacı Analizi"])

with t1:
    st.markdown('<div class="section-title">📄 Genel Karar Çizelgesi</div>', unsafe_allow_html=True)
    if df_r is not None:
        # 1. ve 2. satır başlık karmaşası olduğu için 2. satırdan (veriden) başlıyoruz
        df_view = df_r.iloc[1:13].applymap(fmt)
        st.markdown('<div class="wide-table-wrapper">' + df_view.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with t2:
    st.markdown('<div class="section-title">👥 Raportör Karar Ayrıntıları</div>', unsafe_allow_html=True)
    if df_r is not None:
        r_names = df_r.iloc[2:13, 1].tolist()
        sec_r = st.selectbox("Raportör Seçin:", r_names)
        r_row = df_r[df_r.iloc[:, 1] == sec_r].iloc[0]
        
        # Excel Sütun Sıralamasına Göre Kesin Çekim
        atanan = r_row.iloc[2]
        onay_toplam = r_row.iloc[-8] # ONAY Sütunu (Excel'de sağdan 8.)
        karar_toplam = r_row.iloc[-1] # EN SAĞDAKİ TOPLAM
        bekleyen = float(atanan) - float(karar_toplam)

        ik_detay = pd.DataFrame({
            "Karar Türü": ["📌 Atanan Dosya", "✅ Onay Toplam", "📊 Karar Verilen", "⏳ Bekleyen Dosya Sayısı", "📉 Bekleyen / 2"],
            "Sayı": [fmt(atanan), fmt(onay_toplam), fmt(karar_toplam), fmt(bekleyen), fmt(bekleyen/2)]
        })
        st.markdown('<div class="table-wrapper">' + ik_detay.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="section-title">🏢 Birim Analizi</div>', unsafe_allow_html=True)
    if df_p is not None:
        b_df = df_p.iloc[1:, [0, 1]].dropna()
        b_df.columns = ["Birim Adı", "Dosya Sayısı"]
        st.markdown('<div class="table-wrapper">' + b_df.applymap(fmt).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with t4:
    st.markdown('<div class="section-title">👨‍🏫 Araştırmacı Analizi</div>', unsafe_allow_html=True)
    if df_p is not None:
        s_df = df_p.iloc[1:, [3, 4]].dropna()
        s_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        st.markdown('<div class="table-wrapper">' + s_df.applymap(fmt).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
