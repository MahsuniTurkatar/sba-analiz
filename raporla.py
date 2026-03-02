import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- VERİ YÜKLEME ---
EXCEL_FILE = "2026_SBA.xlsx"

@st.cache_data
def load_all_data():
    try:
        # Başvuru sayfası
        df_basvuru = pd.read_excel(EXCEL_FILE, sheet_name="Başvuru", header=0)
        df_basvuru = df_basvuru[
            df_basvuru["SBA NUMARASI"].notna() &
            df_basvuru["SBA NUMARASI"].astype(str).str.startswith("SBA")
        ].copy()

        # Sayılar sayfası (2. satırdan başlık)
        df_sayilar = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", header=2)
        df_sayilar.columns = ["S.NO", "Gündem Tarihleri", "Başvuru", "Düzeltme", "Dilekçe", "Toplam"]
        df_sayilar = df_sayilar[df_sayilar["Gündem Tarihleri"].notna()].copy()

        # Toplam satırı
        df_sayilar_raw = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", header=None)
        toplam_satir = df_sayilar_raw[df_sayilar_raw[0] == "TOPLAM"].iloc[0]

        # Üye_1 sayfası
        df_uye = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", header=0)
        df_uye.columns = [str(c).strip() for c in df_uye.columns]
        df_uye = df_uye[df_uye["Adı Soyadı"].notna()].copy()

        # Pivot sayfası
        df_pivot = pd.read_excel(EXCEL_FILE, sheet_name="Pivot", header=0)

        return df_basvuru, df_sayilar, toplam_satir, df_uye, df_pivot

    except Exception as e:
        st.error(f"Excel Okuma Hatası: {e}")
        return None, None, None, None, None

df_basvuru, df_sayilar, toplam_satir, df_uye, df_pivot = load_all_data()

# --- DİNAMİK SAYILAR ---
def hesapla_gostergeler(df_b, toplam):
    toplam_basvuru = int(toplam[2]) if toplam is not None else 0
    nitelik = df_b["NİTELİĞİ"].value_counts()
    bireysel   = int(nitelik.get("Bireysel Araştırma", 0))
    uzmanlik   = int(nitelik.get("Uzmanlık Tezi", 0))
    yuksek     = int(nitelik.get("Yüksek Lisans Tezi", 0))
    doktora    = int(nitelik.get("Doktora Tezi", 0))
    return toplam_basvuru, bireysel, uzmanlik, yuksek, doktora

toplam_b, bireysel, uzmanlik, yuksek, doktora = (0,0,0,0,0)
if df_basvuru is not None:
    toplam_b, bireysel, uzmanlik, yuksek, doktora = hesapla_gostergeler(df_basvuru, toplam_satir)

