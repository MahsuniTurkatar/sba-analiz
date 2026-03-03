import streamlit as st
import pandas as pd

st.set_page_config(page_title="SBA 2026 — Etik Kurul", layout="wide", page_icon="🔬")

# ── VERİ YÜKLEME ─────────────────────────────────────────────────────────────
EXCEL_FILE = "2026_SBA.xlsx"

@st.cache_data
def load_all_data():
    try:
        df_basvuru = pd.read_excel(EXCEL_FILE, sheet_name="Başvuru", header=0)
        df_basvuru = df_basvuru[
            df_basvuru["SBA NUMARASI"].notna() &
            df_basvuru["SBA NUMARASI"].astype(str).str.startswith("SBA")
        ].copy()

        df_sayilar = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", header=2)
        df_sayilar.columns = ["S.NO", "Gündem Tarihleri", "Başvuru", "Düzeltme", "Dilekçe", "Toplam"]
        df_sayilar = df_sayilar[df_sayilar["Gündem Tarihleri"].notna()].copy()

        df_sayilar_raw = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", header=None)
        toplam_satir = df_sayilar_raw[df_sayilar_raw[0] == "TOPLAM"].iloc[0]

        df_uye = pd.read_excel(EXCEL_FILE, sheet_name="Üye_1", header=0)
        df_uye.columns = [str(c).strip() for c in df_uye.columns]
        df_uye = df_uye[df_uye["Adı Soyadı"].notna()].copy()

        df_pivot = pd.read_excel(EXCEL_FILE, sheet_name="Pivot", header=0)

        return df_basvuru, df_sayilar, toplam_satir, df_uye, df_pivot
    except Exception as e:
        st.error(f"Excel Okuma Hatası: {e}")
        return None, None, None, None, None

df_basvuru, df_sayilar, toplam_satir, df_uye, df_pivot = load_all_data()

# ── DİNAMİK SAYILAR ──────────────────────────────────────────────────────────
toplam_b = bireysel = uzmanlik = yuksek = doktora = bekleyen = 0
kurul_sayisi = 0

if df_basvuru is not None and toplam_satir is not None:
    toplam_b = int(toplam_satir[2])
    nitelik  = df_basvuru["NİTELİĞİ"].value_counts()
    bireysel = int(nitelik.get("Bireysel Araştırma", 0))
    uzmanlik = int(nitelik.get("Uzmanlık Tezi", 0))
    yuksek   = int(nitelik.get("Yüksek Lisans Tezi", 0))
    doktora  = int(nitelik.get("Doktora Tezi", 0))

