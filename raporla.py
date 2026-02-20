import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_all_data():
    try:
        # Hata payını sıfırlamak için sütunları string olarak okuyoruz
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", skiprows=1)
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot", skiprows=1)
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: FB TASARIMI VE KESİN HİZALAMA ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Üst Başlık ve Metriklerin Ortalanması */
    .main-title { text-align: center; color: #FEDD00; font-weight: bold; margin-bottom: 30px; }
    
    /* Metrik Kutuları Tasarımı */
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; color: white !important; }
    [data-testid="stMetricLabel"] { color: #FEDD00 !important; font-weight: bold !important; font-size: 1.1rem !important; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 15px !important; text-align: center !important;
        padding: 15px !important; width: 280px !important; margin: auto !important;
    }
    
    /* Tablo Konteynırı ve Ortalama */
    .centered-table-wrapper { display: flex; justify-content: center; width: 100%; margin: 20px 0; }
    .styled-table { width: auto !important; border-collapse: collapse; color: white; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 12px 20px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px 20px; text-align: center; }
    
    /* SOLA DAYALI SÜTUNLAR (Birim ve Sorumlu için) */
    .left-text { text-align: left !important; min-width: 350px; }
    
    /* TOPLAM SATIRI */
    .total-highlight td { background-color: #FEDD00 !important; color: #000814 !important; font-weight: bold !important; }

    .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; font-size: 1.1rem; }
    .footer { text-align: center; color: #FEDD00; padding: 25px; border-top: 1px solid #FEDD00; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST TARAF: BAŞLIK VE ORTALI METRİKLER ---
st.markdown("<h1 class='main-title'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# 190 ve 4 için kesin ortalama (Boş sütunlarla sıkıştırma)
m_left, m_col1, m_col2, m_right = st.columns([1.5, 1, 1, 1.5])
with m_col1: st.metric("📌 Toplam Başvuru", "190")
with m_col2: st.metric("🗓️ Kurul Sayısı", "4")

# --- GÜNDEM SAYILARI (BAŞLIK VE TABLO ORTALI) ---
st.markdown("<h3 style='text-align: center; color: #FEDD00; margin-top:40px;'>🗓️ 2026 Gündem Sayıları</h3>", unsafe_allow_html=True)
if df_gundem is not None:
    df_g_final = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    df_g_final['Gündem Tarihleri'] = pd.to_datetime(df_g_final['Gündem Tarihleri'], errors='coerce').dt.strftime('%d.%m.%Y')
    
    # HTML Tabloya Çevirme ve Ortalamalı Div içine alma
    html_g = df_g_final.to_html(index=False, classes='styled-table')
    st.markdown(f'<div class="centered-table-wrapper">{html_g}</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.markdown("<h3 style='text-align: center;'>📊 Genel Karar Dağılım Çizelgesi</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        try:
            # En alttaki "TOPLAM" satırını güvenli bulma
            t_row = df_raportor[df_raportor.iloc[:, 1].astype(str).str.contains("TOPLAM", na=False)].iloc[0]
            def get_n(idx): return int(pd.to_numeric(t_row.iloc[idx], errors='coerce') or 0)
            
            ciz_data = {
                "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi", "📊 GENEL TOPLAM"],
                "Onay": [get_n(3), get_n(11), get_n(19), get_n(27), 166],
                "Düzeltme": [get_n(4), get_n(12), get_n(20), get_n(28), 104],
                "KAEK": [get_n(5), get_n(13), get_n(21), get_n(29), 6],
                "Görüş": [get_n(6), get_n(14), get_n(22), get_n(30), 4],
                "Ret": [get_n(7), get_n(15), get_n(23), get_n(31), 4],
                "Kapsam Dışı": [get_n(8), get_n(16), get_n(24), get_n(32), 2],
                "Geri Çekildi": [get_n(9), get_n(17), get_n(25), get_n(33), 0],
                "TOPLAM": [get_n(10), get_n(18), get_n(26), get_n(34), 286]
            }
            df_c = pd.DataFrame(ciz_data)
            html_c = df_c.to_html(index=False, classes='styled-table')
            html_c = html_c.replace('<tr>\n      <td>📊 GENEL TOPLAM</td>', '<tr class="total-highlight">\n      <td>📊 GENEL TOPLAM</td>')
            st.markdown(f'<div class="centered-table-wrapper">{html_c}</div>', unsafe_allow_html=True)
        except: st.warning("Karar çizelgesi verileri şu an hazırlanamıyor.")

with tab2:
    st.markdown("<h3 style='text-align: center;'>👥 Raportör Karar Ayrıntıları</h3>", unsafe_allow_html=True)
    if df_raportor is not None:
        r_list = df_raportor[df_raportor.iloc[:, 1].notna() & (~df_raportor.iloc[:, 1].astype(str).str.contains("Adı Soyadı|TOPLAM", na=False))]
        sec_r = st.selectbox("Analiz edilecek Raportörü Seçin:", r_list.iloc[:, 1].unique())
        r_row = r_list[r_list.iloc[:, 1] == sec_r].iloc[0]
        def v(idx): return int(pd.to_numeric(r_row.iloc[idx], errors='coerce') or 0)

        # Raportör Detay Tablosu
        rd_data = {
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
        df_rd = pd.DataFrame(rd_data)
        html_rd = df_rd.to_html(index=False, classes='styled-table').replace('<td>📊 TOPLAM</td>', '<td style="background-color:#FEDD00; color:#000; font-weight:bold;">📊 TOPLAM</td>')
        st.markdown(f'<div class="centered-table-wrapper">{html_rd}</div>', unsafe_allow_html=True)

        # RAPORTÖR ÖZET METRİKLERİ (3'lü kutu düzeni)
        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("📌 Atanan Toplam Dosya", v(2))
        with c2: st.metric("✅ Karar Verilen Toplam", v(42))
        with c3: st.metric("⏳ Bekleyen Dosya Sayısı", v(2) - v(42))

with tab3:
    st.markdown("<h3 style='text-align: center;'>🏢 Birim Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        b_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        b_df.columns = ["Birim Adı", "Dosya Sayısı"]
        b_df = b_df[~b_df["Birim Adı"].astype(str).str.contains("Etiketleri|Toplam", na=False)]
        b_df["Dosya Sayısı"] = b_df["Dosya Sayısı"].astype(int)
        
        # S.No ve Toplam
        b_sum = b_df["Dosya Sayısı"].sum()
        b_df = pd.concat([b_df, pd.DataFrame([{"Birim Adı": "GENEL TOPLAM", "Dosya Sayısı": b_sum}])], ignore_index=True)
        b_df.insert(0, "S.NO", range(1, len(b_df) + 1))
        
        # HTML manipülasyonu (Birim isimlerini sola daya)
        html_b = b_df.to_html(index=False, classes='styled-table')
        html_b = html_b.replace('<td>', '<td class="left-text">', len(b_df)*2).replace('<td class="left-text">', '<td>', len(b_df))
        html_b = html_b.replace('<td>GENEL TOPLAM</td>', '<td class="total-highlight">GENEL TOPLAM</td>')
        st.markdown(f'<div class="centered-table-wrapper">{html_b}</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("<h3 style='text-align: center;'>👨‍🏫 Sorumlu Araştırmacı Analizi</h3>", unsafe_allow_html=True)
    if df_pivot is not None:
        s_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        s_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        s_df = s_df[~s_df["Sorumlu Araştırmacı"].astype(str).str.contains("Etiketleri|Toplam", na=False)]
        s_df["Dosya Sayısı"] = s_df["Dosya Sayısı"].astype(int)
        
        s_sum = s_df["Dosya Sayısı"].sum()
        s_df = pd.concat([s_df, pd.DataFrame([{"Sorumlu Araştırmacı": "GENEL TOPLAM", "Dosya Sayısı": s_sum}])], ignore_index=True)
        s_df.insert(0, "S.NO", range(1, len(s_df) + 1))
        
        # HTML manipülasyonu (Sorumlu isimlerini sola daya)
        html_s = s_df.to_html(index=False, classes='styled-table')
        html_s = html_s.replace('<td>', '<td class="left-text">', len(s_df)*2).replace('<td class="left-text">', '<td>', len(s_df))
        html_s = html_s.replace('<td>GENEL TOPLAM</td>', '<td class="total-highlight">GENEL TOPLAM</td>')
        st.markdown(f'<div class="centered-table-wrapper">{html_s}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer"><b>Mahsuni TÜRKATAR</b></div>', unsafe_allow_html=True)
