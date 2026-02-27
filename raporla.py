import streamlit as st
import pandas as pd

# Sayfa Yapılandırması (SABİT)
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx" 

@st.cache_data
def load_all_data():
    try:
        # Sayıları 2. satırdan, Raportörü (Üye_1) 1. satırdan alıyoruz
        df_g = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", skiprows=2)
        df_r = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1") 
        df_p = pd.read_excel(EXCEL_FILE, sheet_name="Pivot") 
        
        # Sütun temizliği (Gizli boşlukları siler)
        df_r.columns = [str(c).strip() for c in df_r.columns]
        return df_g, df_r, df_p
    except:
        return None, None, None

df_gundem, df_raportor, df_pivot = load_all_data()

# --- CSS: FB TASARIMI VE İĞNELENMİŞ MİZANPAJ ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .main-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 2.2rem; margin-bottom: 25px; }
    
    /* ÜST KUTULAR (SAYI ÜSTTE) */
    .metric-row { display: flex; justify-content: center; gap: 20px; margin-bottom: 15px; }
    .main-box { background-color: #001d3d; border: 2px solid #FEDD00; border-radius: 12px; padding: 15px 45px; text-align: center; min-width: 200px; }
    .main-val { color: #FEDD00; font-size: 3.2rem; font-weight: bold; display: block; line-height: 1; }
    .main-lab { color: #ffffff; font-size: 1.1rem; display: block; margin-top: 8px; }

    .sub-box { background-color: #001d3d; border: 1px solid #FEDD00; border-radius: 8px; padding: 12px; text-align: center; min-width: 155px; }
    .sub-val { color: #FEDD00; font-size: 1.7rem; font-weight: bold; display: block; }
    .sub-lab { color: #ffffff; font-size: 0.85rem; display: block; }

    /* TABLOLAR: LACİVERT ARKA PLAN, SARI ÇERÇEVE */
    .table-container { display: flex; flex-direction: column; align-items: center; margin: 20px 0; width: 100%; overflow-x: auto; }
    .section-head { color: #FEDD00 !important; font-size: 1.5rem; font-weight: bold; margin-bottom: 10px; width: 100%; text-align: left; padding-left: 5%; }
    
    .styled-table { width: 95% !important; border-collapse: collapse; color: #ffffff; font-size: 0.85rem; }
    .styled-table th { background-color: #001d3d !important; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px; text-align: center !important; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px; text-align: center !important; background-color: #001d3d; color: white !important; }
    
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold !important; }
    .stTabs [aria-selected="true"] { color: #FEDD00 !important; border-bottom-color: #FEDD00 !important; }
    
    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 40px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def clean_num(val):
    if pd.isna(val) or val == "" or val == 0 or val == "0" or str(val).strip() == "0.0": return ""
    try:
        # Eğer veri zaten bir sayı ise float'a çevirip int yap
        return str(int(float(val)))
    except:
        return str(val)

# --- 1. ÜST PANEL (225 SAYISI İLE GÜNCELLENDİ) ---
st.markdown('<div class="main-title">Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="metric-row">
        <div class="main-box"><span class="main-val">5</span><span class="main-lab">Kurul Sayısı</span></div>
        <div class="main-box"><span class="main-val">225</span><span class="main-lab">Toplam Başvuru</span></div>
    </div>
    <div class="metric-row">
        <div class="sub-box"><span class="sub-val">135</span><span class="sub-lab">Bireysel Araştırma</span></div>
        <div class="sub-box"><span class="sub-val">41</span><span class="sub-lab">Uzmanlık Tezi</span></div>
        <div class="sub-box"><span class="sub-val">12</span><span class="sub-lab">Y. Lisans Tezi</span></div>
        <div class="sub-box"><span class="sub-val">18</span><span class="sub-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. GÜNDEM SAYILARI ---
if df_gundem is not None:
    st.markdown('<div class="table-container"><div class="section-head">🗓️ 2026 Gündem Sayıları</div>', unsafe_allow_html=True)
    dg = df_gundem[df_gundem['Gündem Tarihleri'].notna()].copy()
    dg['Gündem Tarihleri'] = pd.to_datetime(dg['Gündem Tarihleri'], errors='coerce').dt.strftime('%d.%m.%Y')
    
    # Toplam satırı (225 ve yeni kararlar için güncellenmiş varsayılan değerler)
    t_row = pd.DataFrame([{"S.NO": "TOPLAM", "Gündem Tarihleri": "", "Başvuru": 225, "Düzeltme": 68, "Dilekçe": 45, "Toplam": 338}])
    dg_render = pd.concat([dg, t_row], ignore_index=True).applymap(clean_num)
    
    st.markdown(dg_render.to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

# --- 3. ANALİZLER ---
st.markdown("<h2 style='text-align: center; color: white; margin-top:30px;'>📊 ANALİZLER</h2>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Sorumlu Araştırmacı Analizi"])

with tab1:
    st.write("#### 📋 Genel Karar Çizelgesi (Üye_1 Sayfası)")
    if df_raportor is not None:
        # Excel'deki yeni yatay başlıkları doğrudan kullanıyoruz
        st.markdown('<div class="table-container">' + df_raportor.applymap(clean_num).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tab2:
    st.write("#### 👥 Raportör Karar Ayrıntıları")
    if df_raportor is not None:
        # Adı Soyadı sütunu üzerinden seçim (AKARSU hocamız dahil tüm liste)
        r_list = df_raportor.iloc[:, 1].dropna().unique().tolist()
        sec_r = st.selectbox("Analiz edilecek raportörü seçiniz:", r_list)
        
        r_row = df_raportor[df_raportor.iloc[:, 1] == sec_r].iloc[0]
        
        # Seçilen raportörün özet tablosu
        # Not: Sütun indexleri Excel yapına göre değişebilir, eğer hata verirse sütun isimleriyle çağırırız.
        dosya = int(pd.to_numeric(r_row.iloc[2], errors='coerce') or 0)
        toplam_karar = int(pd.to_numeric(r_row.iloc[-1], errors='coerce') or 0)
        
        detay = {
            "Kategori": ["Atanan Toplam Dosya", "Karar Verilen Toplam", "Bekleyen Dosya"],
            "Sayı": [dosya, toplam_karar, (dosya - toplam_karar)]
        }
        st.markdown('<div class="table-container">' + pd.DataFrame(detay).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tab3:
    st.write("#### 🏢 Birim Analizi")
    if df_pivot is not None:
        birim_df = df_pivot.iloc[:, [0, 1]].dropna().copy()
        birim_df.columns = ["Birim Adı", "Dosya Sayısı"]
        st.markdown('<div class="table-container">' + birim_df.applymap(clean_num).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

with tab4:
    st.write("#### 👨‍🏫 Sorumlu Araştırmacı Analizi")
    if df_pivot is not None:
        sorumlu_df = df_pivot.iloc[:, [3, 4]].dropna().copy()
        sorumlu_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        st.markdown('<div class="table-container">' + sorumlu_df.applymap(clean_num).to_html(index=False, classes='styled-table') + '</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
