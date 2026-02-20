import streamlit as st
import pandas as pd
import os

# Sayfa Yapılandırması (SABİT)
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_all_data():
    try:
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", skiprows=1)
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot") 
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: FB TASARIMI (KUTSAL EMANET) ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    div[data-testid="stMetric"] {
        background-color: #001d3d !important; border: 2px solid #FEDD00 !important;
        border-radius: 12px !important; text-align: center !important;
    }
    .nitelik-container { display: flex; justify-content: space-between; gap: 10px; margin: 20px 0; }
    .nitelik-card {
        flex: 1; background-color: #001d3d; border: 1px solid #FEDD00;
        border-radius: 8px; padding: 15px; text-align: center;
    }
    .n-val { color: #FEDD00; font-size: 1.5rem; font-weight: bold; display: block; }
    .n-lab { color: #ffffff; font-size: 0.9rem; }
    .table-container { display: flex; justify-content: center; margin: 20px 0; }
    .styled-table { width: 100% !important; border-collapse: collapse; color: white; margin-bottom: 20px; }
    .styled-table th { background-color: #001d3d; color: #FEDD00; border: 1px solid #FEDD00; padding: 10px; text-align: center; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center; }
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #FEDD00 !important; }
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</h1>", unsafe_allow_html=True)

# --- ÜST METRİKLER VE GÜNDEM (DEĞİŞMEDİ) ---
c1, c2 = st.columns(2)
c1.metric("📌 Toplam Başvuru", "190")
c2.metric("🗓️ Kurul Sayısı", "4")

if df_gundem is not None:
    df_g_final = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    df_g_final['Gündem Tarihleri'] = pd.to_datetime(df_g_final['Gündem Tarihleri'], errors='coerce').dt.strftime('%d.%m.%Y')
    for col in ['Başvuru', 'Düzeltme', 'Dilekçe', 'Toplam']:
        if col in df_g_final.columns:
            df_g_final[col] = pd.to_numeric(df_g_final[col], errors='coerce').fillna(0).astype(int)
    st.write("### 📅 2026 Gündem Sayıları")
    st.markdown('<div class="table-container">' + df_g_final.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

# --- SEKMELER ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    img_path = "genel_tablo_ekran_goruntusu.png"
    if os.path.exists(img_path): st.image(img_path, use_container_width=True)

with tab2:
    st.write("### 👥 Raportör Detaylı Karar Dağılımı")
    if df_raportor is not None:
        r_clean = df_raportor[df_raportor.iloc[:, 1].notna() & (df_raportor.iloc[:, 1] != "Adı Soyadı")].copy()
        r_list = [x for x in r_clean.iloc[:, 1].unique().tolist() if "TOPLAM" not in str(x)]
        sec_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = r_clean[r_clean.iloc[:, 1] == sec_r].iloc[0]

        # Sayıları temiz çekme (Sütun indisleri 1. görseldeki Excel sırasına göredir)
        # Bireysel (3-9), Y. Lisans (11-17), Doktora (19-25), Uzmanlık (27-33)
        def get_val(idx): return int(pd.to_numeric(r_row.iloc[idx], errors='coerce') or 0)

        # Branş Bazlı Tablo (Senin istediğin detaylı görünüm)
        brans_data = {
            "Başvuru Türü": ["📄 Bireysel Araştırma", "🎓 Yüksek Lisans Tezi", "🔬 Doktora Tezi", "🏥 Uzmanlık Tezi"],
            "Onay": [get_val(3), get_val(11), get_val(19), get_val(27)],
            "Düzeltme": [get_val(4), get_val(12), get_val(20), get_val(28)],
            "KAEK": [get_val(5), get_val(13), get_val(21), get_val(29)],
            "Görüş": [get_val(6), get_val(14), get_val(22), get_val(30)],
            "Ret": [get_val(7), get_val(15), get_val(23), get_val(31)],
            "Kapsam Dışı": [get_val(8), get_val(16), get_val(24), get_val(32)],
            "Geri Çekildi": [get_val(9), get_val(17), get_val(25), get_val(33)],
            "TOPLAM": [get_val(10), get_val(18), get_val(26), get_val(34)]
        }
        
        st.markdown('<div class="table-container">' + pd.DataFrame(brans_data).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

        # --- ALT ÖZET KARTLARI ---
        atanan = get_val(2)
        karar_toplam = get_val(42) # GENEL TOPLAM sütunu
        bekleyen = atanan - karar_toplam

        st.markdown(f"""
            <div class="nitelik-container">
                <div class="nitelik-card"><span class="n-val">{atanan}</span><span class="n-lab">📌 Atanan Toplam Dosya</span></div>
                <div class="nitelik-card"><span class="n-val">{karar_toplam}</span><span class="n-lab">✅ Karar Verilen Toplam</span></div>
                <div class="nitelik-card"><span class="n-val">{bekleyen}</span><span class="n-lab">⏳ Bekleyen Dosya Sayısı</span></div>
            </div>
        """, unsafe_allow_html=True)

with tab3: # (SABİT)
    st.write("#### 🏢 Birim Analizi")
    if df_pivot is not None:
        birim_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        birim_df.columns = ["Birim Adı", "Dosya Sayısı"]
        birim_df["Dosya Sayısı"] = birim_df["Dosya Sayısı"].astype(int)
        st.table(birim_df)

with tab4: # (SABİT)
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Analizi")
    if df_pivot is not None:
        sorumlu_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        sorumlu_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        sorumlu_df["Dosya Sayısı"] = sorumlu_df["Dosya Sayısı"].astype(int)
        st.table(sorumlu_df)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
