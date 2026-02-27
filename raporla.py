import streamlit as st
import pandas as pd
import numpy as np

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

@st.cache_data
def load_data():
    try:
        # Sayfaları oku
        df_g = pd.read_excel("2026_SBA.xlsx", sheet_name="Sayılar", skiprows=2)
        # Üye_1 sayfasında 1. satırı başlık al, 2. satırı (alt başlıklar) temizle
        df_r = pd.read_excel("2026_SBA.xlsx", sheet_name="Üye_1", header=0)
        df_p = pd.read_excel("2026_SBA.xlsx", sheet_name="Pivot")
        return df_g, df_r, df_p
    except Exception as e:
        st.error(f"Dosya okuma hatası: {e}")
        return None, None, None

df_gundem, df_raportor, df_pivot = load_data()

# --- CSS: FABRİKA AYARLARI ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .centered-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 2.2rem; margin: 30px 0; }
    .section-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 1.8rem; margin: 25px 0; display: block; }
    
    .metric-row { display: flex; justify-content: center; gap: 20px; margin-bottom: 25px; }
    .main-box { background-color: #001d3d; border: 2px solid #FEDD00; border-radius: 12px; padding: 25px 50px; text-align: center; min-width: 220px; }
    .main-val { color: #FEDD00; font-size: 3.5rem; font-weight: bold; display: block; line-height: 1; }
    .main-lab { color: #ffffff; font-size: 1.2rem; display: block; margin-top: 10px; }

    .sub-box { background-color: #001d3d; border: 1px solid #FEDD00; border-radius: 8px; padding: 15px; text-align: center; min-width: 160px; }
    .sub-val { color: #FEDD00; font-size: 1.8rem; font-weight: bold; }
    .sub-lab { color: #ffffff; font-size: 0.9rem; margin-top: 5px; }

    .table-wrapper { display: flex; justify-content: center; width: 100%; overflow-x: auto; padding: 10px; }
    .styled-table { border-collapse: collapse; color: white !important; font-size: 0.9rem; margin: auto; }
    .styled-table th { background-color: #001d3d !important; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 12px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px; text-align: center; background-color: #001d3d; }
    
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

# --- GÜNDEM SAYILARI ---
st.markdown('<div class="section-title">🗓️ 2026 Gündem Sayıları</div>', unsafe_allow_html=True)
if df_gundem is not None:
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].iloc[:4].copy() # Boş satırları alma
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 190, "Düzeltme": 58, "Dilekçe": 41, "Toplam": 289}])
    st.markdown('<div class="table-wrapper">' + pd.concat([dg, t_row]).applymap(fmt).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

# --- ANALİZLER ---
st.markdown('<div class="centered-title">📊 ANALİZLER</div>', unsafe_allow_html=True)
tabs = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Araştırmacı Analizi"])

with tabs[0]:
    st.markdown('<div class="section-title">📄 Genel Karar Çizelgesi</div>', unsafe_allow_html=True)
    if df_raportor is not None:
        # Sadece veri olan satırları göster (TOPLAM satırına kadar)
        df_view = df_raportor.iloc[1:13].applymap(fmt)
        st.markdown('<div class="wide-table-wrapper">' + df_view.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown('<div class="section-title">👥 Raportör Karar Ayrıntıları</div>', unsafe_allow_html=True)
    if df_raportor is not None:
        r_list = df_raportor.iloc[2:13, 1].tolist()
        sec_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = df_raportor[df_raportor.iloc[:, 1] == sec_r].iloc[0]
        
        # Excel'deki tam yerleri (Sütun Sayarak)
        atanan = r_row.iloc[2]
        onay = r_row.iloc[-8] # Sondan 8. sütun Onay Toplam
        karar_toplam = r_row.iloc[-1] # En sondaki Toplam
        bekleyen = float(atanan) - float(karar_toplam)

        res = pd.DataFrame({
            "Kategori": ["📌 Atanan Dosya", "✅ Onay Toplam", "📊 Karar Verilen", "⏳ Bekleyen Dosya Sayısı", "📉 Bekleyen / 2"],
            "Değer": [fmt(atanan), fmt(onay), fmt(karar_toplam), fmt(bekleyen), fmt(bekleyen/2)]
        })
        st.markdown('<div class="table-wrapper">' + res.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tabs[2]:
    st.markdown('<div class="section-title">🏢 Birim Analizi</div>', unsafe_allow_html=True)
    if df_pivot is not None:
        b_df = df_pivot.iloc[:, [0, 1]].dropna().iloc[1:]
        b_df.columns = ["Birim Adı", "Sayı"]
        st.markdown('<div class="table-wrapper">' + b_df.applymap(fmt).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tabs[3]:
    st.markdown('<div class="section-title">👨‍🏫 Sorumlu Araştırmacı Analizi</div>', unsafe_allow_html=True)
    if df_pivot is not None:
        s_df = df_pivot.iloc[:, [3, 4]].dropna().iloc[1:]
        s_df.columns = ["Araştırmacı", "Sayı"]
        st.markdown('<div class="table-wrapper">' + s_df.applymap(fmt).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
