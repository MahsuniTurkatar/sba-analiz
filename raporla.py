import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_all_data():
    try:
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1")
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot")
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: BEYAZ BAŞLIKLAR VE TAM ORTALI NİZAM ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BEYAZ BAŞLIKLAR */
    h1, h2, h3, h4, .stMetric label, [data-baseweb="tab"] p { 
        color: #FFFFFF !important; 
        text-align: center !important;
        font-weight: bold !important;
    }
    
    /* METRİK KUTULARI: Sarı ve Merkeze Yakın */
    [data-testid="stMetricValue"] { color: #FEDD00 !important; text-align: center !important; font-size: 1.8rem !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
        width: 180px !important; margin: auto !important;
    }
    
    /* TABLO TASARIMI: Tamamen Ortalı */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 10px 0; }
    .styled-table { width: auto !important; border-collapse: collapse; color: white; font-size: 0.85rem; margin: auto; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px 12px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 6px 12px; text-align: center !important; }
    
    /* TOPLAM SATIRI: Lacivert Zemin, Sarı Yazı */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border: 2px solid #FEDD00 !important; }

    hr { border: 0.5px solid #FEDD00; opacity: 0.2; }
    .footer { text-align: center; color: #FFFFFF; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Sıfırları gizleme fonksiyonu
def clean_zeros(val):
    if str(val) == "0" or str(val) == "0.0" or val is None:
        return ""
    return val

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. ANA METRİKLER ---
m_col1, m_c1, m_c2, m_col2 = st.columns([2, 1, 1, 2])
with m_c1: st.metric("Toplam Başvuru", "206")
with m_c2: st.metric("Kurul Sayısı", "5")

# --- 2. GÜNDEM SAYILARI (SIFIRSIZ) ---
if df_gundem is not None:
    st.markdown("<h3>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    df_g_show = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    df_g_show = df_g_show[df_g_show['Toplam'] > 0] # Sadece dolu gündemler
    df_g_show['Gündem Tarihleri'] = pd.to_datetime(df_g_show['Gündem Tarihleri']).dt.strftime('%d.%m.%Y')
    
    html_g = df_g_show.applymap(clean_zeros).to_html(index=False, classes='styled-table')
    st.markdown(f'<div class="table-wrapper">{html_g}</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Analizi"])

with tab1:
    st.markdown("<h3>📊 Genel Karar Dağılım Çizelgesi</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        try:
            # Dosyadaki gerçek sütun isimlerini kullanarak toplamları çekiyoruz
            total_data = df_raportor[df_raportor['Adı Soyadı'].astype(str).str.contains("TOPLAM", na=False)].iloc[0]
            
            ciz_dict = {
                "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi", "📊 GENEL TOPLAM"],
                "Onay": [total_data['Bireysel Araştırma Onay'], total_data['Yüksek Lisans Tezi Onay'], total_data['Doktora Tezi Onay'], total_data['Uzmanlık Tezi Onay'], 166],
                "Düzeltme": [total_data['Bireysel Araştırma Düzeltme'], 0, total_data['Doktora Tezi  Düzeltme'], total_data['Uzmanlık Tezi Düzeltme'], 104],
                "KAEK": [total_data['Bireysel Araştırma KAEK'], 0, total_data['Doktora Tezi KAEK'], total_data['Uzmanlık Tezi KAEK'], 6],
                "Görüş": [total_data['Bireysel Araştırma Görüş'], 0, total_data['Doktora Tezi Görüş'], total_data['Uzmanlık Tezi Görüş'], 4],
                "TOPLAM": [total_data['BİREYSEL TOPLAM'], total_data['YÜKSEK LİSANS TEZİ TOPLAM'], total_data['DOKTORA TEZİ TOPLAM'], total_data['UZMANLIK TEZİ TOPLAM'], 286]
            }
            df_c = pd.DataFrame(ciz_dict)
            html_c = df_c.applymap(clean_zeros).to_html(index=False, classes='styled-table')
            html_c = html_c.replace('<td>📊 GENEL TOPLAM</td>', '<td class="total-row">📊 GENEL TOPLAM</td>')
            st.markdown(f'<div class="table-wrapper">{html_c}</div>', unsafe_allow_html=True)
        except: st.error("Çizelge verisi çekilemedi.")

with tab2:
    st.markdown("<h3>👥 Raportör Karar Ayrıntıları</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        r_list = df_raportor[df_raportor['Adı Soyadı'].notna() & (~df_raportor['Adı Soyadı'].str.contains("TOPLAM|S.No", na=False))]['Adı Soyadı'].unique()
        selected_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = df_raportor[df_raportor['Adı Soyadı'] == selected_r].iloc[0]

        r_detay = {
            "Başvuru Türü": ["📄 Bireysel", "🎓 Yüksek Lisans", "🔬 Doktora", "🏥 Uzmanlık", "📊 TOPLAM"],
            "Onay": [r_row['Bireysel Araştırma Onay'], r_row['Yüksek Lisans Tezi Onay'], r_row['Doktora Tezi Onay'], r_row['Uzmanlık Tezi Onay'], r_row['Onay Toplam']],
            "Düzeltme": [r_row['Bireysel Araştırma Düzeltme'], 0, r_row['Doktora Tezi  Düzeltme'], r_row['Uzmanlık Tezi Düzeltme'], r_row['Düzeltme Toplam ']],
            "KAEK": [r_row['Bireysel Araştırma KAEK'], 0, r_row['Doktora Tezi KAEK'], r_row['Uzmanlık Tezi KAEK'], r_row['KAEK  Toplam ']],
            "TOPLAM": [r_row['BİREYSEL TOPLAM'], r_row['YÜKSEK LİSANS TEZİ TOPLAM'], r_row['DOKTORA TEZİ TOPLAM'], r_row['UZMANLIK TEZİ TOPLAM'], r_row['Karar Verilen Toplam ']]
        }
        html_r = pd.DataFrame(r_detay).applymap(clean_zeros).to_html(index=False, classes='styled-table').replace('<td>📊 TOPLAM</td>', '<td class="total-row">📊 TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_r}</div>', unsafe_allow_html=True)
        
        # RAPORTÖR METRİKLERİ (YAKINLAŞTIRILMIŞ)
        st.markdown("<br>", unsafe_allow_html=True)
        rc1, rc2, rc3, rc4, rc5 = st.columns([1.5, 1, 1, 1, 1.5])
        with rc2: st.metric("Atanan", r_row['Dosya Sayısı'])
        with rc3: st.metric("Karar", r_row['Karar Verilen Toplam '])
        with rc4: st.metric("Bekleyen", int(r_row['Dosya Sayısı']) - int(r_row['Karar Verilen Toplam ']))

with tab3:
    st.markdown("<h3>🏢 Birim Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        # Pivot dosyasındaki ilk iki sütun: Birimler
        b_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b_df.columns = ["Birim Adı", "Dosya Sayısı"]
        b_df = b_df[~b_df["Birim Adı"].str.contains("Etiketleri|Toplam|Genel", na=False)]
        b_df["Dosya Sayısı"] = b_df["Dosya Sayısı"].astype(int)
        
        b_sum = b_df["Dosya Sayısı"].sum()
        b_df = pd.concat([b_df, pd.DataFrame([{"Birim Adı": "GENEL TOPLAM", "Dosya Sayısı": b_sum}])], ignore_index=True)
        b_df.insert(0, "S.NO", range(1, len(b_df) + 1))
        
        html_b = b_df.to_html(index=False, classes='styled-table').replace('<td>GENEL TOPLAM</td>', '<td class="total-row">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_b}</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("<h3>👨‍🏫 Sorumlu Araştırmacı Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        # Pivot dosyasındaki 4. ve 5. sütunlar: Sorumlular
        s_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        s_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        s_df = s_df[~s_df["Sorumlu Araştırmacı"].str.contains("Etiketleri|Toplam|Genel", na=False)]
        s_df["Dosya Sayısı"] = s_df["Dosya Sayısı"].astype(int)
        
        s_sum = s_df["Dosya Sayısı"].sum()
        s_df = pd.concat([s_df, pd.DataFrame([{"Sorumlu Araştırmacı": "GENEL TOPLAM", "Dosya Sayısı": s_sum}])], ignore_index=True)
        s_df.insert(0, "S.NO", range(1, len(s_df) + 1))
        
        html_s = s_df.to_html(index=False, classes='styled-table').replace('<td>GENEL TOPLAM</td>', '<td class="total-row">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_s}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
