import streamlit as st
import pandas as pd

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
        
        # Sütun isimlerini ve veriyi temizle
        df_r.columns = df_r.columns.str.strip()
        df_r['Adı Soyadı'] = df_r['Adı Soyadı'].astype(str).str.strip()
        return df_g, df_r, df_p
    except Exception as e:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_data()

# --- CSS: İĞNELENMİŞ SÜTUNLAR VE MERKEZİ DÜZEN ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BAŞLIKLAR */
    h1, h2, h3 { color: #FFFFFF !important; text-align: center !important; }
    
    /* METRİKLERİ YAN YANA VE TAM ORTADA TUT (KAPATMA AÇMA DEMİŞTİN) */
    [data-testid="stHorizontalBlock"] {
        justify-content: center !important;
        gap: 20px !important;
    }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; 
        border: 2px solid #FEDD00 !important;
        border-radius: 12px !important;
        padding: 10px 25px !important;
        width: fit-content !important;
        min-width: 180px;
    }
    [data-testid="stMetricValue"] { color: #FEDD00 !important; text-align: center !important; font-size: 2.2rem !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; text-align: center !important; }

    /* TABLOLAR: İĞNELENDİ - SÜTUN GENİŞLİĞİ İÇERİK KADAR */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 20px 0; }
    .styled-table { 
        margin: auto; 
        border-collapse: collapse; 
        color: white; 
        font-size: 0.85rem; 
        width: auto !important; /* İÇERİK KADAR GENİŞLİK */
        table-layout: auto !important; 
    }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px 15px; text-align: center !important; white-space: nowrap; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px 12px; text-align: center !important; white-space: nowrap; }
    
    /* TOPLAM SATIRI */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border-top: 2px solid #FEDD00 !important; }
    
    /* SEKMELER */
    .stTabs [data-baseweb="tab"] p { color: white !important; font-weight: bold; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# TEMİZLİK: .0 ve 0 SİLİCİ
def clean_df(df):
    def fmt(x):
        if pd.isna(x) or str(x).strip() in ["0", "0.0", ""]: return ""
        try: return int(float(x))
        except: return x
    return df.applymap(fmt)

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER (ORTALANMIŞ) ---
_, m1, m2, _ = st.columns([1, 1, 1, 1]) # Kenarlardan sıkıştırıp ortaya topladım
with m1: st.metric("Toplam Başvuru", "206")
with m2: st.metric("Kurul Sayısı", "5")

# --- 2. GÜNDEM SAYILARI (DİNAMİK TOPLAMLI) ---
if df_gundem is not None:
    st.markdown("<h3>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    # Alt Toplam Satırı Oluştur
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": dg['Başvuru'].sum(), "Düzeltme": dg['Düzeltme'].sum(), "Dilekçe": dg['Dilekçe'].sum(), "Toplam": dg['Toplam'].sum()}])
    dg_final = pd.concat([dg, t_row], ignore_index=True)
    
    html_g = clean_df(dg_final).to_html(index=False, classes="styled-table")
    html_g = html_g.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-wrapper">{html_g}</div>', unsafe_allow_html=True)

# --- 3. SEKMELİ ANALİZ MENÜSÜ ---
st.markdown("---")
t1, t2, t3, t4 = st.tabs(["📊 Genel Çizelge", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with t1:
    if df_raportor is not None:
        st.markdown("<h3>📊 Raportör Karar Dağılım Çizelgesi</h3>", unsafe_allow_html=True)
        cols = ["S.No", "Adı Soyadı", "Dosya Sayısı", "BİREYSEL TOPLAM", "YÜKSEK LİSANS TEZİ TOPLAM", "DOKTORA TEZİ TOPLAM", "UZMANLIK TEZİ TOPLAM", "Onay Toplam", "Karar Verilen Toplam "]
        # Sütunların varlığını kontrol et
        actual_cols = [c for c in cols if c in df_raportor.columns]
        df_display = df_raportor[actual_cols].dropna(subset=['Adı Soyadı'])
        
        html_r = clean_df(df_display).to_html(index=False, classes='styled-table')
        html_r = html_r.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_r}</div>', unsafe_allow_html=True)

with t2:
    if df_raportor is not None:
        r_list = df_raportor[df_raportor['Adı Soyadı'].notna() & (~df_raportor['Adı Soyadı'].str.contains("TOPLAM", case=False))]['Adı Soyadı'].unique()
        sel_r = st.selectbox("Raportör Seçiniz:", r_list)
        rr = df_raportor[df_raportor['Adı Soyadı'] == sel_r].iloc[0]
        
        rd = {
            "Başvuru Türü": ["Bireysel Araştırma", "Yüksek Lisans Tezi", "Doktora Tezi", "Uzmanlık Tezi", "GENEL TOPLAM"],
            "Onay": [rr.get('Bireysel Araştırma Onay',0), rr.get('Yüksek Lisans Tezi Onay',0), rr.get('Doktora Tezi Onay',0), rr.get('Uzmanlık Tezi Onay',0), rr.get('Onay Toplam',0)],
            "Karar Toplam": [rr.get('BİREYSEL TOPLAM',0), rr.get('YÜKSEK LİSANS TEZİ TOPLAM',0), rr.get('DOKTORA TEZİ TOPLAM',0), rr.get('UZMANLIK TEZİ TOPLAM',0), rr.get('Karar Verilen Toplam ',0)]
        }
        st.markdown(f'<div class="table-wrapper">{clean_df(pd.DataFrame(rd)).to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)

with t3:
    if df_pivot is not None:
        st.markdown("<h3>🏢 Birim Dağılım Analizi</h3>", unsafe_allow_html=True)
        b = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b.columns = ["Birim Adı", "Sayı"]
        b = b[~b["Birim Adı"].str.contains("Etiketleri|Toplam|Genel", case=False)]
        st.markdown(f'<div class="table-wrapper">{clean_df(b).to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)

with t4:
    if df_pivot is not None:
        st.markdown("<h3>👨‍🏫 Sorumlu Araştırmacı Dağılımı</h3>", unsafe_allow_html=True)
        s = df_pivot.iloc[:, [3, 4]].dropna().copy()
        s.columns = ["Sorumlu Araştırmacı", "Sayı"]
        s = s[~s["Sorumlu Araştırmacı"].str.contains("Etiketleri|Toplam|Genel", case=False)]
        st.markdown(f'<div class="table-wrapper">{clean_df(s).to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:white; padding:20px; font-weight:bold;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
