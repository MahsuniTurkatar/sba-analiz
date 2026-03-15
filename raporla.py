import streamlit as st
import pandas as pd

st.set_page_config(page_title="SBA 2026 — Etik Kurul", layout="wide", page_icon="🔬")

EXCEL_FILE = "2026_SBA.xlsx"

RAPORTORLER = [
    'Prof. Dr. Ayşe Nurten AKARSU', 'Prof. Dr. M. Özgür UYANIK',
    'Prof. Dr. Melih Önder BABAOĞLU', 'Prof. Dr. Ayşe KİN İŞLER',
    'Prof. Dr. Yavuz AYHAN', 'Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY',
    'Prof. Dr. Gözde GİRGİN', 'Doç. Dr. Kübra AYKAÇ',
    'Doç. Dr. Tolga ÇAKMAK', 'Doç. Dr. Burcu ERSÖZ ALAN',
    'Doç. Dr. Ekim GÜMELER', 'Dr. Öğr. Üyesi Müge DEMİR',
]

# ── VERİ YÜKLEME ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name="Başvuru", header=0)
        df = df[df["SBA NUMARASI"].notna() &
                df["SBA NUMARASI"].astype(str).str.startswith("SBA")].copy()
        # Tüm sütunları string olarak temizle
        for c in df.columns:
            df[c] = df[c].apply(lambda x:
                str(x).strip() if pd.notna(x) and str(x).strip() not in
                ('nan','None','0','') else '')
        return df
    except Exception as e:
        st.error(f"Excel Okuma Hatası: {e}")
        return None

df = load_data()

# ── HESAPLAMALAR ──────────────────────────────────────────────────────────────
def safe_int(v):
    try: return int(float(v)) if v not in ('','nan') else 0
    except: return 0

def pct(n, t):
    if not t: return ""
    return f"<span class='pct'>%{round(n/t*100,1)}</span>"

toplam_b = bireysel = uzmanlik = yuksek = doktora = bekleyen = 0
kurul_sayisi = 0; son_tarih = ""

