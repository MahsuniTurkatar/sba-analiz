import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_data():
    try:
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1")
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot")
        # Sütun isimlerindeki gizli boşlukları temizle
        df_r.columns = df_r.columns.str.strip()
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_data()

# --- CSS: BEYAZ BAŞLIKLAR VE KUSURSUZ ORTALAMA ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BAŞLIKLAR: Beyaz ve Ortalı */
    h1, h2, h3, h4, .stMetric label, [data-baseweb="tab"] p { 
        color: #FFFFFF !important; 
        text-align: center !important;
        justify-content: center !important;
        font-weight: bold !important;
    }
    
    /* METRİKLER: Tam Merkez */
    [data-testid="stMetricValue"] { color: #FEDD00 !important; text-align: center !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
        width: 180px !important; margin: auto !important;
    }
    
    /* TABLOLAR: Milimetrik Ortalama */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 15px 0; }
    .styled-table { width: auto !important; border-collapse: collapse; color: white; font-size: 0.85rem; margin: auto; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px 15px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px 15px; text-align: center !important; }
    
    /* TOPLAM SATIRI (FB Renkleri) */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border: 2px solid #FEDD00 !important; }

    .footer { text-align: center; color: #FFFFFF; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# SIFIRLARI SİLME FONKSİYONU
def hide_zeros(df):
    return df.mask(df == 0, "").mask(df == "0", "")

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. ANA METRİKLER ---
m_l, m_c1, m_c2, m_r = st.columns([2, 1, 1, 2])
with m_c1: st.metric("Toplam Başvuru", "206")
with m_c2: st.metric("Kurul Sayısı", "5")

# --- 2. GÜNDEM (SIFIRSIZ VE ORTALI) ---
if df_gundem is not None:
    st.markdown("<h3>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    df_g_clean = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    df_g_clean = df_g_clean[df_g_clean['Toplam'] > 0]
    df_g_clean['Gündem Tarihleri'] = pd.to_datetime(df_g_clean['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    html_g = hide_zeros(df_g_clean).to_html(index=False, classes='styled-table')
    st.markdown(f'<div class="table-wrapper">{html_g}</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.markdown("<h3>📊 Genel Karar Dağılım Çizelgesi</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        tr = df_raportor[df_raportor['Adı Soyadı'].astype(str).str.contains("TOPLAM", na=False)].iloc[0]
        ciz_dict = {
            "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi", "📊 GENEL TOPLAM"],
            "Onay": [tr['Bireysel Araştırma Onay'], tr['Yüksek Lisans Tezi Onay'], tr['Doktora Tezi Onay'], tr['Uzmanlık Tezi Onay'], 166],
            "Düzeltme": [tr['Bireysel Araştırma Düzeltme'], 0, tr['Doktora Tezi  Düzeltme'], tr['Uzmanlık Tezi Düzeltme'], 104],
            "KAEK": [tr['Bireysel Araştırma KAEK'], 0, tr['Doktora Tezi KAEK'], tr['Uzmanlık Tezi KAEK'], 6],
            "TOPLAM": [tr['BİREYSEL TOPLAM'], tr['YÜKSEK LİSANS TEZİ TOPLAM'], tr['DOKTORA TEZİ TOPLAM'], tr['UZMANLIK TEZİ TOPLAM'], 286]
        }
        html_c = hide_zeros(pd.DataFrame(ciz_dict)).to_html(index=False, classes='styled-table')
        html_c = html_c.replace('<td>📊 GENEL TOPLAM</td>', '<td class="total-row">📊 GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_c}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("<h3>👥 Raportör Karar Ayrıntıları</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        r_list = df_raportor[df_raportor['Adı Soyadı'].notna() & (~df_raportor['Adı Soyadı'].str.contains("TOPLAM|S.No", na=False))]['Adı Soyadı'].unique()
        sr = st.selectbox("Raportör:", r_list)
        rr = df_raportor[df_raportor['Adı Soyadı'] == sr].iloc[0]

        r_data = {
            "Başvuru Türü": ["📄 Bireysel", "🎓 Yüksek Lisans", "🔬 Doktora", "🏥 Uzmanlık", "📊 TOPLAM"],
            "Onay": [rr['Bireysel Araştırma Onay'], rr['Yüksek Lisans Tezi Onay'], rr['Doktora Tezi Onay'], rr['Uzmanlık Tezi Onay'], rr['Onay Toplam']],
            "Düzeltme": [rr['Bireysel Araştırma Düzeltme'], 0, rr['Doktora Tezi  Düzeltme'], rr['Uzmanlık Tezi Düzeltme'], rr['Düzeltme Toplam']],
            "TOPLAM": [rr['BİREYSEL TOPLAM'], rr['YÜKSEK LİSANS TEZİ TOPLAM'], rr['DOKTORA TEZİ TOPLAM'], rr['UZMANLIK TEZİ TOPLAM'], rr['Karar Verilen Toplam']]
        }
        html_r = hide_zeros(pd.DataFrame(r_data)).to_html(index=False, classes='styled-table').replace('<td>📊 TOPLAM</td>', '<td class="total-row">📊 TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_r}</div>', unsafe_allow_html=True)
        
        # Yakınlaştırılmış Metrikler
        c1, c2, c3, c4, c5 = st.columns([1.5, 1, 1, 1, 1.5])
        with c2: st.metric("Atanan", int(rr['Dosya Sayısı']))
        with c3: st.metric("Karar", int(rr['Karar Verilen Toplam']))
        with c4: st.metric("Bekleyen", int(rr['Dosya Sayısı']) - int(rr['Karar Verilen Toplam']))

with tab3:
    st.markdown("<h3>🏢 Birim Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        b_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b_df.columns = ["Birim Adı", "Dosya Sayısı"]
        b_df = b_df[~b_df["Birim Adı"].str.contains("Etiketleri|Toplam|Genel", na=False)]
        b_sum = b_df["Dosya Sayısı"].astype(int).sum()
        b_df = pd.concat([b_df, pd.DataFrame([{"Birim Adı": "GENEL TOPLAM", "Dosya Sayısı": b_sum}])], ignore_index=True)
        b_df.insert(0, "S.NO", range(1, len(b_df) + 1))
        
        html_b = b_df.to_html(index=False, classes='styled-table').replace('<td>GENEL TOPLAM</td>', '<td class="total-row">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_b}</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("<h3>👨‍🏫 Sorumlu Araştırmacı Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        s_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        s_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        s_df = s_df[~s_df["Sorumlu Araştırmacı"].str.contains("Etiketleri|Toplam|Genel", na=False)]
        s_sum = s_df["Dosya Sayısı"].astype(int).sum()
        s_df = pd.concat([s_df, pd.DataFrame([{"Sorumlu Araştırmacı": "GENEL TOPLAM", "Dosya Sayısı": s_sum}])], ignore_index=True)
        s_df.insert(0, "S.NO", range(1, len(s_df) + 1))
        
        html_s = s_df.to_html(index=False, classes='styled-table').replace('<td>GENEL TOPLAM</td>', '<td class="total-row">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_s}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
