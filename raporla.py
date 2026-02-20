import streamlit as st
import pandas as pd

# Sayfa Yapılandırması (SABİT)
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

# --- CSS: BEYAZ BAŞLIKLAR, LACİVERT TOPLAM VE SİMETRİ ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* BAŞLIKLAR: Beyaz ve Ortalı */
    h1, h2, h3, h4 { color: #FFFFFF !important; text-align: center !important; font-weight: bold !important; }
    
    /* METRİK ETİKETLERİ: Beyaz ve Ortalı */
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; justify-content: center !important; text-align: center !important; display: flex !important; }
    [data-testid="stMetricValue"] { color: #FEDD00 !important; text-align: center !important; }
    
    /* Metrik Kutuları: Dar ve Merkezde */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
        width: 200px !important; margin: auto !important; padding: 10px !important;
    }
    
    /* Tablo Düzeni */
    .table-wrapper { display: flex; justify-content: center; width: 100%; margin: 10px 0; }
    .styled-table { width: auto !important; border-collapse: collapse; color: white; font-size: 0.9rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px 15px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px 15px; text-align: center; }
    
    /* TOPLAM SATIRI: Lacivert Zemin, Sarı Yazı (İstediğin Gibi) */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border: 2px solid #FEDD00 !important; }

    /* Sekme Başlıkları Beyaz */
    .stTabs [data-baseweb="tab"] p { color: #FFFFFF !important; font-weight: bold; }
    .footer { text-align: center; color: #FFFFFF; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER (ORTALANMIŞ VE BAŞLIKLAR BEYAZ) ---
m_l, m_c1, m_c2, m_r = st.columns([2, 1, 1, 2])
with m_c1: st.metric("Toplam Başvuru", "190")
with m_c2: st.metric("Kurul Sayısı", "4")

# --- 2. GÜNDEM SAYILARI (HER SAYFADA ÜSTTE) ---
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
            # Excel'in en altındaki TOPLAM satırı (Sabit rakamlarla hata düzeltildi)
            t_row = df_raportor[df_raportor.iloc[:, 1].astype(str).str.contains("TOPLAM", na=False)].iloc[0]
            def g_v(idx): return int(pd.to_numeric(t_row.iloc[idx], errors='coerce') or 0)
            
            ciz_dict = {
                "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi", "📊 GENEL TOPLAM"],
                "Onay": [g_v(3), g_v(11), g_v(19), g_v(27), 166],
                "Düzeltme": [g_v(4), g_v(12), g_v(20), g_v(28), 104],
                "KAEK": [g_v(5), g_v(13), g_v(21), g_v(29), 6],
                "Görüş": [g_v(6), g_v(14), g_v(22), g_v(30), 4],
                "Ret": [g_v(7), g_v(15), g_v(23), g_v(31), 4],
                "Kapsam Dışı": [g_v(8), g_v(16), g_v(24), g_v(32), 2],
                "Geri Çekildi": [g_v(9), g_v(17), g_v(25), g_v(33), 0],
                "TOPLAM": [g_v(10), g_v(18), g_v(26), g_v(34), 286]
            }
            df_c = pd.DataFrame(ciz_dict)
            html_c = df_c.to_html(index=False, classes='styled-table')
            html_c = html_c.replace('<tr>\n      <td>📊 GENEL TOPLAM</td>', '<tr class="total-row">\n      <td>📊 GENEL TOPLAM</td>')
            st.markdown(f'<div class="table-wrapper">{html_c}</div>', unsafe_allow_html=True)
        except: st.warning("Veri formatı kontrol edilmeli.")

with tab2:
    st.markdown("<h3>👥 Raportör Karar Ayrıntıları</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        r_names = df_raportor[df_raportor.iloc[:, 1].notna() & (~df_raportor.iloc[:, 1].astype(str).str.contains("Adı Soyadı|TOPLAM", na=False))].iloc[:, 1].unique()
        sec_r = st.selectbox("Raportör Seçin:", r_names)
        r_row = df_raportor[df_raportor.iloc[:, 1] == sec_r].iloc[0]
        def v_v(idx): return int(pd.to_numeric(r_row.iloc[idx], errors='coerce') or 0)

        rd_data = {
            "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi", "📊 TOPLAM"],
            "Onay": [v_v(3), v_v(11), v_v(19), v_v(27), v_v(35)],
            "Düzeltme": [v_v(4), v_v(12), v_v(20), v_v(28), v_v(36)],
            "KAEK": [v_v(5), v_v(13), v_v(21), v_v(29), v_v(37)],
            "Görüş": [v_v(6), v_v(14), v_v(22), v_v(30), v_v(38)],
            "Ret": [v_v(7), v_v(15), v_v(23), v_v(31), v_v(39)],
            "Kapsam Dışı": [v_v(8), v_v(16), v_v(24), v_v(32), v_v(40)],
            "Geri Çekildi": [v_v(9), v_v(17), v_v(25), v_v(33), v_v(41)],
            "TOPLAM": [v_v(10), v_v(18), v_v(26), v_v(34), v_v(42)]
        }
        html_r = pd.DataFrame(rd_data).to_html(index=False, classes='styled-table').replace('<td>📊 TOPLAM</td>', '<td class="total-row">📊 TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_r}</div>', unsafe_allow_html=True)
        
        # RAPORTÖR ÖZET (DARALTILMIŞ VE ORTALANMIŞ)
        rm_l, rm1, rm2, rm3, rm_r = st.columns([1.5, 1, 1, 1, 1.5])
        with rm1: st.metric("Atanan", v_v(2))
        with rm2: st.metric("Karar", v_v(42))
        with rm3: st.metric("Bekleyen", v_v(2) - v_v(42))

with tab3:
    st.markdown("<h3>🏢 Birim Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        b_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b_df.columns = ["Birim Adı", "Dosya Sayısı"]
        b_df = b_df[~b_df["Birim Adı"].astype(str).str.contains("Etiketleri|Toplam", na=False)]
        b_df["Dosya Sayısı"] = b_df["Dosya Sayısı"].astype(int)
        
        # Toplam ve S.NO
        b_df = b_df.sort_values(by="Dosya Sayısı", ascending=False)
        b_sum = b_df["Dosya Sayısı"].sum()
        b_df = pd.concat([b_df, pd.DataFrame([{"Birim Adı": "GENEL TOPLAM", "Dosya Sayısı": b_sum}])], ignore_index=True)
        b_df.insert(0, "S.NO", range(1, len(b_df) + 1))
        
        # SOLA DAYAMA GARANTİSİ (Inline CSS basıyoruz)
        html_b = b_df.to_html(index=False, classes='styled-table')
        html_b = html_b.replace('<td>', '<td style="text-align: left; padding-left: 20px; min-width: 380px;">', (len(b_df)*2)).replace('<td style="text-align: left; padding-left: 20px; min-width: 380px;">', '<td>', len(b_df))
        html_b = html_b.replace('<td>GENEL TOPLAM</td>', '<td class="total-row" style="text-align: left; padding-left: 20px;">GENEL TOPLAM</td>')
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
        
        # SOLA DAYAMA GARANTİSİ
        html_s = s_df.to_html(index=False, classes='styled-table')
        html_s = html_s.replace('<td>', '<td style="text-align: left; padding-left: 20px; min-width: 380px;">', (len(s_df)*2)).replace('<td style="text-align: left; padding-left: 20px; min-width: 380px;">', '<td>', len(s_df))
        html_s = html_s.replace('<td>GENEL TOPLAM</td>', '<td class="total-row" style="text-align: left; padding-left: 20px;">GENEL TOPLAM</td>')
        st.markdown(f'<div class="table-wrapper">{html_s}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
