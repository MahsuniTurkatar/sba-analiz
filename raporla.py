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

# --- CSS: BEYAZ BAŞLIKLAR VE KESİN DÜZEN ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BAŞLIKLARIN TAMAMI BEYAZ */
    h1, h2, h3, h4, .stMetric label, [data-baseweb="tab"] p { 
        color: #FFFFFF !important; 
        text-align: center !important;
        font-weight: bold !important;
    }
    
    /* Metrik Kutuları: Merkeze Hizalı ve Dar */
    [data-testid="stMetricValue"] { font-size: 2rem !important; color: #FEDD00 !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
        width: 220px !important; margin: auto !important;
    }
    
    /* Tablo Tasarımı */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 20px 0; }
    .styled-table { width: auto !important; border-collapse: collapse; color: white; font-size: 0.9rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px 15px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px 15px; text-align: center; }
    
    /* SOLA DAYALI İSİMLER */
    .left-text { text-align: left !important; padding-left: 20px !important; min-width: 350px; }
    
    /* TOPLAM SATIRI: Lacivert Arka Plan, Sarı Yazı */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border: 2px solid #FEDD00 !important; }

    .footer { text-align: center; color: #FFFFFF; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER (TAM ORTADA) ---
m_col_left, m_c1, m_c2, m_col_right = st.columns([2, 1, 1, 2])
with m_c1: st.metric("Toplam Başvuru", "190")
with m_c2: st.metric("Kurul Sayısı", "4")

# --- 2. GÜNDEM SAYILARI (TEPEDE SABİT) ---
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
            # Excel'in en altındaki TOPLAM satırı
            t_row = df_raportor[df_raportor.iloc[:, 1].astype(str).str.contains("TOPLAM", na=False)].iloc[0]
            def g_val(idx): return int(pd.to_numeric(t_row.iloc[idx], errors='coerce') or 0)
            
            ciz_dict = {
                "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi", "📊 GENEL TOPLAM"],
                "Onay": [g_val(3), g_val(11), g_val(19), g_val(27), 166],
                "Düzeltme": [g_val(4), g_val(12), g_val(20), g_val(28), 104],
                "KAEK": [g_val(5), g_val(13), g_val(21), g_val(29), 6],
                "Görüş": [g_val(6), g_val(14), g_val(22), g_val(30), 4],
                "Ret": [g_val(7), g_val(15), g_val(23), g_val(31), 4],
                "Kapsam Dışı": [g_val(8), g_val(16), g_val(24), g_val(32), 2],
                "Geri Çekildi": [g_val(9), g_val(17), g_val(25), g_val(33), 0],
                "TOPLAM": [g_val(10), g_val(18), g_val(26), g_val(34), 286]
            }
            df_c = pd.DataFrame(ciz_dict)
            html_c = df_c.to_html(index=False, classes='styled-table')
            html_c = html_c.replace('<tr>\n      <td>📊 GENEL TOPLAM</td>', '<tr class="total-row">\n      <td>📊 GENEL TOPLAM</td>')
            st.markdown(f'<div class="table-wrapper">{html_c}</div>', unsafe_allow_html=True)
        except Exception: st.error("Veri işleme hatası!")

with tab2:
    st.markdown("<h3>👥 Raportör Karar Ayrıntıları</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        r_names = df_raportor[df_raportor.iloc[:, 1].notna() & (~df_raportor.iloc[:, 1].astype(str).str.contains("Adı Soyadı|TOPLAM", na=False))].iloc[:, 1].unique()
        sec_r = st.selectbox("Raportör Seçin:", r_names)
        r_row = df_raportor[df_raportor.iloc[:, 1] == sec_r].iloc[0]
        def v_val(idx): return int(pd.to_numeric(r_row.iloc[idx], errors='coerce') or 0)

        rd_data = {
            "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi", "📊 TOPLAM"],
            "Onay": [v_val(3), v_val(11), v_val(19), v_val(27), v_val(35)],
            "Düzeltme": [v_val(4), v_val(12), v_val(20), v_val(28), v_val(36)],
            "KAEK": [v_val(5), v_val(13), v_val(21), v_val(29), v_val(37)],
            "Görüş": [v_val(6), v_val(14), v_val(22), v_val(30), v_val(38)],
            "Ret": [v_val(7), v_val(15), v_val(23), v_val(31), v_val(39)],
            "Kapsam Dışı": [v_val(8), v_val(16), v_val(24), v_val(32), v_val(40)],
            "Geri Çekildi": [v_val(9), v_val(17), v_val(25), v_val(33), v_val(41)],
            "TOPLAM": [v_val(10), v_val(18), v_val(26), v_val(34), v_val(42)]
        }
        df_r_tab = pd.DataFrame(rd_data)
        html_r = df_r_tab.to_html(index=False, classes='styled-table').replace('<td>📊 TOPLAM</td>', '<td class="total-row">📊 TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_r}</div>', unsafe_allow_html=True)
        
        # Raportör Metrikleri
        st.write("---")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Atanan Dosya", v_val(2))
        with c2: st.metric("Karar Verilen", v_val(42))
        with c3: st.metric("Bekleyen", v_val(2) - v_val(42))

with tab3:
    st.markdown("<h3>🏢 Birim Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        b_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b_df.columns = ["Birim Adı", "Dosya Sayısı"]
        b_df = b_df[~b_df["Birim Adı"].astype(str).str.contains("Etiketleri|Toplam", na=False)]
        b_df["Dosya Sayısı"] = b_df["Dosya Sayısı"].astype(int)
        
        b_sum = b_df["Dosya Sayısı"].sum()
        b_df = pd.concat([b_df, pd.DataFrame([{"Birim Adı": "GENEL TOPLAM", "Dosya Sayısı": b_sum}])], ignore_index=True)
        b_df.insert(0, "S.NO", range(1, len(b_df) + 1))
        
        html_b = b_df.to_html(index=False, classes='styled-table')
        # Sola dayama (İkinci sütun için)
        html_b = html_b.replace('<td>', '<td class="left-text">', (len(b_df)*2)).replace('<td class="left-text">', '<td>', len(b_df))
        html_b = html_b.replace('<td>GENEL TOPLAM</td>', '<td class="total-row">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_b}</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("<h3>👨‍🏫 Sorumlu Araştırmacı Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        s_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        s_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        s_df = s_df[~s_df["Sorumlu Araştırmacı"].astype(str).str.contains("Etiketleri|Toplam", na=False)]
        s_df["Dosya Sayısı"] = s_df["Dosya Sayısı"].astype(int)
        
        s_sum = s_df["Dosya Sayısı"].sum()
        s_df = pd.concat([s_df, pd.DataFrame([{"Sorumlu Araştırmacı": "GENEL TOPLAM", "Dosya Sayısı": s_sum}])], ignore_index=True)
        s_df.insert(0, "S.NO", range(1, len(s_df) + 1))
        
        html_s = s_df.to_html(index=False, classes='styled-table')
        html_s = html_s.replace('<td>', '<td class="left-text">', (len(s_df)*2)).replace('<td class="left-text">', '<td>', len(s_df))
        html_s = html_s.replace('<td>GENEL TOPLAM</td>', '<td class="total-row">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_s}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
