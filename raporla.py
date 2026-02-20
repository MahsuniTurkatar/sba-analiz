import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_data():
    try:
        # Sayfaları oku
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1")
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot")
        
        # Temizlik
        df_r.columns = df_r.columns.str.strip()
        df_r['Adı Soyadı'] = df_r['Adı Soyadı'].astype(str).str.strip()
        return df_g, df_r, df_p
    except Exception as e:
        st.error(f"Veri yükleme hatası: {e}")
        return None, None, None

df_gundem, df_raportor, df_pivot = load_data()

# --- CSS: KESİN MERKEZLEME VE İÇERİK KADAR GENİŞLİK ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3 { color: #FFFFFF !important; text-align: center !important; }
    
    /* METRİKLERİ YAN YANA VE ORTADA TUT */
    [data-testid="stHorizontalBlock"] { justify-content: center !important; gap: 20px !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; padding: 10px 25px !important; width: fit-content !important; min-width: 180px;
    }
    [data-testid="stMetricValue"] { color: #FEDD00 !important; text-align: center !important; font-size: 2.2rem !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; text-align: center !important; }

    /* TABLOLAR: İĞNELENMİŞ GENİŞLİK (İÇERİK KADAR) */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 20px 0; overflow-x: auto; }
    .styled-table { 
        margin: auto; border-collapse: collapse; color: white; font-size: 0.85rem; 
        width: auto !important; table-layout: auto !important; 
    }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px 15px; text-align: center !important; white-space: nowrap; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px 12px; text-align: center !important; white-space: nowrap; }
    
    /* TOPLAM SATIRI */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border-top: 2px solid #FEDD00 !important; }
    
    /* SEKMELER */
    .stTabs [data-baseweb="tab"] p { color: white !important; font-weight: bold; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# GÖRSEL TEMİZLİK FONKSİYONU
def clean_df(df):
    def fmt(x):
        if pd.isna(x) or str(x).strip() in ["0", "0.0", "0.00", ""]: return ""
        try:
            val = float(x)
            return int(val) if val == int(val) else val
        except: return x
    return df.applymap(fmt)

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER (206 ve 5 - ORTADA) ---
col_m1, col_m2 = st.columns(2)
with col_m1: st.metric("Toplam Başvuru", "206")
with col_m2: st.metric("Kurul Sayısı", "5")

# --- 2. GÜNDEM TABLOSU (TOPLAM SATIRI İLE) ---
if df_gundem is not None:
    st.markdown("<h3>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    # Alt Toplam Satırı (Excel verisiyle eşleşen)
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 206, "Düzeltme": 68, "Dilekçe": 45, "Toplam": 319}])
    dg_final = pd.concat([dg, t_row], ignore_index=True)
    
    html_g = clean_df(dg_final).to_html(index=False, classes="styled-table")
    html_g = html_g.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-wrapper">{html_g}</div>', unsafe_allow_html=True)

# --- 3. ANALİZ SEKMELERİ ---
st.markdown("---")
t1, t2, t3, t4 = st.tabs(["📋 Genel Çizelge", "👤 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with t1:
    if df_raportor is not None:
        st.markdown("<h3>📊 Kurul Karar Dağılım Çizelgesi (Tam Liste)</h3>", unsafe_allow_html=True)
        # Tablonun tamamını temizleyip basıyoruz
        df_full = df_raportor.dropna(subset=['Adı Soyadı'])
        html_r = clean_df(df_full).to_html(index=False, classes='styled-table')
        html_r = html_r.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_r}</div>', unsafe_allow_html=True)

with t2:
    if df_raportor is not None:
        r_list = df_raportor[df_raportor['Adı Soyadı'].notna() & (~df_raportor['Adı Soyadı'].str.contains("TOPLAM", case=False))]['Adı Soyadı'].unique()
        sel_r = st.selectbox("Raportör Seçiniz:", r_list)
        rr = df_raportor[df_raportor['Adı Soyadı'] == sel_r].iloc[0]
        
        # İkonlu Tablo Geri Geldi
        rd = {
            "Dosya Türü": ["📜 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "📚 Doktora Tezi", "🩺 Uzmanlık Tezi", "⭐ GENEL TOPLAM"],
            "Onay": [rr.get('Bireysel Araştırma Onay',0), rr.get('Yüksek Lisans Tezi Onay',0), rr.get('Doktora Tezi Onay',0), rr.get('Uzmanlık Tezi Onay',0), rr.get('Onay Toplam',0)],
            "Karar Alınan": [rr.get('BİREYSEL TOPLAM',0), rr.get('YÜKSEK LİSANS TEZİ TOPLAM',0), rr.get('DOKTORA TEZİ TOPLAM',0), rr.get('UZMANLIK TEZİ TOPLAM',0), rr.get('Karar Verilen Toplam ',0)]
        }
        st.markdown(f'<div class="table-wrapper">{clean_df(pd.DataFrame(rd)).to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)
        
        # Atanan-Karar-Bekleyen Kutuları
        c1, c2, c3 = st.columns(3)
        atanan = int(rr['Dosya Sayısı'])
        karar = int(rr['Karar Verilen Toplam '])
        c1.metric("Atanan Dosya", atanan)
        c2.metric("Karar Alınan", karar)
        c3.metric("Bekleyen", atanan - karar)

with t3:
    if df_pivot is not None:
        st.markdown("<h3>🏢 Birim Dağılım Analizi</h3>", unsafe_allow_html=True)
        b = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b.columns = ["Birim Adı", "Sayı"]
        b = b[~b["Birim Adı"].str.contains("Etiketleri|Toplam|Genel", case=False)]
        b.insert(0, "S.No", range(1, len(b) + 1))
        # Toplam iğneleme (206 olmalı)
        b_sum = pd.DataFrame([{"S.No": "TOPLAM", "Birim Adı": "", "Sayı": b['Sayı'].sum()}])
        b_final = pd.concat([b, b_sum], ignore_index=True)
        html_b = clean_df(b_final).to_html(index=False, classes="styled-table")
        html_b = html_b.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_b}</div>', unsafe_allow_html=True)

with t4:
    if df_pivot is not None:
        st.markdown("<h3>👨‍🏫 Sorumlu Araştırmacı Dağılımı</h3>", unsafe_allow_html=True)
        s = df_pivot.iloc[:, [3, 4]].dropna().copy()
        s.columns = ["Sorumlu Araştırmacı", "Sayı"]
        s = s[~s["Sorumlu Araştırmacı"].str.contains("Etiketleri|Toplam|Genel", case=False)]
        s.insert(0, "S.No", range(1, len(s) + 1))
        # Toplam iğneleme (206 olmalı)
        s_sum = pd.DataFrame([{"S.No": "TOPLAM", "Sorumlu Araştırmacı": "", "Sayı": s['Sayı'].sum()}])
        s_final = pd.concat([s, s_sum], ignore_index=True)
        html_s = clean_df(s_final).to_html(index=False, classes="styled-table")
        html_s = html_s.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_s}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:white; padding:20px; font-weight:bold;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
