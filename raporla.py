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
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", skiprows=1)
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot", skiprows=1)
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: BEYAZ BAŞLIKLAR VE KESİN SİMETRİ ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Tüm Başlıklar: Beyaz */
    h1, h2, h3, h4, .stMetric label, .stTabs [data-baseweb="tab"] { 
        color: #ffffff !important; 
        text-align: center !important;
        font-weight: bold !important;
    }
    
    /* Metrik Kutuları: Merkeze Hizalı */
    [data-testid="stMetricValue"] { font-size: 2rem !important; color: #FEDD00 !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
        width: 220px !important; margin: auto !important;
    }
    
    /* Tablo Konteynırı ve Tasarımı */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 20px 0; }
    .styled-table { width: auto !important; border-collapse: collapse; color: white; font-size: 0.9rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 10px 15px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px 15px; text-align: center; }
    
    /* SOLA DAYALI İSİMLER (Birim ve Sorumlu) */
    .left-text { text-align: left !important; padding-left: 15px !important; min-width: 320px; }
    
    /* TOPLAM SATIRI: Lacivert Arka Plan, Sarı Yazı */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border: 2px solid #FEDD00 !important; }

    .footer { text-align: center; color: #ffffff; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER (ORTALANMIŞ) ---
m_l, m_c1, m_c2, m_r = st.columns([2, 1, 1, 2])
with m_c1: st.metric("Toplam Başvuru", "190")
with m_c2: st.metric("Kurul Sayısı", "4")

# --- 2. GÜNDEM SAYILARI (SABİT ÜST PANEL) ---
if df_gundem is not None:
    st.markdown("<h3>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    df_g_final = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    df_g_final['Gündem Tarihleri'] = pd.to_datetime(df_g_final['Gündem Tarihleri'], errors='coerce').dt.strftime('%d.%m.%Y')
    
    html_g = df_g_final.to_html(index=False, classes='styled-table')
    st.markdown(f'<div class="table-wrapper">{html_g}</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.markdown("<h3>📊 Genel Karar Dağılım Çizelgesi</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        try:
            t_row = df_raportor[df_raportor.iloc[:, 1].astype(str).str.contains("TOPLAM", na=False)].iloc[0]
            def g(i): return int(pd.to_numeric(t_row.iloc[i], errors='coerce') or 0)
            
            ciz_dict = {
                "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi", "📊 GENEL TOPLAM"],
                "Onay": [g(3), g(11), g(19), g(27), 166],
                "Düzeltme": [g(4), g(12), g(20), g(28), 104],
                "KAEK": [g(5), g(13), g(21), g(29), 6],
                "Görüş": [g(6), g(14), g(22), g(30), 4],
                "Ret": [g(7), g(15), g(23), g(31), 4],
                "Kapsam Dışı": [get_n(8) if 'get_n' in locals() else g(8), g(16), g(24), g(32), 2],
                "Geri Çekildi": [g(9), g(17), g(25), g(33), 0],
                "TOPLAM": [g(10), g(18), g(26), g(34), 286]
            }
            df_c = pd.DataFrame(ciz_dict)
            html_c = df_c.to_html(index=False, classes='styled-table')
            html_c = html_c.replace('<tr>\n      <td>📊 GENEL TOPLAM</td>', '<tr class="total-row">\n      <td>📊 GENEL TOPLAM</td>')
            st.markdown(f'<div class="table-wrapper">{html_c}</div>', unsafe_allow_html=True)
        except: st.error("Çizelge verisi yüklenemedi.")

with tab2:
    st.markdown("<h3>👥 Raportör Karar Ayrıntıları</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        r_list = df_raportor[df_raportor.iloc[:, 1].notna() & (~df_raportor.iloc[:, 1].astype(str).str.contains("Adı Soyadı|TOPLAM", na=False))]
        sec_r = st.selectbox("Raportör Seçin:", r_list.iloc[:, 1].unique())
        r_row = df_raportor[df_raportor.iloc[:, 1] == sec_r].iloc[0]
        def v(i): return int(pd.to_numeric(r_row.iloc[i], errors='coerce') or 0)

        r_data = {
            "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi", "📊 TOPLAM"],
            "Onay": [v(3), v(11), v(19), v(27), v(35)],
            "Düzeltme": [v(4), v(12), v(20), v(28), v(36)],
            "KAEK": [v(5), v(13), v(21), v(29), v(37)],
            "Görüş": [v(6), v(14), v(22), v(30), v(38)],
            "Ret": [v(7), v(15), v(23), v(31), v(39)],
            "Kapsam Dışı": [v(8), v(16), v(24), v(32), v(40)],
            "Geri Çekildi": [v(9), v(17), v(25), v(33), v(41)],
            "TOPLAM": [v(10), v(18), v(26), v(34), v(42)]
        }
        df_r_detay = pd.DataFrame(r_data)
        html_r = df_r_detay.to_html(index=False, classes='styled-table').replace('<td>📊 TOPLAM</td>', '<td class="total-row">📊 TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_r}</div>', unsafe_allow_html=True)
        
        # RAPORTÖR METRİKLERİ
        st.write("---")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("📌 Atanan", v(2))
        with c2: st.metric("✅ Karar", v(42))
        with c3: st.metric("⏳ Bekleyen", v(2) - v(42))

with tab3:
    st.markdown("<h3>🏢 Birim Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        b_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b_df.columns = ["Birim Adı", "Dosya Sayısı"]
        b_df = b_df[~b_df["Birim Adı"].astype(str).str.contains("Etiketleri|Toplam", na=False)]
        b_df["Dosya Sayısı"] = b_df["Dosya Sayısı"].astype(int)
        
        b_total = b_df["Dosya Sayısı"].sum()
        b_df = pd.concat([b_df, pd.DataFrame([{"Birim Adı": "GENEL TOPLAM", "Dosya Sayısı": b_total}])], ignore_index=True)
        b_df.insert(0, "S.NO", range(1, len(b_df) + 1))
        
        html_b = b_df.to_html(index=False, classes='styled-table')
        # Sola dayama hilesi
        html_b = html_b.replace('<td>', '<td class="left-text">', len(b_df)*2).replace('<td class="left-text">', '<td>', len(b_df))
        html_b = html_b.replace('<td>GENEL TOPLAM</td>', '<td class="total-row">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_b}</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("<h3>👨‍🏫 Sorumlu Araştırmacı Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        s_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        s_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        s_df = s_df[~s_df["Sorumlu Araştırmacı"].astype(str).str.contains("Etiketleri|Toplam", na=False)]
        s_df["Dosya Sayısı"] = s_df["Dosya Sayısı"].astype(int)
        
        s_total = s_df["Dosya Sayısı"].sum()
        s_df = pd.concat([s_df, pd.DataFrame([{"Sorumlu Araştırmacı": "GENEL TOPLAM", "Dosya Sayısı": s_total}])], ignore_index=True)
        s_df.insert(0, "S.NO", range(1, len(s_df) + 1))
        
        html_s = s_df.to_html(index=False, classes='styled-table')
        html_s = html_s.replace('<td>', '<td class="left-text">', len(s_df)*2).replace('<td class="left-text">', '<td>', len(s_df))
        html_s = html_s.replace('<td>GENEL TOPLAM</td>', '<td class="total-row">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_s}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
