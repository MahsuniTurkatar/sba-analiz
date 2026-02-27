import streamlit as st
import pandas as pd

# --- SABİT AYARLAR ---
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

@st.cache_data
def load_data():
    try:
        # Excel'i en saf haliyle, başlıkları ellemeden okuyoruz
        df_g = pd.read_excel("2026_SBA.xlsx", sheet_name="Sayılar")
        df_r = pd.read_excel("2026_SBA.xlsx", sheet_name="Üye_1", header=None) # Header=None ile tüm satırları alıyoruz
        df_p = pd.read_excel("2026_SBA.xlsx", sheet_name="Pivot")
        return df_g, df_r, df_p
    except Exception as e:
        st.error(f"Dosya Okuma Hatası: {e}")
        return None, None, None

df_g, df_r, df_p = load_data()

# --- CSS: MÜHÜRLÜ VE GENİŞ TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .centered-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 2.2rem; margin: 30px 0; }
    .section-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 1.8rem; margin: 25px 0; display: block; }
    
    /* GÖSTERGELER (İKONLAR KALDIRILDI) */
    .metric-row { display: flex; justify-content: center; gap: 20px; margin-bottom: 25px; flex-wrap: wrap; }
    .main-box { background-color: #001d3d; border: 2px solid #FEDD00; border-radius: 12px; padding: 20px 45px; text-align: center; min-width: 200px; }
    .main-val { color: #FEDD00; font-size: 3.5rem; font-weight: bold; display: block; line-height: 1; }
    .main-lab { color: #ffffff; font-size: 1.2rem; display: block; margin-top: 8px; }

    .sub-box { background-color: #001d3d; border: 1px solid #FEDD00; border-radius: 8px; padding: 15px; text-align: center; min-width: 160px; }
    .sub-val { color: #FEDD00; font-size: 1.8rem; font-weight: bold; }
    .sub-lab { color: #ffffff; font-size: 0.9rem; display: block; margin-top: 5px; }

    /* TABLOLAR (GENİŞ VE EXCEL GİBİ) */
    .table-wrapper { display: flex; justify-content: center; width: 100%; overflow-x: auto; padding: 10px; }
    .styled-table { border-collapse: collapse; color: white !important; font-size: 0.85rem; width: 100%; margin: auto; }
    .styled-table td, .styled-table th { border: 1px solid #FEDD00; padding: 8px; text-align: center; background-color: #001d3d; color: white !important; }
    
    .wide-table-wrapper { width: 100%; overflow-x: auto; border: 1px solid #FEDD00; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

def fmt(val):
    if pd.isna(val) or val == "" or str(val).strip() in ["0", "0.0", "nan"]: return ""
    try: return str(int(float(val)))
    except: return str(val)

# --- ÜST GÖSTERGELER ---
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

# --- ANALİZ SEKMELERİ ---
t1, t2, t3, t4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Araştırmacı Analizi"])

with t1:
    st.markdown('<div class="section-title">📄 Genel Karar Çizelgesi</div>', unsafe_allow_html=True)
    if df_r is not None:
        # Excel'in Üye_1 sayfasını 1. satırdan itibaren (başlıklar dahil) olduğu gibi basıyoruz
        st.markdown('<div class="wide-table-wrapper">' + df_r.applymap(fmt).to_html(index=False, header=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with t2:
    st.markdown('<div class="section-title">👥 Raportör Karar Ayrıntıları</div>', unsafe_allow_html=True)
    if df_r is not None:
        # Raportör isimlerini B sütunundan (1. index) çekiyoruz
        r_list = df_r.iloc[2:14, 1].dropna().tolist()
        sec_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = df_r[df_r.iloc[:, 1] == sec_r].iloc[0]
        
        # Veri eşleştirme (Excel sütun sıralamana göre)
        atanan = r_row.iloc[2]
        onay = r_row.iloc[-8] # ONAY sütununun yeri
        karar_verilen = r_row.iloc[-2] # TOPLAM sütununun yeri (Bekleyen'den bir önceki)
        bekleyen = r_row.iloc[-1] # En sağdaki yeni açtığın "Bekleyen" sütunu

        res_df = pd.DataFrame({
            "Kategori": ["📌 Atanan Dosya", "✅ Onay Toplam", "📊 Karar Verilen", "⏳ Bekleyen Dosya Sayısı", "📉 Bekleyen / 2"],
            "Değer": [fmt(atanan), fmt(onay), fmt(karar_verilen), fmt(bekleyen), fmt(float(bekleyen)/2 if bekleyen != "" else "")]
        })
        st.markdown('<div class="table-wrapper">' + res_df.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="section-title">🏢 Birim Analizi</div>', unsafe_allow_html=True)
    if df_p is not None:
        b_df = df_p.iloc[1:, [0, 1]].dropna()
        b_df.columns = ["Birim Adı", "Sayı"]
        st.markdown('<div class="table-wrapper">' + b_df.applymap(fmt).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with t4:
    st.markdown('<div class="section-title">👨‍🏫 Sorumlu Araştırmacı Analizi</div>', unsafe_allow_html=True)
    if df_p is not None:
        s_df = df_p.iloc[1:, [3, 4]].dropna()
        s_df.columns = ["Araştırmacı", "Sayı"]
        st.markdown('<div class="table-wrapper">' + s_df.applymap(fmt).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
