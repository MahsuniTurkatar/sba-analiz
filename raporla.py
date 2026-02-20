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
        # Gündem Sayıları
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        # Raportör Analizi (Üye_1)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1")
        # PİVOT
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot") 
        
        df_r.columns = df_r.columns.str.strip()
        df_r['Adı Soyadı'] = df_r['Adı Soyadı'].astype(str).str.strip()
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: FB TASARIMI VE GELİŞMİŞ TABLO DÜZENİ ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    h1, h2, h3, h4 { color: #FEDD00 !important; text-align: center !important; }
    
    /* METRİKLER VE KARTLAR */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
    }
    [data-testid="stMetricValue"] { color: #FEDD00 !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; }

    .nitelik-container { display: flex; justify-content: space-between; gap: 10px; margin: 20px 0; }
    .nitelik-card {
        flex: 1; background-color: #001d3d; border: 1px solid #FEDD00;
        border-radius: 8px; padding: 15px; text-align: center;
    }
    .n-val { color: #FEDD00; font-size: 1.5rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.9rem; }

    /* TABLOLAR: TAM GENİŞLİK VE SABİT TASARIM */
    .table-container { display: flex; justify-content: center; margin: 20px 0; width: 100%; overflow-x: auto; }
    .styled-table { width: 100% !important; border-collapse: collapse; color: white; margin-bottom: 20px; font-size: 0.85rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center !important; }
    
    /* TOPLAM SATIRI VURGUSU */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border-top: 2px solid #FEDD00 !important; }
    
    .stTabs [data-baseweb="tab"] p { color: #FEDD00 !important; font-weight: bold; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Veri Temizleme (0'ları gizle, sayıları tam sayı yap)
def clean_df(df):
    return df.applymap(lambda x: "" if (pd.isna(x) or str(x).strip() in ["0", "0.0", "0.00"]) else (int(x) if isinstance(x, (int, float)) else x))

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- ÜST METRİKLER (206 ve 5 Olarak Güncellendi) ---
c_m1, c_m2 = st.columns(2)
with c_m1: st.metric("📌 Toplam Başvuru", "206")
with c_m2: st.metric("🗓️ Kurul Sayısı", "5")

# --- NİTELİK KARTLARI ---
st.markdown("""
    <div class="nitelik-container">
        <div class="nitelik-card"><span class="n-val">128</span><span class="n-lab">Bireysel Araştırma</span></div>
        <div class="nitelik-card"><span class="n-val">48</span><span class="n-lab">Uzmanlık Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">12</span><span class="n-lab">Y. Lisans Tezi</span></div>
        <div class="nitelik-card"><span class="n-val">18</span><span class="n-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 1. GÜNDEM SAYILARI (SAKIN BOZMA DEDİĞİN KISIM) ---
if df_gundem is not None:
    st.write("### 📅 2026 Gündem Sayıları")
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg = dg[dg['Toplam'] > 0]
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    # Toplam Satırı
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 206, "Düzeltme": 68, "Dilekçe": 45, "Toplam": 319}])
    dg_final = pd.concat([dg, t_row], ignore_index=True)
    
    html_g = clean_df(dg_final).to_html(index=False, classes='styled-table')
    html_g = html_g.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
    st.markdown(f'<div class="table-container">{html_g}</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.write("#### 📋 Genel Karar Dağılım Tablosu (Tam Liste)")
    if df_raportor is not None:
        # Tablonun tamamını al (Sadece toplamlar değil)
        df_all = df_raportor.dropna(subset=['Adı Soyadı']).copy()
        html_all = clean_df(df_all).to_html(index=False, classes='styled-table')
        html_all = html_all.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
        st.markdown(f'<div class="table-container">{html_all}</div>', unsafe_allow_html=True)

with tab2:
    st.write("#### 👥 Raportör Karar Ayrıntıları (İkonlu)")
    if df_raportor is not None:
        r_list = df_raportor[df_raportor['Adı Soyadı'].notna() & (~df_raportor['Adı Soyadı'].str.contains("TOPLAM", case=False))]['Adı Soyadı'].unique()
        sec_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = df_raportor[df_raportor['Adı Soyadı'] == sec_r].iloc[0]

        # İkonlu Detay Tablosu
        rd = {
            "Dosya Türü": ["📜 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "📚 Doktora Tezi", "🩺 Uzmanlık Tezi", "⭐ GENEL TOPLAM"],
            "Onay": [r_row.get('Bireysel Araştırma Onay',0), r_row.get('Yüksek Lisans Tezi Onay',0), r_row.get('Doktora Tezi Onay',0), r_row.get('Uzmanlık Tezi Onay',0), r_row.get('Onay Toplam',0)],
            "Karar Alınan": [r_row.get('BİREYSEL TOPLAM',0), r_row.get('YÜKSEK LİSANS TEZİ TOPLAM',0), r_row.get('DOKTORA TEZİ TOPLAM',0), r_row.get('UZMANLIK TEZİ TOPLAM',0), r_row.get('Karar Verilen Toplam ',0)]
        }
        st.markdown('<div class="table-container">' + clean_df(pd.DataFrame(rd)).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)
        
        # Alt Metrikler (Atanan-Karar-Bekleyen)
        c1, c2, c3 = st.columns(3)
        atanan = int(r_row['Dosya Sayısı'])
        karar = int(r_row['Karar Verilen Toplam '])
        c1.metric("Atanan Dosya", atanan)
        c2.metric("Karar Alınan", karar)
        c3.metric("Bekleyen", atanan - karar)

with tab3:
    st.write("#### 🏢 Birim Analizi")
    if df_pivot is not None:
        b = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b.columns = ["Birim Adı", "Sayı"]
        b = b[~b["Birim Adı"].str.contains("Etiketleri|Toplam|Genel", case=False)]
        b.insert(0, "S.No", range(1, len(b) + 1))
        
        # Alt Toplam
        b_sum = pd.DataFrame([{"S.No": "TOPLAM", "Birim Adı": "", "Sayı": b['Sayı'].sum()}])
        b_final = pd.concat([b, b_sum], ignore_index=True)
        
        html_b = clean_df(b_final).to_html(index=False, classes='styled-table')
        html_b = html_b.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
        st.markdown(f'<div class="table-container">{html_b}</div>', unsafe_allow_html=True)

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Analizi")
    if df_pivot is not None:
        s = df_pivot.iloc[:, [3, 4]].dropna().copy()
        s.columns = ["Sorumlu Araştırmacı", "Sayı"]
        s = s[~s["Sorumlu Araştırmacı"].str.contains("Etiketleri|Toplam|Genel", case=False)]
        s.insert(0, "S.No", range(1, len(s) + 1))
        
        # Alt Toplam
        s_sum = pd.DataFrame([{"S.No": "TOPLAM", "Sorumlu Araştırmacı": "", "Sayı": s['Sayı'].sum()}])
        s_final = pd.concat([s, s_sum], ignore_index=True)
        
        html_s = clean_df(s_final).to_html(index=False, classes='styled-table')
        html_s = html_s.replace('<td>TOPLAM</td>', '<td class="total-row">TOPLAM</td>')
        st.markdown(f'<div class="table-container">{html_s}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