if df_uye is not None:
    bekleyen     = int(df_uye["BEKLEYEN DOSYA SAYISI"].sum() // 2)
    kurul_sayisi = len(df_sayilar) if df_sayilar is not None else 0

son_tarih = ""
if df_sayilar is not None and len(df_sayilar) > 0:
    son = pd.to_datetime(df_sayilar["Gündem Tarihleri"].dropna().iloc[-1], errors="coerce")
    if pd.notna(son):
        son_tarih = son.strftime("%d.%m.%Y")

def clean_num(val):
    if pd.isna(val) or val == "" or str(val).strip() in ["0", "0.0", "nan"]: return ""
    try: return str(int(float(val)))
    except: return str(val)

def safe_int(val):
    try:
        v = float(val)
        return int(v) if not pd.isna(v) else 0
    except: return 0

def pct_span(sayi, toplam):
    if toplam == 0: return ""
    return f"<span class='pct'>%{round(sayi/toplam*100,1)}</span>"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

.stApp { background-color: #F5F3EE !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.topbar {
    background: #1A1814; padding: 0 32px; height: 52px;
    display: flex; align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 999;
}
.topbar-brand {
    display: flex; align-items: center; gap: 10px;
    font-family: 'DM Sans', sans-serif; font-size: 0.75rem;
    font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase;
    color: rgba(255,255,255,0.85);
}
.brand-dot {
    width: 8px; height: 8px; border-radius: 50%; background: #C8502A;
    animation: pulse 2.5s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{transform:scale(1);opacity:1} 50%{transform:scale(1.5);opacity:0.7} }
.topbar-center { font-family:'DM Sans',sans-serif; font-size:0.78rem; color:rgba(255,255,255,0.45); }
.topbar-center b { color:rgba(255,255,255,0.85); font-weight:500; }
.topbar-stats { display:flex; align-items:center; }
.t-stat { display:flex; align-items:center; gap:8px; padding:0 20px; border-left:1px solid rgba(255,255,255,0.1); }
.t-num { font-family:'IBM Plex Mono',monospace; font-size:0.9rem; font-weight:500; color:#fff; }
.t-num.hi { color:#C8502A; }
.t-label { font-size:0.65rem; letter-spacing:0.07em; text-transform:uppercase; color:rgba(255,255,255,0.4); }

.page-head { display:flex; align-items:baseline; justify-content:space-between; padding:28px 32px 0; margin-bottom:20px; }
.page-title { font-family:'DM Serif Display',serif; font-size:2rem; font-weight:400; color:#1A1814; }
.page-date { font-family:'IBM Plex Mono',monospace; font-size:0.85rem; color:#8C8880; }

.cards { display:grid; grid-template-columns:repeat(6,1fr); gap:14px; padding:0 32px 24px; }
.card { background:#FFFFFF; border:1px solid #E0DCD4; border-radius:12px; padding:20px 22px; position:relative; overflow:hidden; }
.card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background:#E0DCD4; }
.card.primary::before { background:#C8502A; }
.card-num { font-family:'IBM Plex Mono',monospace; font-size:2.2rem; font-weight:500; color:#1A1814; line-height:1; }
.card.primary .card-num { color:#C8502A; }
.card-label { font-size:0.78rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; color:#8C8880; margin-top:8px; }
.card-sub { font-family:'IBM Plex Mono',monospace; font-size:0.78rem; color:#C4BFB8; margin-top:4px; }

.panel { background:#FFFFFF; border:1px solid #E0DCD4; border-radius:12px; overflow:hidden; margin:0 32px 24px; }
.panel-head { padding:16px 22px; border-bottom:1px solid #E0DCD4; display:flex; align-items:center; justify-content:space-between; background:#FAF8F4; }
.panel-title { font-size:0.82rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; color:#8C8880; }
.panel-footer { padding:12px 22px; background:#FAF8F4; border-top:1px solid #E0DCD4; font-family:'IBM Plex Mono',monospace; font-size:0.78rem; color:#8C8880; display:flex; justify-content:space-between; }

.styled-table { border-collapse:collapse; width:100% !important; font-family:'DM Sans',sans-serif; font-size:0.92rem; }
.styled-table th { padding:12px 16px; text-align:left !important; font-size:0.75rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; color:#8C8880 !important; background:#FAF8F4 !important; border-bottom:1px solid #E0DCD4 !important; border-top:none !important; border-left:none !important; border-right:none !important; white-space:nowrap; }
.styled-table td { padding:13px 16px; border-bottom:1px solid #F0EDE8 !important; border-top:none !important; border-left:none !important; border-right:none !important; color:#1A1814 !important; background:#FFFFFF !important; white-space:nowrap; text-align:left !important; }
.styled-table tr:last-child td { border-bottom:none !important; }
.styled-table tr:hover td { background:#FAF8F4 !important; }
.styled-table tr.toplam-satir td { background:#FAF8F4 !important; font-family:'IBM Plex Mono',monospace; font-weight:500; color:#1A1814 !important; border-top:2px solid #E0DCD4 !important; }
.styled-table tr.bolum-satir td { background:#FFF0EB !important; font-family:'IBM Plex Mono',monospace; font-weight:500; color:#C8502A !important; }

.mono { font-family:'IBM Plex Mono',monospace !important; font-size:0.9rem !important; }
.pct { color:#C4BFB8; font-size:0.75rem; font-family:'IBM Plex Mono',monospace; margin-left:4px; }

.prog-wrap { display:flex; align-items:center; gap:8px; min-width:130px; }
.prog-bar { flex:1; height:6px; background:#E0DCD4; border-radius:3px; overflow:hidden; }
.prog-fill { height:100%; border-radius:3px; background:#C8502A; }
.prog-fill.green { background:#2A7A4F; }
.prog-pct { font-family:'IBM Plex Mono',monospace; font-size:0.78rem; color:#8C8880; width:36px; text-align:right; flex-shrink:0; }

.wide-table-wrapper { width:100%; overflow-x:auto; }
.table-wrapper { width:100%; overflow-x:auto; }

.stTabs [data-baseweb="tab-list"] { background:#FAF8F4 !important; border-bottom:1px solid #E0DCD4 !important; padding:0 32px !important; gap:0 !important; }
.stTabs [data-baseweb="tab"] { color:#8C8880 !important; font-family:'DM Sans',sans-serif !important; font-size:0.82rem !important; font-weight:400 !important; padding:14px 20px !important; border-bottom:2px solid transparent !important; background:transparent !important; }
.stTabs [aria-selected="true"] { color:#C8502A !important; border-bottom:2px solid #C8502A !important; background:transparent !important; }
.stTabs [data-baseweb="tab-panel"] { padding:0 !important; }

.stSelectbox label { font-family:'DM Sans',sans-serif !important; font-size:0.78rem !important; color:#8C8880 !important; }

.footer { text-align:center; padding:20px; border-top:1px solid #E0DCD4; font-family:'IBM Plex Mono',monospace; font-size:0.72rem; color:#8C8880; margin-top:16px; }
.footer b { color:#1A1814; }
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
    <div class="topbar-brand">
        <div class="brand-dot"></div>SBA Etik Kurul
    </div>
    <div class="topbar-center">
        <b>Sağlık Bilimleri Araştırma Etik Kurulu</b> &nbsp;/&nbsp; Analiz Portalı &nbsp;/&nbsp; 2026
    </div>
    <div class="topbar-stats">
        <div class="t-stat"><span class="t-num hi">{toplam_b}</span><span class="t-label">Başvuru</span></div>
        <div class="t-stat"><span class="t-num">{kurul_sayisi}</span><span class="t-label">Toplantı</span></div>
        <div class="t-stat"><span class="t-num">{bekleyen}</span><span class="t-label">Bekleyen</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SAYFA BAŞLIĞI + KARTLAR ───────────────────────────────────────────────────
st.markdown(f"""
<div class="page-head">
    <div class="page-title">Başvuru Gösterge Paneli</div>
    <span class="page-date">Son toplantı: {son_tarih} &nbsp;·&nbsp; {kurul_sayisi}. Toplantı</span>
</div>
<div class="cards">
    <div class="card primary">
        <div class="card-num">{toplam_b}</div>
        <div class="card-label">Toplam Başvuru</div>
        <div class="card-sub">{kurul_sayisi} toplantı · 2026</div>
    </div>
    <div class="card">
        <div class="card-num">{bireysel}</div>
        <div class="card-label">Bireysel Araştırma</div>
        <div class="card-sub">%{round(bireysel/toplam_b*100,1) if toplam_b else 0} pay</div>
    </div>
    <div class="card">
        <div class="card-num">{uzmanlik}</div>
        <div class="card-label">Uzmanlık Tezi</div>
        <div class="card-sub">%{round(uzmanlik/toplam_b*100,1) if toplam_b else 0} pay</div>
    </div>
    <div class="card">
        <div class="card-num">{yuksek}</div>
        <div class="card-label">Y. Lisans Tezi</div>
        <div class="card-sub">%{round(yuksek/toplam_b*100,1) if toplam_b else 0} pay</div>
    </div>
    <div class="card">
        <div class="card-num">{doktora}</div>
        <div class="card-label">Doktora Tezi</div>
        <div class="card-sub">%{round(doktora/toplam_b*100,1) if toplam_b else 0} pay</div>
    </div>
    <div class="card">
        <div class="card-num">{bekleyen}</div>
        <div class="card-label">Bekleyen Dosya</div>
        <div class="card-sub">%{round(bekleyen/toplam_b*100,1) if toplam_b else 0} oranı</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Karar Çizelgesi", "👥 Raportör Analizi", "🗓 Gündem Sayıları",
    "🏢 Birim Analizi", "👨‍🏫 Araştırmacı Analizi"
])

# ── TAB 1: KARAR ÇİZELGESİ ───────────────────────────────────────────────────
with tab1:
    if df_uye is not None:
        sayi_cols = df_uye.select_dtypes(include="number").columns.tolist()
        rows_html = ""
        for _, row in df_uye.iterrows():
            dosya = safe_int(row["Dosya Sayısı"])
            onay  = safe_int(row["Onay Toplam"])
            duz   = safe_int(row["Düzeltme Toplam"])
            genel = safe_int(row["GENEL TOPLAM"])
            bek   = safe_int(row["BEKLEYEN DOSYA SAYISI"])
            tam   = round(genel/dosya*100) if dosya else 0
            bar_c = "green" if tam >= 80 else ""
            rows_html += f"""<tr>
                <td class="mono" style="color:#C4BFB8">{clean_num(row['S.No'])}</td>
                <td>{row['Adı Soyadı']}</td>
                <td class="mono">{dosya}</td>
                <td class="mono">{onay} {pct_span(onay,dosya)}</td>
                <td class="mono">{duz} {pct_span(duz,dosya)}</td>
                <td class="mono">{clean_num(row['KAEK  Toplam'])}</td>
                <td class="mono">{clean_num(row['Görüş Toplam'])}</td>
                <td class="mono">{clean_num(row['Ret Toplam'])}</td>
                <td class="mono">{clean_num(row['Kapsam Dışı Toplam'])}</td>
                <td class="mono">{clean_num(row['Geri Çekildi Toplam'])}</td>
                <td class="mono">{genel} {pct_span(genel,dosya)}</td>
                <td class="mono">{bek}</td>
                <td><div class="prog-wrap"><div class="prog-bar"><div class="prog-fill {bar_c}" style="width:{tam}%"></div></div><span class="prog-pct">{tam}%</span></div></td>
            </tr>"""

        t = {c: int(df_uye[c].sum()) for c in sayi_cols}
        td = t.get("Dosya Sayısı",0); to = t.get("Onay Toplam",0)
        tdz= t.get("Düzeltme Toplam",0); tg = t.get("GENEL TOPLAM",0)
        tb = t.get("BEKLEYEN DOSYA SAYISI",0)
        rows_html += f"""<tr class="toplam-satir">
            <td colspan="2">TOPLAM</td>
            <td class="mono">{td}</td>
            <td class="mono">{to} {pct_span(to,td)}</td>
            <td class="mono">{tdz} {pct_span(tdz,td)}</td>
            <td class="mono">{t.get('KAEK  Toplam',0)}</td>
            <td class="mono">{t.get('Görüş Toplam',0)}</td>
            <td class="mono">{t.get('Ret Toplam',0)}</td>
            <td class="mono">{t.get('Kapsam Dışı Toplam',0)}</td>
            <td class="mono">{t.get('Geri Çekildi Toplam',0)}</td>
            <td class="mono">{tg} {pct_span(tg,td)}</td>
            <td class="mono">{tb}</td><td></td>
        </tr>"""
        dd=td//2; do_=to//2; ddz=tdz//2; dg=tg//2; db=tb//2
        rows_html += f"""<tr class="bolum-satir">
            <td colspan="2">DOSYA SAYISI (Toplam / 2)</td>
            <td class="mono">{dd}</td>
            <td class="mono">{do_} {pct_span(do_,dd)}</td>
            <td class="mono">{ddz} {pct_span(ddz,dd)}</td>
            <td colspan="5"></td>
            <td class="mono">{dg} {pct_span(dg,dd)}</td>
            <td class="mono">{db}</td><td></td>
        </tr>"""
        st.markdown(f"""
        <div class="panel">
            <div class="panel-head"><span class="panel-title">Raportör Performans Tablosu</span></div>
            <div class="wide-table-wrapper">
            <table class="styled-table"><thead><tr>
                <th>#</th><th>Adı Soyadı</th><th>Atanan</th>
                <th>Onay</th><th>Düzeltme</th><th>KAEK</th><th>Görüş</th>
                <th>Ret</th><th>Kapsam Dışı</th><th>Geri Çekildi</th>
                <th>Karar Verilen</th><th>Bekleyen</th><th>Tamamlanma</th>
            </tr></thead><tbody>{rows_html}</tbody></table>
            </div>
            <div class="panel-footer">
                <span>Her dosyaya 2 raportör atanır · Toplam raportör bazında, Dosya Sayısı (/2) gerçek dosya sayısıdır</span>
                <span>Son güncelleme: {son_tarih}</span>
            </div>
        </div>""", unsafe_allow_html=True)

# ── TAB 2: RAPORTÖR ANALİZİ ──────────────────────────────────────────────────
with tab2:
    if df_uye is not None:
        r_list = df_uye["Adı Soyadı"].dropna().unique().tolist()
        _, col_mid, _ = st.columns([2, 1, 2])
        with col_mid:
            sec_r = st.selectbox("Raportör Seçin:", r_list)
        r = df_uye[df_uye["Adı Soyadı"] == sec_r].iloc[0]
        dosya = safe_int(r["Dosya Sayısı"])
        onay  = safe_int(r["Onay Toplam"])
        duz   = safe_int(r["Düzeltme Toplam"])
        kaek  = safe_int(r["KAEK  Toplam"])
        gorus = safe_int(r["Görüş Toplam"])
        ret   = safe_int(r["Ret Toplam"])
        kap   = safe_int(r["Kapsam Dışı Toplam"])
        geri  = safe_int(r["Geri Çekildi Toplam"])
        genel = safe_int(r["GENEL TOPLAM"])
        bek   = safe_int(r["BEKLEYEN DOSYA SAYISI"])
        tam   = round(genel/dosya*100) if dosya else 0

        st.markdown(f"""
        <div class="panel" style="max-width:480px; margin:24px auto;">
            <div class="panel-head"><span class="panel-title">{sec_r}</span></div>
            <table class="styled-table">
                <thead><tr><th>Karar Türü</th><th>Sayı</th><th>Pay</th></tr></thead>
                <tbody>
                <tr><td>📌 Atanan Dosya</td><td class="mono">{dosya}</td><td>—</td></tr>
                <tr><td>✅ Onay</td><td class="mono">{onay}</td><td class="mono">{pct_span(onay,dosya)}</td></tr>
                <tr><td>📝 Düzeltme</td><td class="mono">{duz}</td><td class="mono">{pct_span(duz,dosya)}</td></tr>
                <tr><td>🏛️ KAEK</td><td class="mono">{kaek}</td><td class="mono">{pct_span(kaek,dosya)}</td></tr>
                <tr><td>💬 Görüş</td><td class="mono">{gorus}</td><td class="mono">{pct_span(gorus,dosya)}</td></tr>
                <tr><td>❌ Ret</td><td class="mono">{ret}</td><td class="mono">{pct_span(ret,dosya)}</td></tr>
                <tr><td>🚫 Kapsam Dışı</td><td class="mono">{kap}</td><td class="mono">{pct_span(kap,dosya)}</td></tr>
                <tr><td>📤 Geri Çekildi</td><td class="mono">{geri}</td><td>—</td></tr>
                <tr style="border-top:2px solid #E0DCD4">
                    <td><b>📊 Karar Verilen</b></td>
                    <td class="mono"><b>{genel}</b></td>
                    <td class="mono"><b>{pct_span(genel,dosya)}</b></td>
                </tr>
                <tr><td>⏳ Bekleyen</td><td class="mono">{bek}</td><td class="mono">{pct_span(bek,dosya)}</td></tr>
                </tbody>
            </table>
            <div class="panel-footer">
                <span>Tamamlanma oranı</span>
                <span><b>{tam}%</b></span>
            </div>
        </div>""", unsafe_allow_html=True)

# ── TAB 3: GÜNDEM SAYILARI ────────────────────────────────────────────────────
with tab3:
    if df_sayilar is not None:
        dg = df_sayilar.copy()
        dg["Gündem Tarihleri"] = pd.to_datetime(dg["Gündem Tarihleri"], errors="coerce").dt.strftime("%d.%m.%Y")
        t_bas=int(toplam_satir[2]); t_duz=int(toplam_satir[3])
        t_dil=int(toplam_satir[4]); t_top=int(toplam_satir[5])
        rows = ""
        for _, row in dg.iterrows():
            bas = safe_int(row["Başvuru"])
            rows += f"""<tr>
                <td class="mono">{clean_num(row['S.NO'])}</td>
                <td class="mono">{row['Gündem Tarihleri']}</td>
                <td class="mono">{bas}</td>
                <td class="mono">{clean_num(row['Düzeltme'])}</td>
                <td class="mono">{clean_num(row['Dilekçe'])}</td>
                <td class="mono">{clean_num(row['Toplam'])}</td>
            </tr>"""
        rows += f"""<tr class="toplam-satir">
            <td colspan="2">TOPLAM</td>
            <td class="mono">{t_bas}</td><td class="mono">{t_duz}</td>
            <td class="mono">{t_dil}</td><td class="mono">{t_top}</td>
        </tr>"""
        st.markdown(f"""
        <div class="panel" style="max-width:560px; margin:24px 32px;">
            <div class="panel-head"><span class="panel-title">2026 Gündem Sayıları</span></div>
            <table class="styled-table"><thead><tr>
                <th>S.NO</th><th>Gündem Tarihi</th><th>Başvuru</th>
                <th>Düzeltme</th><th>Dilekçe</th><th>Toplam</th>
            </tr></thead><tbody>{rows}</tbody></table>
        </div>""", unsafe_allow_html=True)

# ── TAB 4: BİRİM ANALİZİ ─────────────────────────────────────────────────────
with tab4:
    if df_pivot is not None:
        birim_df = df_pivot[["Satır Etiketleri","Say BİRİMİ"]].dropna().copy()
        birim_df.columns = ["Birim Adı","Dosya Sayısı"]
        birim_df = birim_df[birim_df["Birim Adı"] != "Satır Etiketleri"].copy()
        b_top = int(birim_df["Dosya Sayısı"].sum())
        rows = ""
        for i, (_, row) in enumerate(birim_df.iterrows(), 1):
            s = int(row["Dosya Sayısı"])
            p = round(s/b_top*100,1) if b_top else 0
            rows += f"""<tr>
                <td class="mono" style="color:#C4BFB8">{i:02d}</td>
                <td>{row['Birim Adı']}</td>
                <td class="mono">{s}</td>
                <td><div class="prog-wrap"><div class="prog-bar"><div class="prog-fill" style="width:{round(p)}%"></div></div><span class="prog-pct">{p}%</span></div></td>
            </tr>"""
        st.markdown(f"""
        <div class="panel" style="margin:24px 32px;">
            <div class="panel-head"><span class="panel-title">Birim Analizi — {len(birim_df)} birim</span></div>
            <table class="styled-table"><thead><tr>
                <th>#</th><th>Birim Adı</th><th>Dosya Sayısı</th><th>Dağılım</th>
            </tr></thead><tbody>{rows}</tbody></table>
        </div>""", unsafe_allow_html=True)

# ── TAB 5: ARAŞTIRMACI ANALİZİ ───────────────────────────────────────────────
with tab5:
    if df_pivot is not None:
        sor_df = df_pivot[["Satır Etiketleri.1","Say SORUMLUSU"]].dropna().copy()
        sor_df.columns = ["Sorumlu Araştırmacı","Dosya Sayısı"]
        sor_df = sor_df[sor_df["Sorumlu Araştırmacı"] != "Satır Etiketleri"].copy()
        s_top = int(sor_df["Dosya Sayısı"].sum())
        rows = ""
        for i, (_, row) in enumerate(sor_df.iterrows(), 1):
            s = int(row["Dosya Sayısı"])
            p = round(s/s_top*100,1) if s_top else 0
            rows += f"""<tr>
                <td class="mono" style="color:#C4BFB8">{i:02d}</td>
                <td>{row['Sorumlu Araştırmacı']}</td>
                <td class="mono">{s}</td>
                <td><div class="prog-wrap"><div class="prog-bar"><div class="prog-fill" style="width:{round(p)}%"></div></div><span class="prog-pct">{p}%</span></div></td>
            </tr>"""
        st.markdown(f"""
        <div class="panel" style="margin:24px 32px;">
            <div class="panel-head"><span class="panel-title">Sorumlu Araştırmacı Analizi — {len(sor_df)} araştırmacı</span></div>
            <table class="styled-table"><thead><tr>
                <th>#</th><th>Sorumlu Araştırmacı</th><th>Dosya Sayısı</th><th>Dağılım</th>
            </tr></thead><tbody>{rows}</tbody></table>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <b>Mahsuni TÜRKATAR</b> &nbsp;·&nbsp; Hacettepe Üniversitesi &nbsp;·&nbsp;
    Sağlık Bilimleri Araştırma Etik Kurulu &nbsp;·&nbsp; {son_tarih}
</div>
""", unsafe_allow_html=True)