if df is not None:
    toplam_b = len(df)
    nit = df["NİTELİĞİ"].value_counts()
    bireysel = int(nit.get("Bireysel Araştırma", 0))
    uzmanlik = int(nit.get("Uzmanlık Tezi", 0))
    yuksek   = int(nit.get("Yüksek Lisans Tezi", 0))
    doktora  = int(nit.get("Doktora Tezi", 0))
    bekleyen = int((df["GÜNCEL DURUM"] == "BEKLİYOR").sum())

    # Kurul sayısı: KURUL TARİHİ sütunundan benzersiz tarihler
    if "KURUL TARİHİ" in df.columns:
        tarihler = df["KURUL TARİHİ"].replace('', pd.NA).dropna().unique()
        kurul_sayisi = len(tarihler)
        try:
            son = pd.to_datetime(
                pd.Series(tarihler), dayfirst=True, errors='coerce'
            ).dropna().max()
            if pd.notna(son): son_tarih = son.strftime("%d.%m.%Y")
        except: pass

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
.stApp { background-color: #F5F3EE !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.topbar { background:#1A1814; padding:0 32px; height:52px; display:flex; align-items:center; justify-content:space-between; position:sticky; top:0; z-index:999; }
.topbar-brand { display:flex; align-items:center; gap:10px; font-family:'DM Sans',sans-serif; font-size:0.75rem; font-weight:500; letter-spacing:0.08em; text-transform:uppercase; color:rgba(255,255,255,0.85); }
.brand-dot { width:8px; height:8px; border-radius:50%; background:#C8502A; animation:pulse 2.5s ease-in-out infinite; }
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
.mono { font-family:'IBM Plex Mono',monospace !important; font-size:0.9rem !important; }
.c-num { font-family:'IBM Plex Mono',monospace !important; font-size:0.88rem !important; text-align:center !important; white-space:nowrap; }
.c-idx { font-family:'IBM Plex Mono',monospace !important; font-size:0.78rem !important; color:#C4BFB8; text-align:center !important; width:36px; }
.styled-table td.c-num { text-align:center !important; }
.styled-table th.c-num { text-align:center !important; }
.pct { color:#C4BFB8; font-size:0.72rem; font-family:'IBM Plex Mono',monospace; display:block; line-height:1.2; }
.prog-wrap { display:flex; align-items:center; gap:8px; min-width:130px; }
.prog-bar { flex:1; height:6px; background:#E0DCD4; border-radius:3px; overflow:hidden; }
.prog-fill { height:100%; border-radius:3px; background:#C8502A; }
.prog-fill.green { background:#2A7A4F; }
.prog-pct { font-family:'IBM Plex Mono',monospace; font-size:0.78rem; color:#8C8880; width:36px; text-align:right; flex-shrink:0; }
.wide-table-wrapper { width:100%; overflow-x:auto; }
.stTabs [data-baseweb="tab-list"] { background:#FAF8F4 !important; border-bottom:1px solid #E0DCD4 !important; padding:0 32px !important; gap:0 !important; }
.stTabs [data-baseweb="tab"] { color:#8C8880 !important; font-family:'DM Sans',sans-serif !important; font-size:0.82rem !important; font-weight:400 !important; padding:14px 20px !important; border-bottom:2px solid transparent !important; background:transparent !important; }
.stTabs [aria-selected="true"] { color:#C8502A !important; border-bottom:2px solid #C8502A !important; }
.stTabs [data-baseweb="tab-panel"] { padding:0 !important; }
.footer { text-align:center; padding:20px; border-top:1px solid #E0DCD4; font-family:'IBM Plex Mono',monospace; font-size:0.72rem; color:#8C8880; margin-top:16px; }
.footer b { color:#1A1814; }
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
    <div class="topbar-brand"><div class="brand-dot"></div>SBA Etik Kurul</div>
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

# ── KARTLAR ───────────────────────────────────────────────────────────────────
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
    if df is not None:
        TURLAR = [('K1','R1K1','R2K1','KK1','K1 DİLEKÇE','KK2'),
                  ('K2','R1K2','R2K2','KK2','K2 DİLEKÇE','KK3'),
                  ('K3','R1K3','R2K3','KK3','K3 DİLEKÇE','KK4'),
                  ('K4','R1K4','R2K4','KK4','K4 DİLEKÇE', None)]
        KARARLAR = ['ONAY','DÜZELTME','GÖRÜŞ','KAEK','RET','KAPSAM DIŞI']
        KAR_RENK = {'ONAY':'#2E7D32','DÜZELTME':'#E65100','GÖRÜŞ':'#1565C0',
                    'KAEK':'#4527A0','RET':'#C62828','KAPSAM DIŞI':'#616161'}

        rows_html = ""
        for si, raptor in enumerate(RAPORTORLER, 1):
            mask = (df["RAPORTÖR 1"] == raptor) | (df["RAPORTÖR 2"] == raptor)
            r_df = df[mask]
            dosya = len(r_df)
            cells = f'<td class="c-idx">{si}</td><td>{raptor}</td>'

            toplam_onay = toplam_duz = toplam_dil = 0
            for tur, r1c, r2c, kkc, dilc, kk_son in TURLAR:
                for kar in KARARLAR:
                    say = 0
                    if r1c in df.columns:
                        say += int(((df["RAPORTÖR 1"]==raptor) & (df[r1c]==kar)).sum())
                    if r2c in df.columns:
                        say += int(((df["RAPORTÖR 2"]==raptor) & (df[r2c]==kar)).sum())
                    renk = KAR_RENK.get(kar,'#9E9E9E')
                    cells += f'<td class="c-num" style="color:{renk if say else "#CFD8DC"}">{say or ""}</td>'
                    if kar == 'ONAY': toplam_onay += say
                    if kar == 'DÜZELTME': toplam_duz += say

                # Dilekçe alan sayısı
                dil = 0
                if dilc in df.columns:
                    dil = int((df[dilc] == raptor).sum())
                toplam_dil += dil
                cells += f'<td class="c-num" style="color:{"#BF360C" if dil else "#CFD8DC"}">{dil or ""}</td>'

            bek = int((mask & (df["GÜNCEL DURUM"]=="BEKLİYOR")).sum())
            tam = round((dosya-bek)/dosya*100) if dosya else 0
            bar_c = "green" if tam >= 80 else ""
            cells += f"""
                <td class="c-num" style="color:#2E7D32;border-left:2px solid #E0DCD4">{toplam_onay or ""}</td>
                <td class="c-num" style="color:#E65100">{toplam_duz or ""}</td>
                <td class="c-num" style="color:#BF360C">{toplam_dil or ""}</td>
                <td class="c-num">{bek or ""}</td>
                <td><div class="prog-wrap"><div class="prog-bar">
                    <div class="prog-fill {bar_c}" style="width:{tam}%"></div>
                    </div><span class="prog-pct">{tam}%</span></div></td>"""
            rows_html += f"<tr>{cells}</tr>"

        # Başlık grupları
        tur_basliklar = ""
        for tur, *_ in TURLAR:
            tur_basliklar += f'<th class="c-num" colspan="{len(KARARLAR)+1}">{tur.replace("K","")}.TUR</th>'

        kar_basliklar = ""
        for tur, *_ in TURLAR:
            for kar in KARARLAR:
                kar_basliklar += f'<th class="c-num">{kar[:3]}</th>'
            kar_basliklar += '<th class="c-num">Dilekçe</th>'

        st.markdown(f"""
        <div class="panel">
            <div class="panel-head"><span class="panel-title">Raportör Karar Çizelgesi</span>
            <span style="font-size:0.72rem;color:#8C8880;font-family:'IBM Plex Mono',monospace">
                Bireysel raportör kararları (R1K1/R2K1...) · Word gündeminden otomatik
            </span></div>
            <div class="wide-table-wrapper">
            <table class="styled-table"><thead>
                <tr>
                    <th class="c-idx" rowspan="2">#</th>
                    <th rowspan="2">Raportör</th>
                    {tur_basliklar}
                    <th class="c-num" colspan="4" style="border-left:2px solid #D0CBC0">GENEL</th>
                    <th rowspan="2"></th>
                </tr>
                <tr>
                    {kar_basliklar}
                    <th class="c-num" style="border-left:2px solid #D0CBC0">Onay</th>
                    <th class="c-num">Düz.</th>
                    <th class="c-num">Dilekçe</th>
                    <th class="c-num">Bekl.</th>
                </tr>
            </thead><tbody>{rows_html}</tbody></table>
            </div>
            <div class="panel-footer">
                <span>R1K1/R2K1 = 1.tur bireysel karar · KK = kurul kararı · Dilekçe = tekrar değerlendirme alanlar</span>
                <span>Son güncelleme: {son_tarih}</span>
            </div>
        </div>""", unsafe_allow_html=True)

# ── TAB 2: RAPORTÖR ANALİZİ ──────────────────────────────────────────────────
with tab2:
    if df is not None:
        _, col_mid, _ = st.columns([2, 1, 2])
        with col_mid:
            sec_r = st.selectbox("Raportör Seçin:", RAPORTORLER)

        mask = (df["RAPORTÖR 1"] == sec_r) | (df["RAPORTÖR 2"] == sec_r)
        r_df = df[mask].copy()
        dosya = len(r_df)
        bek   = int((r_df["GÜNCEL DURUM"] == "BEKLİYOR").sum())
        tam   = round((dosya-bek)/dosya*100) if dosya else 0

        NIT_KEYS = ["Bireysel Araştırma","Uzmanlık Tezi","Yüksek Lisans Tezi","Doktora Tezi"]
        NIT_LBL  = ["Bireysel","Uzm. Tezi","YL Tezi","Doktora"]
        KARARLAR2 = ["ONAY","DÜZELTME","GÖRÜŞ","KAEK","RET","KAPSAM DIŞI"]
        KAR_EMO  = {"ONAY":"✅","DÜZELTME":"📝","GÖRÜŞ":"💬","KAEK":"🏛","RET":"❌","KAPSAM DIŞI":"🚫"}

        # KK1 × Nitelik matrisi
        matrix_rows = ""
        for kar in KARARLAR2:
            kar_df = r_df[r_df["KK1"] == kar]
            cells = "".join(
                f'<td class="c-num">{int((kar_df["NİTELİĞİ"]==n).sum()) or ""}</td>'
                for n in NIT_KEYS)
            top = len(kar_df)
            matrix_rows += f"""<tr>
                <td>{KAR_EMO.get(kar,'')} {kar}</td>{cells}
                <td class="c-num" style="font-weight:500;border-left:2px solid #E0DCD4">
                    {top or ""} {pct(top,dosya)}
                </td></tr>"""

        # TOPLAM
        nit_tops = "".join(
            f'<td class="c-num" style="font-weight:500">{int((r_df["NİTELİĞİ"]==n).sum())}</td>'
            for n in NIT_KEYS)
        kk1_dolu = r_df[r_df["KK1"].ne("")]
        matrix_rows += f"""<tr class="toplam-satir">
            <td>📊 Karar Verilen (KK1)</td>{nit_tops}
            <td class="c-num" style="font-weight:600;border-left:2px solid #D0CBC0">
                {len(kk1_dolu)} {pct(len(kk1_dolu),dosya)}</td></tr>"""
        matrix_rows += f"""<tr style="background:#FFF0EB">
            <td style="color:#C8502A;font-weight:500">⏳ Bekleyen</td>
            <td colspan="4"></td>
            <td class="c-num" style="color:#C8502A;font-weight:500;border-left:2px solid #E0DCD4">
                {bek or ""} {pct(bek,dosya)}</td></tr>"""

        # Düzeltme takibi
        duz_rows = ""
        for tur_lbl, r1c, r2c, kkc, dilc, kk_son in [
            ('1.Tur','R1K1','R2K1','KK1','K1 DİLEKÇE','KK2'),
            ('2.Tur','R1K2','R2K2','KK2','K2 DİLEKÇE','KK3'),
        ]:
            if r1c not in df.columns: continue
            duz_mask = (
                ((df["RAPORTÖR 1"]==sec_r) & (df[r1c].isin(["DÜZELTME","GÖRÜŞ"]))) |
                ((df["RAPORTÖR 2"]==sec_r) & (df[r2c].isin(["DÜZELTME","GÖRÜŞ"])
                  if r2c in df.columns else [False]*len(df)))
            )
            duz_df = df[duz_mask]
            alan = len(duz_df)
            if not alan: continue
            gelen = int((duz_df[kk_son].ne("")).sum()) if kk_son in df.columns else 0
            bek2 = alan - gelen
            kk_dag = duz_df[kk_son].value_counts().to_dict() if kk_son in df.columns else {}
            kk_ozet = "  ".join(f"{k}:{v}" for k,v in kk_dag.items() if k) or "—"
            duz_rows += f"""
            <tr><td style="padding:9px 16px;font-weight:500">{tur_lbl}</td>
                <td class="c-num" style="color:#E65100">{alan}</td>
                <td class="c-num" style="color:#2E7D32">{gelen or "—"}</td>
                <td class="c-num" style="color:#E65100">{bek2 or "—"}</td>
                <td class="c-num" style="color:#8C8880;font-size:0.78rem">{kk_ozet}</td></tr>"""

        duz_panel = f"""
        <div class="panel" style="margin:0 32px 12px;">
            <div class="panel-head"><span class="panel-title">Düzeltme Takibi</span></div>
            <table class="styled-table"><thead><tr>
                <th>Tur</th><th class="c-num">Düz/Görüş Alan</th>
                <th class="c-num">Geri Gelen</th><th class="c-num">Bekliyor</th>
                <th class="c-num">Gelen Kararlar</th>
            </tr></thead><tbody>{duz_rows if duz_rows else '<tr><td colspan="5" style="text-align:center;color:#8C8880;padding:20px">Düzeltme kaydı yok</td></tr>'}</tbody></table>
        </div>""" if duz_rows else ""

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding:24px 32px 0;">
            <div class="card primary"><div class="card-num">{dosya}</div><div class="card-label">Atanan Dosya</div></div>
            <div class="card"><div class="card-num">{len(kk1_dolu)}</div><div class="card-label">Karar Verilen</div><div class="card-sub">{pct(len(kk1_dolu),dosya)}</div></div>
            <div class="card"><div class="card-num">{bek}</div><div class="card-label">Bekleyen</div><div class="card-sub">{pct(bek,dosya)}</div></div>
            <div class="card"><div class="card-num">{tam}%</div><div class="card-label">Tamamlanma</div></div>
        </div>
        <div class="panel" style="margin:16px 32px 8px;">
            <div class="panel-head"><span class="panel-title">Kurul Kararı (KK1) × Nitelik Matrisi</span></div>
            <table class="styled-table"><thead><tr>
                <th>Karar Türü</th>
                {"".join(f'<th class="c-num">{l}</th>' for l in NIT_LBL)}
                <th class="c-num" style="border-left:2px solid #E0DCD4">Toplam</th>
            </tr></thead><tbody>{matrix_rows}</tbody></table>
            <div class="panel-footer"><span>{sec_r}</span><span>Son güncelleme: {son_tarih}</span></div>
        </div>
        {duz_panel}""", unsafe_allow_html=True)

# ── TAB 3: GÜNDEM SAYILARI ────────────────────────────────────────────────────
with tab3:
    if df is not None and "KURUL TARİHİ" in df.columns:
        gundem = df[df["KURUL TARİHİ"].ne("")].groupby("KURUL TARİHİ").agg(
            Başvuru=("SBA NUMARASI","count"),
            Düzeltme=("KK1", lambda x: (x=="DÜZELTME").sum()),
            Görüş=("KK1", lambda x: (x=="GÖRÜŞ").sum()),
            Onay=("KK1", lambda x: (x=="ONAY").sum()),
        ).reset_index()

        # Tarihlere göre sırala
        try:
            gundem["_sort"] = pd.to_datetime(gundem["KURUL TARİHİ"], dayfirst=True, errors='coerce')
            gundem = gundem.sort_values("_sort").drop(columns="_sort")
        except: pass

        gundem["Toplam"] = gundem["Başvuru"]
        rows = ""
        for si, (_, row) in enumerate(gundem.iterrows(), 1):
            rows += f"""<tr>
                <td class="mono">{si}</td>
                <td class="mono">{row['KURUL TARİHİ']}</td>
                <td class="mono">{int(row['Başvuru'])}</td>
                <td class="mono">{int(row['Onay']) or ''}</td>
                <td class="mono">{int(row['Düzeltme']) or ''}</td>
                <td class="mono">{int(row['Görüş']) or ''}</td>
                <td class="mono">{int(row['Toplam'])}</td></tr>"""
        rows += f"""<tr class="toplam-satir">
            <td colspan="2">TOPLAM</td>
            <td class="mono">{int(gundem['Başvuru'].sum())}</td>
            <td class="mono">{int(gundem['Onay'].sum())}</td>
            <td class="mono">{int(gundem['Düzeltme'].sum())}</td>
            <td class="mono">{int(gundem['Görüş'].sum())}</td>
            <td class="mono">{int(gundem['Toplam'].sum())}</td></tr>"""

        st.markdown(f"""
        <div class="panel" style="max-width:560px;margin:24px 32px;">
            <div class="panel-head"><span class="panel-title">2026 Gündem Sayıları</span></div>
            <table class="styled-table"><thead><tr>
                <th>S.NO</th><th>Gündem Tarihi</th><th>Başvuru</th>
                <th>Onay</th><th>Düzeltme</th><th>Görüş</th><th>Toplam</th>
            </tr></thead><tbody>{rows}</tbody></table>
        </div>""", unsafe_allow_html=True)

# ── TAB 4: BİRİM ANALİZİ ─────────────────────────────────────────────────────
with tab4:
    if df is not None:
        NIT_KEYS2 = ["Bireysel Araştırma","Uzmanlık Tezi","Yüksek Lisans Tezi","Doktora Tezi"]
        bn = df.groupby("BİRİMİ")["NİTELİĞİ"].value_counts().unstack(fill_value=0)
        for n in NIT_KEYS2:
            if n not in bn.columns: bn[n] = 0
        bn = bn[NIT_KEYS2]
        bn["Toplam"] = bn.sum(axis=1)
        bn = bn.sort_values("Toplam", ascending=False).reset_index()

        rows = ""
        for i, row in bn.iterrows():
            rows += f"""<tr>
                <td class="c-idx">{i+1:02d}</td>
                <td>{row['BİRİMİ']}</td>
                <td class="c-num">{int(row['Bireysel Araştırma']) or ''}</td>
                <td class="c-num">{int(row['Uzmanlık Tezi']) or ''}</td>
                <td class="c-num">{int(row['Yüksek Lisans Tezi']) or ''}</td>
                <td class="c-num">{int(row['Doktora Tezi']) or ''}</td>
                <td class="c-num" style="font-weight:500">{int(row['Toplam'])}</td></tr>"""
        rows += f"""<tr class="toplam-satir"><td colspan="2">TOPLAM</td>
            {"".join(f'<td class="c-num">{int(bn[n].sum())}</td>' for n in NIT_KEYS2)}
            <td class="c-num">{int(bn['Toplam'].sum())}</td></tr>"""

        st.markdown(f"""
        <div class="panel" style="margin:24px 32px;">
            <div class="panel-head"><span class="panel-title">Birim Analizi — {len(bn)} birim</span></div>
            <table class="styled-table"><thead><tr>
                <th class="c-idx">#</th><th>Birim Adı</th>
                <th class="c-num">Bireysel</th><th class="c-num">Uzm. Tezi</th>
                <th class="c-num">YL Tezi</th><th class="c-num">Doktora</th>
                <th class="c-num">Toplam</th>
            </tr></thead><tbody>{rows}</tbody></table>
        </div>""", unsafe_allow_html=True)

# ── TAB 5: ARAŞTIRMACI ANALİZİ ───────────────────────────────────────────────
with tab5:
    if df is not None:
        b = df.copy()
        nit_p = b.groupby("SORUMLUSU")["NİTELİĞİ"].value_counts().unstack(fill_value=0)
        for n in ["Bireysel Araştırma","Uzmanlık Tezi","Yüksek Lisans Tezi","Doktora Tezi"]:
            if n not in nit_p.columns: nit_p[n] = 0
        kar_p = b.groupby("SORUMLUSU")["GÜNCEL DURUM"].value_counts().unstack(fill_value=0)
        for k in ["ONAY","DÜZELTME","BEKLİYOR"]:
            if k not in kar_p.columns: kar_p[k] = 0
        sor_df = pd.concat([nit_p, kar_p], axis=1).fillna(0).astype(int)
        sor_df["TOPLAM"] = b.groupby("SORUMLUSU").size()
        sor_df = sor_df.reset_index().sort_values("TOPLAM", ascending=False).reset_index(drop=True)

        rows = ""
        for i, row in sor_df.iterrows():
            rows += f"""<tr>
                <td class="c-idx">{i+1:02d}</td>
                <td>{row['SORUMLUSU']}</td>
                <td class="c-num">{int(row['Bireysel Araştırma']) or ''}</td>
                <td class="c-num">{int(row['Uzmanlık Tezi']) or ''}</td>
                <td class="c-num">{int(row['Yüksek Lisans Tezi']) or ''}</td>
                <td class="c-num">{int(row['Doktora Tezi']) or ''}</td>
                <td class="c-num" style="border-left:2px solid #E0DCD4;color:#2E7D32">{int(row['ONAY']) or ''}</td>
                <td class="c-num" style="color:#E65100">{int(row['DÜZELTME']) or ''}</td>
                <td class="c-num" style="color:#C8502A">{int(row['BEKLİYOR']) or ''}</td>
                <td class="c-num" style="font-weight:500;border-left:2px solid #E0DCD4">{int(row['TOPLAM'])}</td></tr>"""
        rows += f"""<tr class="toplam-satir"><td colspan="2">TOPLAM</td>
            {"".join(f'<td class="c-num">{int(sor_df[n].sum())}</td>' for n in ["Bireysel Araştırma","Uzmanlık Tezi","Yüksek Lisans Tezi","Doktora Tezi"])}
            <td class="c-num" style="border-left:2px solid #D0CBC0">{int(sor_df['ONAY'].sum())}</td>
            <td class="c-num">{int(sor_df['DÜZELTME'].sum())}</td>
            <td class="c-num">{int(sor_df['BEKLİYOR'].sum())}</td>
            <td class="c-num" style="font-weight:500;border-left:2px solid #D0CBC0">{int(sor_df['TOPLAM'].sum())}</td></tr>"""

        st.markdown(f"""
        <div class="panel" style="margin:24px 32px;">
            <div class="panel-head">
                <span class="panel-title">Sorumlu Araştırmacı Analizi — {len(sor_df)} araştırmacı</span>
            </div>
            <div class="wide-table-wrapper">
            <table class="styled-table"><thead><tr>
                <th class="c-idx">#</th><th>Sorumlu Araştırmacı</th>
                <th class="c-num">Bireysel</th><th class="c-num">Uzm. Tezi</th>
                <th class="c-num">YL Tezi</th><th class="c-num">Doktora</th>
                <th class="c-num" style="border-left:2px solid #E0DCD4">Onay</th>
                <th class="c-num">Düzeltme</th><th class="c-num">Bekleyen</th>
                <th class="c-num" style="border-left:2px solid #E0DCD4">Toplam</th>
            </tr></thead><tbody>{rows}</tbody></table>
            </div>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <b>Mahsuni TÜRKATAR</b> &nbsp;·&nbsp; Hacettepe Üniversitesi &nbsp;·&nbsp;
    Sağlık Bilimleri Araştırma Etik Kurulu &nbsp;·&nbsp; {son_tarih}
</div>
""", unsafe_allow_html=True)