# Kurul sayısı = dolu gündem satırı sayısı
kurul_sayisi = len(df_sayilar) if df_sayilar is not None else 0

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    .centered-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 2.2rem; margin: 30px 0; }
    .section-title { color: #ffffff !important; text-align: center !important; font-weight: bold !important; font-size: 1.8rem; margin: 25px 0; display: block; }

    .metric-row { display: flex; justify-content: center; gap: 20px; margin-bottom: 25px; flex-wrap: wrap; }
    .main-box { background-color: #001d3d; border: 2px solid #FEDD00; border-radius: 12px; padding: 15px 40px; text-align: center; min-width: 180px; position: relative; }
    .main-box::before { content: "📌"; position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: #001d3d; padding: 0 10px; font-size: 1.2rem; }
    .kurul-box::before { content: "📋"; }

    .main-val { color: #FEDD00; font-size: 3rem; font-weight: bold; display: block; line-height: 1; }
    .main-lab { color: #ffffff; font-size: 1rem; display: block; margin-top: 5px; }

    .sub-box { background-color: #001d3d; border: 1px solid #FEDD00; border-radius: 8px; padding: 10px; text-align: center; min-width: 140px; }
    .sub-val { color: #FEDD00; font-size: 1.5rem; font-weight: bold; display: block; }
    .sub-lab { color: #ffffff; font-size: 0.8rem; display: block; }

    .table-wrapper { display: flex; justify-content: center; width: 100%; overflow-x: auto; padding: 10px; }
    .styled-table { border-collapse: collapse; color: #ffffff; font-size: 0.85rem; width: auto !important; margin: auto; }
    .styled-table th { background-color: #001d3d !important; color: #FEDD00 !important; border: 1px solid #FEDD00; padding: 10px 15px; text-align: center !important; white-space: nowrap; }
    .styled-table td { border: 1px solid #FEDD00; padding: 8px 12px; text-align: center !important; background-color: #001d3d; color: white !important; white-space: nowrap; }

    .wide-table-wrapper { width: 100%; overflow-x: scroll; border: 1px solid #FEDD00; border-radius: 8px; }

    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-weight: bold !important; font-size: 1.1rem; }
    .stTabs [aria-selected="true"] { color: #FEDD00 !important; border-bottom: 3px solid #FEDD00 !important; }

    .footer { text-align: center; color: #FEDD00; padding: 20px; border-top: 1px solid #FEDD00; margin-top: 40px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def clean_num(val):
    if pd.isna(val) or val == "" or str(val).strip() in ["0", "0.0", "nan"]: return ""
    try: return str(int(float(val)))
    except: return str(val)

def df_to_html(df):
    return df.map(clean_num).to_html(index=False, classes="styled-table")

# --- 1. GÖSTERGELER ---
st.markdown('<div class="centered-title">Sağlık Bilimleri Araştırma Etik Kurulu Başvuruları</div>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="metric-row">
        <div class="main-box kurul-box"><span class="main-val">{kurul_sayisi}</span><span class="main-lab">Kurul Sayısı</span></div>
        <div class="main-box"><span class="main-val">{toplam_b}</span><span class="main-lab">Toplam Başvuru</span></div>
    </div>
    <div class="metric-row">
        <div class="sub-box"><span class="sub-val">{bireysel}</span><span class="sub-lab">Bireysel Araştırma</span></div>
        <div class="sub-box"><span class="sub-val">{uzmanlik}</span><span class="sub-lab">Uzmanlık Tezi</span></div>
        <div class="sub-box"><span class="sub-val">{yuksek}</span><span class="sub-lab">Y. Lisans Tezi</span></div>
        <div class="sub-box"><span class="sub-val">{doktora}</span><span class="sub-lab">Doktora Tezi</span></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. GÜNDEM SAYILARI ---
st.markdown('<div class="section-title">🗓️ 2026 Gündem Sayıları</div>', unsafe_allow_html=True)

if df_sayilar is not None:
    dg = df_sayilar.copy()
    dg["Gündem Tarihleri"] = pd.to_datetime(dg["Gündem Tarihleri"], errors="coerce").dt.strftime("%d.%m.%Y")

    # Toplam satırı ekle
    t_row = pd.DataFrame([{
        "S.NO": "TOPLAM",
        "Gündem Tarihleri": "",
        "Başvuru": int(toplam_satir[2]),
        "Düzeltme": int(toplam_satir[3]),
        "Dilekçe": int(toplam_satir[4]),
        "Toplam": int(toplam_satir[5])
    }])

    tablo = pd.concat([dg, t_row], ignore_index=True)
    st.markdown('<div class="table-wrapper">' + df_to_html(tablo) + '</div>', unsafe_allow_html=True)

# --- 3. ANALİZLER ---
st.markdown('<div class="centered-title">📊 ANALİZLER</div>', unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Karar Çizelgesi", "👥 Raportör Analizi", "🏢 Birim Analizi", "👨‍🏫 Araştırmacı Analizi"])

with tab1:
    st.markdown('<div class="section-title">📄 Genel Karar Çizelgesi</div>', unsafe_allow_html=True)
    if df_uye is not None:
        sayi_sutunlar = df_uye.select_dtypes(include="number").columns.tolist()
        toplam_uye_satir = {col: "" for col in df_uye.columns}
        toplam_uye_satir["S.No"] = "TOPLAM"
        toplam_uye_satir["Adı Soyadı"] = ""
        for col in sayi_sutunlar:
            toplam_uye_satir[col] = int(df_uye[col].sum())
        df_uye_toplam = pd.concat([df_uye, pd.DataFrame([toplam_uye_satir])], ignore_index=True)
        st.markdown('<div class="wide-table-wrapper">' + df_to_html(df_uye_toplam) + '</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">👥 Raportör Karar Ayrıntıları</div>', unsafe_allow_html=True)
    if df_uye is not None:
        r_list = df_uye["Adı Soyadı"].dropna().unique().tolist()
        _, col_mid, _ = st.columns([1, 2, 1])
        with col_mid:
            sec_r = st.selectbox("Raportör Seçin:", r_list)
        r_row = df_uye[df_uye["Adı Soyadı"] == sec_r].iloc[0]

        ik_detay = pd.DataFrame({
            "Karar Türü": ["📌 Toplam Dosya", "✅ Onay", "📝 Düzeltme", "🏛️ KAEK",
                           "💬 Görüş", "❌ Ret", "🚫 Kapsam Dışı", "📤 Geri Çekildi",
                           "📊 KARAR VERİLEN", "⏳ BEKLEYEN"],
            "Sayı": [
                clean_num(r_row["Dosya Sayısı"]),
                clean_num(r_row["Onay Toplam"]),
                clean_num(r_row["Düzeltme Toplam"]),
                clean_num(r_row["KAEK  Toplam"]),
                clean_num(r_row["Görüş Toplam"]),
                clean_num(r_row["Ret Toplam"]),
                clean_num(r_row["Kapsam Dışı Toplam"]),
                clean_num(r_row["Geri Çekildi Toplam"]),
                clean_num(r_row["GENEL TOPLAM"]),
                clean_num(r_row["BEKLEYEN DOSYA SAYISI"]),
            ]
        })
        st.markdown('<div class="table-wrapper">' + ik_detay.to_html(index=False, classes="styled-table") + '</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-title">🏢 Birim Analizi</div>', unsafe_allow_html=True)
    if df_pivot is not None:
        birim_df = df_pivot[["Satır Etiketleri", "Say BİRİMİ"]].dropna().copy()
        birim_df.columns = ["Birim Adı", "Dosya Sayısı"]
        birim_df = birim_df[birim_df["Birim Adı"] != "Satır Etiketleri"]
        st.markdown('<div class="table-wrapper">' + df_to_html(birim_df) + '</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-title">👨‍🏫 Sorumlu Araştırmacı Analizi</div>', unsafe_allow_html=True)
    if df_pivot is not None:
        sorumlu_df = df_pivot[["Satır Etiketleri.1", "Say SORUMLUSU"]].dropna().copy()
        sorumlu_df.columns = ["Sorumlu Araştırmacı", "Dosya Sayısı"]
        sorumlu_df = sorumlu_df[sorumlu_df["Sorumlu Araştırmacı"] != "Satır Etiketleri"]
        st.markdown('<div class="table-wrapper">' + df_to_html(sorumlu_df) + '</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Mahsuni TÜRKATAR</div>', unsafe_allow_html=True)
