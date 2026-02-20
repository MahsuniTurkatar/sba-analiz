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
    except Exception as e:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: ORTALAMA VE FB TASARIMI ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Metrikleri ve Başlıkları Ortalama */
    .centered-header { text-align: center; color: #FEDD00 !important; margin-bottom: 20px; }
    
    /* Metrik Kutuları Ayarı */
    [data-testid="stMetricValue"] { font-size: 2rem !important; color: white !important; }
    [data-testid="stMetricLabel"] { color: #FEDD00 !important; font-weight: bold !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
        padding: 10px 30px !important; width: 220px !important;
    }
    
    /* Tablo Konteynırı ve Tasarımı */
    .table-container { display: flex; flex-direction: column; align-items: center; margin: 20px 0; }
    .styled-table { width: auto !important; border-collapse: collapse; color: white; font-size: 0.9rem; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 10px 15px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 6px 12px; text-align: center; }
    
    /* TOPLAM SATIRI: Lacivert Arka Plan, Sarı Yazı */
    .total-row td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; border: 2px solid #FEDD00 !important; }
    .sub-total td { background-color: #001d3d !important; color: #FEDD00 !important; font-weight: bold !important; }

    .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    
    /* Metrik sütunlarını ortalamak için boşluk ayarı */
    .metric-row { display: flex; justify-content: center; gap: 50px; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='centered-header'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- 1. METRİKLER (ORTALANMIŞ) ---
# Sütunları kullanarak metrikleri merkeze topluyoruz
m_left, m_col1, m_col2, m_right = st.columns([2, 1, 1, 2])
with m_col1: st.metric("📌 Toplam Başvuru", "190")
with m_col2: st.metric("🗓️ Kurul Sayısı", "4")

# --- 2. GÜNDEM SAYILARI (BAŞLIK VE TABLO ORTALI) ---
if df_gundem is not None:
    df_g_final = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    df_g_final['Gündem Tarihleri'] = pd.to_datetime(df_g_final['Gündem Tarihleri'], errors='coerce').dt.strftime('%d.%m.%Y')
    for col in ['Başvuru', 'Düzeltme', 'Dilekçe', 'Toplam']:
        if col in df_g_final.columns:
            df_g_final[col] = pd.to_numeric(df_g_final[col], errors='coerce').fillna(0).astype(int)
    
    st.markdown("<h3 style='text-align: center;'>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
    st.markdown('<div class="table-container">' + df_g_final.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.markdown("<h3 style='text-align: center;'>📊 Genel Karar Dağılım Çizelgesi</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        try:
            # HATA DÜZELTME: TOPLAM satırını güvenli bulma
            t_idx = df_raportor[df_raportor.iloc[:, 1].astype(str).str.contains("TOPLAM", na=False)].index
            if not t_idx.empty:
                total_row = df_raportor.loc[t_idx[0]]
                def gv(idx): return int(pd.to_numeric(total_row.iloc[idx], errors='coerce') or 0)

                ciz_data = {
                    "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi", "📊 GENEL TOPLAM"],
                    "Onay": [gv(3), gv(11), gv(19), gv(27), 166],
                    "Düzeltme": [gv(4), gv(12), gv(20), gv(28), 104],
                    "KAEK": [gv(5), gv(13), gv(21), gv(29), 6],
                    "Görüş": [gv(6), gv(14), gv(22), gv(30), 4],
                    "Ret": [gv(7), gv(15), gv(23), gv(31), 4],
                    "Kapsam Dışı": [gv(8), gv(16), gv(24), gv(32), 2],
                    "Geri Çekildi": [gv(9), gv(17), gv(25), gv(33), 0],
                    "TOPLAM": [gv(10), gv(18), gv(26), gv(34), 286]
                }
                df_c = pd.DataFrame(ciz_data)
                html_c = df_c.to_html(index=False, classes='styled-table')
                html_c = html_c.replace('<tr>\n      <td>📊 GENEL TOPLAM</td>', '<tr class="total-row">\n      <td>📊 GENEL TOPLAM</td>')
                st.markdown('<div class="table-container">' + html_c + '</div>', unsafe_allow_html=True)
        except: st.error("Karar çizelgesi verisi yüklenemedi.")

with tab2:
    st.markdown("<h3 style='text-align: center;'>👥 Raportör Karar Ayrıntıları</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        r_list = df_raportor[df_raportor.iloc[:, 1].notna() & (~df_raportor.iloc[:, 1].astype(str).str.contains("Adı Soyadı|TOPLAM", na=False))]
        sec_r = st.selectbox("Raportör Seçin:", r_list.iloc[:, 1].unique())
        r_row = r_list[r_list.iloc[:, 1] == sec_r].iloc[0]

        def get_v(idx): return int(pd.to_numeric(r_row.iloc[idx], errors='coerce') or 0)
        
        br_data = {
            "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi"],
            "Onay": [get_v(3), get_v(11), get_v(19), get_v(27)],
            "Düzeltme": [get_v(4), get_v(12), get_v(20), get_v(28)],
            "KAEK": [get_v(5), get_v(13), get_v(21), get_v(29)],
            "Görüş": [get_v(6), get_v(14), get_v(22), get_v(30)],
            "Ret": [get_v(7), get_v(15), get_v(23), get_v(31)],
            "Kapsam Dışı": [get_v(8), get_v(16), get_v(24), get_v(32)],
            "Geri Çekildi": [get_v(9), get_v(17), get_v(25), get_v(33)],
            "TOPLAM": [get_v(10), get_v(18), get_v(26), get_v(34)]
        }
        df_br = pd.DataFrame(br_data)
        t_row = {"Başvuru Türü": "📊 TOPLAM"}
        for col in df_br.columns[1:]: t_row[col] = df_br[col].sum()
        df_br = pd.concat([df_br, pd.DataFrame([t_row])], ignore_index=True)

        html_r = df_br.to_html(index=False, classes='styled-table')
        html_r = html_r.replace('<tr>\n      <td>📊 TOPLAM</td>', '<tr class="total-row">\n      <td>📊 TOPLAM</td>')
        st.markdown('<div class="table-container">' + html_r + '</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("<h3 style='text-align: center;'>🏢 Birim Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        b_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b_df.columns = ["Birim Adı", "Dosya Sayısı"]
        b_df = b_df[~b_df["Birim Adı"].astype(str).str.contains("Etiketleri|Toplam", na=False)]
        b_df["Dosya Sayısı"] = b_df["Dosya Sayısı"].astype(int)
        b_total = pd.DataFrame([{"Birim Adı": "GENEL TOPLAM", "Dosya Sayısı": b_df["Dosya Sayısı"].sum()}])
        b_df = pd.concat([b_df, b_total], ignore_index=True)
        b_df.insert(0, "S.NO", range(1, len(b_df) + 1))
        
        html_b = b_df.to_html(index=False, classes='styled-table')
        html_b = html_b.replace('<td>GENEL TOPLAM</td>', '<td class="sub-total">GENEL TOPLAM</td>')
        st.markdown('<div class="table-container">' + html_b + '</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("<h3 style='text-align: center;'>👨‍🏫 Sorumlu Araştırmacı Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        s_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        s_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        s_df = s_df[~s_df["Sorumlu Araştırmacı"].astype(str).str.contains("Etiketleri|Toplam", na=False)]
        s_df["Dosya Sayısı"] = s_df["Dosya Sayısı"].astype(int)
        s_total = pd.DataFrame([{"Sorumlu Araştırmacı": "GENEL TOPLAM", "Dosya Sayısı": s_df["Dosya Sayısı"].sum()}])
        s_df = pd.concat([s_df, s_total], ignore_index=True)
        s_df.insert(0, "S.NO", range(1, len(s_df) + 1))
        
        html_s = s_df.to_html(index=False, classes='styled-table')
        html_s = html_s.replace('<td>GENEL TOPLAM</td>', '<td class="sub-total">GENEL TOPLAM</td>')
        st.markdown('<div class="table-container">' + html_s + '</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
