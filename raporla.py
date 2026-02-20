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
        # Sayfaları oku
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1")
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot")
        
        # Sütun isimlerini ve "Adı Soyadı" içeriğini temizle
        df_r.columns = df_r.columns.str.strip()
        df_r['Adı Soyadı'] = df_r['Adı Soyadı'].astype(str).str.strip()
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_data()

# --- CSS: KESİN VE NET ORTALAMA ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BAŞLIKLAR VE METRİKLER: BEYAZ VE TAM ORTALI */
    h1, h2, h3, h4, [data-testid="stMetricLabel"] { 
        color: #FFFFFF !important; 
        text-align: center !important; 
        display: block !important;
        width: 100% !important;
    }
    
    /* Metrik Değerleri (Sarı) */
    [data-testid="stMetricValue"] { 
        color: #FEDD00 !important; 
        text-align: center !important; 
    }
    
    /* Metrik Kutusu Konumu */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; 
        border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; 
        text-align: center !important;
        margin: auto !important;
        width: fit-content !important;
        padding: 10px 30px !important;
    }

    /* TABLOLAR: HER ŞEY ORTALI */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 20px 0; }
    .styled-table { margin-left: auto; margin-right: auto; border-collapse: collapse; color: white; font-size: 0.9rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 12px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 10px; text-align: center !important; }
    
    /* TOPLAM SATIRI */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; }

    /* Sekme Yazıları */
    .stTabs [data-baseweb="tab"] p { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# GÖRSEL TEMİZLİK FONKSİYONU (Sıfırları ve .0 uzantılarını siler)
def format_df(df):
    # Sayıları tam sayıya çevir (float'tan kurtul), 0 olanları boş string yap
    return df.applymap(lambda x: "" if (str(x) == "0" or str(x) == "0.0" or pd.isna(x)) else (int(x) if isinstance(x, (float, int)) else x))

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER (206 ve 5 - TAM ORTALI) ---
c1, c2 = st.columns(2)
with c1: st.metric("Toplam Başvuru", "206")
with c2: st.metric("Kurul Sayısı", "5")

# --- 2. GÜNDEM SAYILARI ---
if df_gundem is not None:
    st.markdown("<h3>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    # Sadece geçerli satırları al
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    html_g = format_df(dg).to_html(index=False, classes='styled-table')
    st.markdown(f'<div class="table-wrapper">{html_g}</div>', unsafe_allow_html=True)

# --- SEKMELER ---
t1, t2, t3, t4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör", "🏢 Birim", "👨‍🏫 Sorumlu"])

with t1:
    st.markdown("<h3>📊 Genel Karar Dağılım Çizelgesi</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        try:
            # Hata veren satır için "case-insensitive" ve "strip" yapılmış arama
            tr = df_raportor[df_raportor['Adı Soyadı'].str.contains("TOPLAM", case=False, na=False)].iloc[0]
            
            c_data = {
                "Başvuru Türü": ["📄 Bireysel", "🎓 Y. Lisans", "🔬 Doktora", "🏥 Uzmanlık", "📊 GENEL TOPLAM"],
                "Onay": [tr['Bireysel Araştırma Onay'], tr['Yüksek Lisans Tezi Onay'], tr['Doktora Tezi Onay'], tr['Uzmanlık Tezi Onay'], 166],
                "Düzeltme": [tr['Bireysel Araştırma Düzeltme'], 0, tr['Doktora Tezi  Düzeltme'], tr['Uzmanlık Tezi Düzeltme'], 104],
                "TOPLAM": [tr['BİREYSEL TOPLAM'], tr['YÜKSEK LİSANS TEZİ TOPLAM'], tr['DOKTORA TEZİ TOPLAM'], tr['UZMANLIK TEZİ TOPLAM'], 286]
            }
            html_c = format_df(pd.DataFrame(c_data)).to_html(index=False, classes='styled-table')
            html_c = html_c.replace('<td>📊 GENEL TOPLAM</td>', '<td class="total-row">📊 GENEL TOPLAM</td>')
            st.markdown(f'<div class="table-wrapper">{html_c}</div>', unsafe_allow_html=True)
        except: st.error("Üye_1 sayfasında 'TOPLAM' satırı bulunamadı.")

with t2:
    if df_raportor is not None:
        r_list = df_raportor[df_raportor['Adı Soyadı'].notna() & (~df_raportor['Adı Soyadı'].str.contains("TOPLAM|S.No", case=False, na=False))]['Adı Soyadı'].unique()
        sel_r = st.selectbox("Raportör:", r_list)
        rr = df_raportor[df_raportor['Adı Soyadı'] == sel_r].iloc[0]
        
        st.markdown(f"<h3>👥 {sel_r} - Karar Analizi</h3>", unsafe_allow_html=True)
        
        rd = {
            "Tür": ["Bireysel", "Y.Lisans", "Doktora", "Uzmanlık", "TOPLAM"],
            "Onay": [rr['Bireysel Araştırma Onay'], rr['Yüksek Lisans Tezi Onay'], rr['Doktora Tezi Onay'], rr['Uzmanlık Tezi Onay'], rr['Onay Toplam']],
            "TOPLAM": [rr['BİREYSEL TOPLAM'], rr['YÜKSEK LİSANS TEZİ TOPLAM'], rr['DOKTORA TEZİ TOPLAM'], rr['UZMANLIK TEZİ TOPLAM'], rr['Karar Verilen Toplam']]
        }
        st.markdown(f'<div class="table-wrapper">{format_df(pd.DataFrame(rd)).to_html(index=False, classes="styled-table")}</div>', unsafe_allow_html=True)
        
        # Raportör Metrikleri (Ortalı)
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Atanan", int(rr['Dosya Sayısı']))
        with m2: st.metric("Karar", int(rr['Karar Verilen Toplam']))
        with m3: st.metric("Bekleyen", int(rr['Dosya Sayısı']) - int(rr['Karar Verilen Toplam']))

with t3:
    st.markdown("<h3>🏢 Birim Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        b = df_pivot.iloc[:, [0, 1]].dropna()
        b.columns = ["Birim Adı", "Sayı"]
        b = b[~b["Birim Adı"].str.contains("Etiketleri|Toplam|Genel", case=False, na=False)]
        b_sum = b["Sayı"].astype(int).sum()
        b = pd.concat([b, pd.DataFrame([{"Birim Adı": "GENEL TOPLAM", "Sayı": b_sum}])], ignore_index=True)
        
        html_b = b.to_html(index=False, classes='styled-table').replace('<td>GENEL TOPLAM</td>', '<td class="total-row">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_b}</div>', unsafe_allow_html=True)

with t4:
    st.markdown("<h3>👨‍🏫 Sorumlu Araştırmacı Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        s = df_pivot.iloc[:, [3, 4]].dropna()
        s.columns = ["Sorumlu", "Sayı"]
        s = s[~s["Sorumlu"].str.contains("Etiketleri|Toplam|Genel", case=False, na=False)]
        s_sum = s["Sayı"].astype(int).sum()
        s = pd.concat([s, pd.DataFrame([{"Sorumlu": "GENEL TOPLAM", "Sayı": s_sum}])], ignore_index=True)
        
        html_s = s.to_html(index=False, classes='styled-table').replace('<td>GENEL TOPLAM</td>', '<td class="total-row">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_s}</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:white; padding:20px;">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
