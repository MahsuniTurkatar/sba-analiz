import streamlit as st
import pandas as pd

st.set_page_config(page_title="SBA 2026 — Etik Kurul", layout="wide", page_icon="🔬")

EXCEL_FILE  = "2026_SBA.xlsx"
RAPORTORLER = [
    'Prof. Dr. Ayşe Nurten AKARSU', 'Prof. Dr. M. Özgür UYANIK',
    'Prof. Dr. Melih Önder BABAOĞLU', 'Prof. Dr. Ayşe KİN İŞLER',
    'Prof. Dr. Yavuz AYHAN', 'Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY',
    'Prof. Dr. Gözde GİRGİN', 'Doç. Dr. Kübra AYKAÇ',
    'Doç. Dr. Tolga ÇAKMAK', 'Doç. Dr. Burcu ERSÖZ ALAN',
    'Doç. Dr. Ekim GÜMELER', 'Dr. Öğr. Üyesi Müge DEMİR',
]
NIT_KEYS  = ['Bireysel Araştırma','Uzmanlık Tezi','Yüksek Lisans Tezi','Doktora Tezi']
NIT_KISA  = ['Bireysel','Uzm. Tezi','YL Tezi','Doktora']
KARARLAR  = ['ONAY','DÜZELTME','GÖRÜŞ','KAEK','RET','KAPSAM DIŞI']
KAR_RENK  = {'ONAY':'#2E7D32','DÜZELTME':'#E65100','GÖRÜŞ':'#1565C0',
              'KAEK':'#4527A0','RET':'#C62828','KAPSAM DIŞI':'#616161'}
KAR_EMO   = {'ONAY':'✅','DÜZELTME':'📝','GÖRÜŞ':'💬',
              'KAEK':'🏛','RET':'❌','KAPSAM DIŞI':'🚫'}

# ── VERİ ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_excel(EXCEL_FILE, sheet_name="Başvuru", header=0)
    df = df[df["SBA NUMARASI"].notna() &
            df["SBA NUMARASI"].astype(str).str.startswith("SBA")].copy()
    # Tarih sütunlarını ÖNCE dönüştür (ham datetime iken)
    for tc in ["KURUL TARİHİ", "BAŞVURU TARİHİ"]:
        if tc in df.columns:
            df[tc] = pd.to_datetime(df[tc], errors="coerce").dt.strftime("%d/%m/%Y").fillna("")
    # Sonra tüm sütunları string olarak temizle
    for c in df.columns:
        df[c] = df[c].apply(lambda x:
            str(x).strip() if pd.notna(x) and str(x).strip() not in
            ('nan','None','0.0') else '')
    # Sayılar sayfası — gündem tablosu
    try:
        sg = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", header=None)
        toplam_satir = sg[sg[0]=="TOPLAM"].iloc[0]
    except:
        toplam_satir = None
    return df, toplam_satir

df, toplam_satir = load()

# ── HESAPLAMALAR ──────────────────────────────────────────────────────────────
def si(v):
    try: return int(float(v)) if v not in ('','nan') else 0
    except: return 0

def pct(n, t, blk=True):
    if not t: return ""
    s = f"%{round(n/t*100,1)}"
    return f"<span class='pct'>{s}</span>" if blk else s

toplam_b = len(df)
nit_say  = df["NİTELİĞİ"].value_counts()
bireysel = int(nit_say.get("Bireysel Araştırma",0))
uzmanlik = int(nit_say.get("Uzmanlık Tezi",0))
yuksek   = int(nit_say.get("Yüksek Lisans Tezi",0))
doktora  = int(nit_say.get("Doktora Tezi",0))

bekleyen = int((df["KURUL KARARI 1"].eq("") & df["RAPORTÖR 1"].ne("")).sum())

# Kurul tarihleri
tarihler = df["KURUL TARİHİ"].replace('',pd.NA).dropna().unique()
kurul_sayisi = len(tarihler)
son_tarih = ""
try:
    # Tarihler zaten DD/MM/YYYY string — datetime parse edip max al
    son = pd.to_datetime(pd.Series(tarihler), format="%d/%m/%Y",
                         errors='coerce').dropna().max()
    if pd.notna(son): son_tarih = son.strftime("%d/%m/%Y")
except: pass

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
.stApp{background:#F5F3EE!important}.block-container{padding:0!important;max-width:100%!important}
.topbar{background:#1A1814;padding:0 32px;height:52px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:999}
.topbar-brand{display:flex;align-items:center;gap:10px;font-family:'DM Sans',sans-serif;font-size:.75rem;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.85)}
.brand-dot{width:8px;height:8px;border-radius:50%;background:#C8502A;animation:pulse 2.5s ease-in-out infinite}
@keyframes pulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.5);opacity:.7}}
.topbar-center{font-family:'DM Sans',sans-serif;font-size:.78rem;color:rgba(255,255,255,.45)}
.topbar-center b{color:rgba(255,255,255,.85);font-weight:500}
.topbar-stats{display:flex;align-items:center}
.t-stat{display:flex;align-items:center;gap:8px;padding:0 20px;border-left:1px solid rgba(255,255,255,.1)}
.t-num{font-family:'IBM Plex Mono',monospace;font-size:.9rem;font-weight:500;color:#fff}
.t-num.hi{color:#C8502A}
.t-label{font-size:.65rem;letter-spacing:.07em;text-transform:uppercase;color:rgba(255,255,255,.4)}
.page-head{display:flex;align-items:baseline;justify-content:space-between;padding:28px 32px 0;margin-bottom:20px}
.page-title{font-family:'DM Serif Display',serif;font-size:2rem;font-weight:400;color:#1A1814}
.page-date{font-family:'IBM Plex Mono',monospace;font-size:.85rem;color:#8C8880}
.cards{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;padding:0 32px 24px}
.card{background:#fff;border:1px solid #E0DCD4;border-radius:12px;padding:20px 22px;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:#E0DCD4}
.card.primary::before{background:#C8502A}
.card-num{font-family:'IBM Plex Mono',monospace;font-size:2.2rem;font-weight:500;color:#1A1814;line-height:1}
.card.primary .card-num{color:#C8502A}
.card-label{font-size:.78rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#8C8880;margin-top:8px}
.card-sub{font-family:'IBM Plex Mono',monospace;font-size:.78rem;color:#C4BFB8;margin-top:4px}
.panel{background:#fff;border:1px solid #E0DCD4;border-radius:12px;overflow:hidden;margin:0 32px 24px}
.panel-head{padding:16px 22px;border-bottom:1px solid #E0DCD4;display:flex;align-items:center;justify-content:space-between;background:#FAF8F4}
.panel-title{font-size:.82rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#8C8880}
.panel-footer{padding:12px 22px;background:#FAF8F4;border-top:1px solid #E0DCD4;font-family:'IBM Plex Mono',monospace;font-size:.78rem;color:#8C8880;display:flex;justify-content:space-between}
.styled-table{border-collapse:collapse;width:100%!important;font-family:'DM Sans',sans-serif;font-size:.92rem}
.styled-table th{padding:12px 16px;text-align:left!important;font-size:.75rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#8C8880!important;background:#FAF8F4!important;border-bottom:1px solid #E0DCD4!important;border-top:none!important;border-left:none!important;border-right:none!important;white-space:nowrap}
.styled-table td{padding:11px 16px;border-bottom:1px solid #F0EDE8!important;border-top:none!important;border-left:none!important;border-right:none!important;color:#1A1814!important;background:#fff!important;white-space:nowrap;text-align:left!important}
.styled-table tr:last-child td{border-bottom:none!important}
.styled-table tr:hover td{background:#FAF8F4!important}
.styled-table tr.tot td{background:#FAF8F4!important;font-family:'IBM Plex Mono',monospace;font-weight:500;border-top:2px solid #E0DCD4!important}
.styled-table tr.sub td{background:#FFF0EB!important;font-family:'IBM Plex Mono',monospace;font-weight:500;color:#C8502A!important}
.c-num{font-family:'IBM Plex Mono',monospace!important;font-size:.88rem!important;text-align:center!important;white-space:nowrap}
.c-idx{font-family:'IBM Plex Mono',monospace!important;font-size:.78rem!important;color:#C4BFB8;text-align:center!important;width:36px}
.styled-table td.c-num,.styled-table th.c-num{text-align:center!important}
.pct{color:#C4BFB8;font-size:.72rem;font-family:'IBM Plex Mono',monospace;display:block;line-height:1.2}
.prog-wrap{display:flex;align-items:center;gap:8px;min-width:130px}
.prog-bar{flex:1;height:6px;background:#E0DCD4;border-radius:3px;overflow:hidden}
.prog-fill{height:100%;border-radius:3px;background:#C8502A}
.prog-fill.green{background:#2A7A4F}
.prog-pct{font-family:'IBM Plex Mono',monospace;font-size:.78rem;color:#8C8880;width:36px;text-align:right;flex-shrink:0}
.wide-wrap{width:100%;overflow-x:auto}
.stTabs [data-baseweb="tab-list"]{background:#FAF8F4!important;border-bottom:1px solid #E0DCD4!important;padding:0 32px!important;gap:0!important}
.stTabs [data-baseweb="tab"]{color:#8C8880!important;font-family:'DM Sans',sans-serif!important;font-size:.82rem!important;padding:14px 20px!important;border-bottom:2px solid transparent!important;background:transparent!important}
.stTabs [aria-selected="true"]{color:#C8502A!important;border-bottom:2px solid #C8502A!important}
.stTabs [data-baseweb="tab-panel"]{padding:0!important}
.footer{text-align:center;padding:20px;border-top:1px solid #E0DCD4;font-family:'IBM Plex Mono',monospace;font-size:.72rem;color:#8C8880;margin-top:16px}
.footer b{color:#1A1814}
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
</div>""", unsafe_allow_html=True)

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
    <div class="card-sub">{pct(bireysel,toplam_b,False)} pay</div>
  </div>
  <div class="card">
    <div class="card-num">{uzmanlik}</div>
    <div class="card-label">Uzmanlık Tezi</div>
    <div class="card-sub">{pct(uzmanlik,toplam_b,False)} pay</div>
  </div>
  <div class="card">
    <div class="card-num">{yuksek}</div>
    <div class="card-label">Y. Lisans Tezi</div>
    <div class="card-sub">{pct(yuksek,toplam_b,False)} pay</div>
  </div>
  <div class="card">
    <div class="card-num">{doktora}</div>
    <div class="card-label">Doktora Tezi</div>
    <div class="card-sub">{pct(doktora,toplam_b,False)} pay</div>
  </div>
  <div class="card">
    <div class="card-num">{bekleyen}</div>
    <div class="card-label">Bekleyen Dosya</div>
    <div class="card-sub">{pct(bekleyen,toplam_b,False)} oranı</div>
  </div>
</div>""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Karar Çizelgesi","👥 Raportör Analizi","🗓 Gündem Sayıları",
    "🏢 Birim Analizi","👨‍🏫 Araştırmacı Analizi"
])

# ══ TAB 1: KARAR ÇİZELGESİ ═══════════════════════════════════════════════════
with tab1:
    rows = ""
    T = {k:0 for k in KARARLAR+['toplam','bekleyen']}
    T_nit = {n:0 for n in NIT_KEYS}

    for si_r, raptor in enumerate(RAPORTORLER, 1):
        mask = (df["RAPORTÖR 1"]==raptor)|(df["RAPORTÖR 2"]==raptor)
        r_df = df[mask]
        dosya = len(r_df)
        bek   = int((r_df["KURUL KARARI 1"].eq("")).sum())
        kk1_v = r_df["KURUL KARARI 1"].value_counts()
        genel = dosya - bek
        tam   = round(genel/dosya*100) if dosya else 0
        bc    = "green" if tam>=80 else ""

        # Nitelik × Karar
        nit_cells = ""
        for nit in NIT_KEYS:
            n_df = r_df[r_df["NİTELİĞİ"]==nit]
            n_top = len(n_df)
            T_nit[nit] += n_top
            nit_cells += f'<td class="c-num">{n_top or ""}</td>'

        # Karar hücreleri
        kar_cells = ""
        for kar in KARARLAR:
            v = int(kk1_v.get(kar,0))
            T[kar] += v
            clr = KAR_RENK.get(kar,"#9E9E9E")
            kar_cells += f'<td class="c-num" style="color:{clr if v else "#CFD8DC"}">{v or ""}</td>'

        T["toplam"]   += genel
        T["bekleyen"] += bek
        rows += f"""<tr>
          <td class="c-idx">{si_r}</td>
          <td>{raptor}</td>
          {nit_cells}
          <td style="border-left:2px solid #E8E4DC"></td>
          {kar_cells}
          <td class="c-num" style="font-weight:500;border-left:2px solid #E8E4DC">{genel or ""}</td>
          <td class="c-num" style="color:{'#C8502A' if bek else '#CFD8DC'}">{bek or ""}</td>
          <td><div class="prog-wrap"><div class="prog-bar">
            <div class="prog-fill {bc}" style="width:{tam}%"></div>
          </div><span class="prog-pct">{tam}%</span></div></td>
        </tr>"""

    # Toplam satırı
    nit_tot = "".join(f'<td class="c-num">{T_nit[n] or ""}</td>' for n in NIT_KEYS)
    kar_tot = "".join(
        f'<td class="c-num" style="color:{KAR_RENK.get(k,"")}">{T[k] or ""}</td>'
        for k in KARARLAR)
    td2 = sum(T_nit.values())
    rows += f"""<tr class="tot">
      <td colspan="2">TOPLAM</td>
      {nit_tot}
      <td style="border-left:2px solid #D0CBC0"></td>
      {kar_tot}
      <td class="c-num" style="font-weight:600;border-left:2px solid #D0CBC0">{T['toplam']}</td>
      <td class="c-num" style="color:#C8502A">{T['bekleyen']}</td>
      <td></td>
    </tr>"""
    # /2 satırı
    nit_half = "".join(f'<td class="c-num">{T_nit[n]//2 or ""}</td>' for n in NIT_KEYS)
    kar_half = "".join(
        f'<td class="c-num">{T[k]//2 or ""}</td>' for k in KARARLAR)
    rows += f"""<tr class="sub">
      <td colspan="2">DOSYA SAYISI (Toplam / 2)</td>
      {nit_half}
      <td style="border-left:2px solid #D0CBC0"></td>
      {kar_half}
      <td class="c-num" style="font-weight:600;border-left:2px solid #D0CBC0">{T['toplam']//2}</td>
      <td class="c-num">{T['bekleyen']//2}</td>
      <td></td>
    </tr>"""

    nit_hdrs = "".join(f'<th class="c-num">{k}</th>' for k in NIT_KISA)
    kar_hdrs = "".join(f'<th class="c-num">{k[:3]}</th>' for k in KARARLAR)
    st.markdown(f"""
    <div class="panel">
      <div class="panel-head"><span class="panel-title">Raportör Karar Çizelgesi</span>
        <span style="font-size:.72rem;color:#8C8880;font-family:'IBM Plex Mono',monospace">
          KK1 bazlı · Her dosyaya 2 raportör atanır · /2 = gerçek dosya sayısı
        </span>
      </div>
      <div class="wide-wrap">
      <table class="styled-table"><thead><tr>
        <th class="c-idx">#</th><th>Adı Soyadı</th>
        {nit_hdrs}
        <th style="border-left:2px solid #E8E4DC"></th>
        {kar_hdrs}
        <th class="c-num" style="border-left:2px solid #E8E4DC">Karar<br>Verilen</th>
        <th class="c-num">Bek.</th>
        <th class="c-num">Tamam.</th>
      </tr></thead><tbody>{rows}</tbody></table>
      </div>
      <div class="panel-footer">
        <span>Her dosyaya 2 raportör atanır · Toplam /2 = gerçek dosya sayısı</span>
        <span>Son güncelleme: {son_tarih}</span>
      </div>
    </div>""", unsafe_allow_html=True)

# ══ TAB 2: RAPORTÖR ANALİZİ ══════════════════════════════════════════════════
with tab2:
    _, cm, _ = st.columns([2,1,2])
    with cm:
        sec = st.selectbox("Raportör Seçin:", RAPORTORLER)

    mask  = (df["RAPORTÖR 1"]==sec)|(df["RAPORTÖR 2"]==sec)
    r_df  = df[mask].copy()
    dosya = len(r_df)
    bek   = int((r_df["KURUL KARARI 1"].eq("")).sum())
    genel = dosya - bek
    tam   = round(genel/dosya*100) if dosya else 0

    # Nitelik × KK1 matrisi
    mrows = ""
    for kar in KARARLAR:
        kar_df = r_df[r_df["KURUL KARARI 1"]==kar]
        cells  = "".join(
            f'<td class="c-num">{int((kar_df["NİTELİĞİ"]==n).sum()) or ""}</td>'
            for n in NIT_KEYS)
        top = len(kar_df)
        mrows += f"""<tr>
          <td>{KAR_EMO.get(kar,'')} {kar}</td>{cells}
          <td class="c-num" style="font-weight:500;border-left:2px solid #E0DCD4">
            {top or ""} {pct(top,dosya)}</td></tr>"""
    nit_tot2 = "".join(
        f'<td class="c-num" style="font-weight:500">{int((r_df["NİTELİĞİ"]==n).sum())}</td>'
        for n in NIT_KEYS)
    mrows += f"""<tr class="tot">
      <td>📊 Karar Verilen</td>{nit_tot2}
      <td class="c-num" style="font-weight:600;border-left:2px solid #D0CBC0">
        {genel} {pct(genel,dosya)}</td></tr>"""
    mrows += f"""<tr style="background:#FFF0EB">
      <td style="color:#C8502A;font-weight:500">⏳ Bekleyen</td>
      <td colspan="{len(NIT_KEYS)}"></td>
      <td class="c-num" style="color:#C8502A;font-weight:500;border-left:2px solid #E0DCD4">
        {bek or ""} {pct(bek,dosya)}</td></tr>"""

    # Düzeltme takibi — KK1=DÜZELTME/GÖRÜŞ → KK2 durumu
    duz_df   = r_df[r_df["KURUL KARARI 1"].isin(["DÜZELTME","GÖRÜŞ"])]
    duz_alan = len(duz_df)
    duz_gel  = int((duz_df["KURUL KARARI 2"].ne("")).sum())
    duz_bek  = duz_alan - duz_gel
    kk2_dag  = duz_df[duz_df["KURUL KARARI 2"].ne("")]["KURUL KARARI 2"].value_counts().to_dict()
    kk2_ozet = "  ".join(f"{k}:{v}" for k,v in kk2_dag.items()) or "—"

    def drow(lbl, sub_df, clr, bg):
        cells = "".join(
            f'<td class="c-num">{int((sub_df["NİTELİĞİ"]==n).sum()) or ""}</td>'
            for n in NIT_KEYS)
        return f"""<tr style="background:{bg}">
          <td style="padding:9px 16px;color:{clr};font-weight:500">{lbl}</td>
          {cells}
          <td class="c-num" style="font-weight:600;border-left:2px solid #E0DCD4;color:{clr}">
            {len(sub_df) or ""}</td></tr>"""

    duz_rows = (
        drow("📝 Düzeltme/Görüş Alan", duz_df, "#C8502A","#FFF8EE") +
        drow("✅ Geri Gelen", duz_df[duz_df["KURUL KARARI 2"].ne("")], "#2A7A4F","#F0FBF0") +
        drow("⏳ Bekliyor",   duz_df[duz_df["KURUL KARARI 2"].eq("")], "#8C6030","#FFFBF0")
    )
    nit_hdrs2 = "".join(f'<th class="c-num">{k}</th>' for k in NIT_KISA)
    tot_hdr   = f'<th class="c-num" style="border-left:2px solid #E0DCD4">Toplam</th>'

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;padding:24px 32px 0">
      <div class="card primary"><div class="card-num">{dosya}</div><div class="card-label">Atanan Dosya</div></div>
      <div class="card"><div class="card-num">{genel}</div><div class="card-label">Karar Verilen</div><div class="card-sub">{pct(genel,dosya,False)}</div></div>
      <div class="card"><div class="card-num">{bek}</div><div class="card-label">Bekleyen</div><div class="card-sub">{pct(bek,dosya,False)}</div></div>
      <div class="card"><div class="card-num">{tam}%</div><div class="card-label">Tamamlanma</div></div>
    </div>
    <div class="panel" style="margin:16px 32px 8px">
      <div class="panel-head"><span class="panel-title">KK1 × Nitelik Matrisi</span></div>
      <table class="styled-table"><thead><tr>
        <th>Karar</th>{nit_hdrs2}{tot_hdr}
      </tr></thead><tbody>{mrows}</tbody></table>
      <div class="panel-footer"><span>{sec}</span><span>Son güncelleme: {son_tarih}</span></div>
    </div>
    <div class="panel" style="margin:0 32px 24px">
      <div class="panel-head"><span class="panel-title">Düzeltme/Görüş Takibi</span>
        <span style="font-size:.72rem;color:#8C8880;font-family:'IBM Plex Mono',monospace">
          KK1=DÜZELTME/GÖRÜŞ → KK2 durumu
        </span>
      </div>
      <table class="styled-table"><thead><tr>
        <th>Durum</th>{nit_hdrs2}{tot_hdr}
      </tr></thead><tbody>{duz_rows}</tbody></table>
      <div class="panel-footer">
        <span>Geri gelenlerin KK2 kararları: {kk2_ozet}</span>
        <span>{sec}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── DOSYA LİSTESİ — karara göre gruplandı ────────────────────────────────
    G_SIRA = ['ONAY','DÜZELTME','GÖRÜŞ','KAEK','RET','KAPSAM DIŞI','']
    G_LBL  = {'ONAY':'✅ ONAY','DÜZELTME':'📝 DÜZELTME','GÖRÜŞ':'💬 GÖRÜŞ',
               'KAEK':'🏛 KAEK','RET':'❌ RET','KAPSAM DIŞI':'🚫 KAPSAM DIŞI',
               '':'⏳ BEKLİYOR'}
    G_CLR  = {'ONAY':('#E8F5E9','#2E7D32'),'DÜZELTME':('#FFF8E1','#E65100'),
               'GÖRÜŞ':('#E3F2FD','#1565C0'),'KAEK':('#EDE7F6','#4527A0'),
               'RET':('#FFEBEE','#C62828'),'KAPSAM DIŞI':('#F5F5F5','#616161'),
               '':('#FFF3E0','#C8502A')}

    satirlar = []
    for grup in G_SIRA:
        gdf = r_df[r_df["KURUL KARARI 1"] == grup]
        if gdf.empty:
            continue
        bg_g, clr_g = G_CLR.get(grup, ('#FAF8F4','#1A1814'))
        satirlar.append(
            '<tr><td colspan="10" style="background:' + bg_g + ';color:' + clr_g + ';'
            'font-family:\'IBM Plex Mono\',monospace;font-weight:600;font-size:.78rem;'
            'letter-spacing:.08em;padding:10px 16px;border-top:2px solid ' + clr_g + '40">'
            + G_LBL.get(grup, grup) + ' &nbsp;·&nbsp; ' + str(len(gdf)) + ' dosya</td></tr>'
        )
        for n_idx, (_, satir) in enumerate(gdf.iterrows(), 1):
            sba_v = satir.get("SBA NUMARASI","")
            ad_v  = satir.get("ADI","")
            sor_v = satir.get("SORUMLUSU","")
            bir_v = satir.get("BİRİMİ","")
            nit_v = satir.get("NİTELİĞİ","")
            kk1_v = satir.get("KURUL KARARI 1","")
            gd_v  = satir.get("GÜNCEL DURUM","") or kk1_v
            tar_v = satir.get("KURUL TARİHİ","")
            rol_v = "R1" if satir.get("RAPORTÖR 1","") == sec else "R2"
            kb, kc = G_CLR.get(kk1_v, ('#F5F5F5','#616161'))
            gb, gc = G_CLR.get(gd_v,  ('#F5F5F5','#616161'))
            rb = '#E3F2FD' if rol_v=='R1' else '#E8F5E9'
            rc = '#1565C0' if rol_v=='R1' else '#2E7D32'
            satirlar.append(
                '<tr>'
                '<td class="c-idx">' + str(n_idx) + '</td>'
                '<td class="c-num" style="font-weight:500">' + sba_v + '</td>'
                '<td style="max-width:260px;white-space:normal;line-height:1.4;font-size:.85rem">' + ad_v + '</td>'
                '<td style="font-size:.85rem">' + sor_v + '</td>'
                '<td style="font-size:.82rem;color:#5A7A8A">' + bir_v + '</td>'
                '<td class="c-num" style="font-size:.82rem">' + nit_v + '</td>'
                '<td class="c-num"><span style="background:' + kb + ';color:' + kc + ';padding:2px 8px;border-radius:4px;font-size:.78rem;font-weight:600">' + (kk1_v or '—') + '</span></td>'
                '<td class="c-num"><span style="background:' + gb + ';color:' + gc + ';padding:2px 8px;border-radius:4px;font-size:.78rem;font-weight:600">' + (gd_v or '—') + '</span></td>'
                '<td class="c-num" style="font-size:.82rem;color:#8C8880">' + tar_v + '</td>'
                '<td class="c-num"><span style="background:' + rb + ';color:' + rc + ';padding:2px 6px;border-radius:4px;font-size:.75rem;font-weight:600">' + rol_v + '</span></td>'
                '</tr>'
            )

    liste_html2 = "\n".join(satirlar)
    st.markdown(f"""
    <div class="panel" style="margin:0 32px 24px">
      <div class="panel-head">
        <span class="panel-title">Dosya Listesi — {dosya} dosya</span>
        <span style="font-size:.72rem;color:#8C8880;font-family:'IBM Plex Mono',monospace">
          Karara göre gruplandı &nbsp;·&nbsp; R1/R2 rolü
        </span>
      </div>
      <div class="wide-wrap">
      <table class="styled-table"><thead><tr>
        <th class="c-idx">#</th>
        <th class="c-num">SBA No</th>
        <th>Araştırma Adı</th>
        <th>Sorumlusu</th>
        <th>Birimi</th>
        <th class="c-num">Niteliği</th>
        <th class="c-num">KK1</th>
        <th class="c-num">Güncel</th>
        <th class="c-num">Kurul Tarihi</th>
        <th class="c-num">Rol</th>
      </tr></thead><tbody>{liste_html2}</tbody></table>
      </div>
      <div class="panel-footer">
        <span>{sec}</span><span>Son güncelleme: {son_tarih}</span>
      </div>
    </div>""", unsafe_allow_html=True)

# ══ TAB 3: GÜNDEM SAYILARI ════════════════════════════════════════════════════
with tab3:
    gundem = df[df["KURUL TARİHİ"].ne("")].groupby("KURUL TARİHİ").agg(
        Başvuru   =("SBA NUMARASI","count"),
        Onay      =("KURUL KARARI 1", lambda x:(x=="ONAY").sum()),
        Düzeltme  =("KURUL KARARI 1", lambda x:(x=="DÜZELTME").sum()),
        Görüş     =("KURUL KARARI 1", lambda x:(x=="GÖRÜŞ").sum()),
        Bekleyen  =("KURUL KARARI 1", lambda x:(x=="").sum()),
    ).reset_index()
    try:
        gundem["_s"] = pd.to_datetime(gundem["KURUL TARİHİ"],dayfirst=True,errors='coerce')
        gundem = gundem.sort_values("_s").drop(columns="_s")
    except: pass

    rows3 = ""
    for si3,(_, row) in enumerate(gundem.iterrows(),1):
        rows3 += f"""<tr>
          <td class="c-num">{si3}</td>
          <td class="c-num">{row['KURUL TARİHİ']}</td>
          <td class="c-num">{int(row['Başvuru'])}</td>
          <td class="c-num" style="color:#2E7D32">{int(row['Onay']) or ''}</td>
          <td class="c-num" style="color:#E65100">{int(row['Düzeltme']) or ''}</td>
          <td class="c-num" style="color:#1565C0">{int(row['Görüş']) or ''}</td>
          <td class="c-num" style="color:#C8502A">{int(row['Bekleyen']) or ''}</td>
          <td class="c-num" style="font-weight:500">{int(row['Başvuru'])}</td>
        </tr>"""
    rows3 += f"""<tr class="tot">
      <td colspan="2">TOPLAM</td>
      <td class="c-num">{int(gundem['Başvuru'].sum())}</td>
      <td class="c-num">{int(gundem['Onay'].sum())}</td>
      <td class="c-num">{int(gundem['Düzeltme'].sum())}</td>
      <td class="c-num">{int(gundem['Görüş'].sum())}</td>
      <td class="c-num">{int(gundem['Bekleyen'].sum())}</td>
      <td class="c-num" style="font-weight:600">{int(gundem['Başvuru'].sum())}</td>
    </tr>"""

    st.markdown(f"""
    <div class="panel" style="max-width:600px;margin:24px 32px">
      <div class="panel-head"><span class="panel-title">2026 Gündem Sayıları</span></div>
      <table class="styled-table"><thead><tr>
        <th class="c-num">S.NO</th><th class="c-num">Gündem Tarihi</th>
        <th class="c-num">Başvuru</th><th class="c-num">Onay</th>
        <th class="c-num">Düzeltme</th><th class="c-num">Görüş</th>
        <th class="c-num">Bekleyen</th><th class="c-num">Toplam</th>
      </tr></thead><tbody>{rows3}</tbody></table>
    </div>""", unsafe_allow_html=True)

# ══ TAB 4: BİRİM ANALİZİ ═════════════════════════════════════════════════════
with tab4:
    bn = df.groupby("BİRİMİ")["NİTELİĞİ"].value_counts().unstack(fill_value=0)
    for n in NIT_KEYS:
        if n not in bn.columns: bn[n] = 0
    bn = bn[NIT_KEYS]; bn["Toplam"] = bn.sum(axis=1)
    bn = bn.sort_values("Toplam",ascending=False).reset_index()

    rows4 = ""
    for i,row in bn.iterrows():
        rows4 += f"""<tr>
          <td class="c-idx">{i+1:02d}</td><td>{row['BİRİMİ']}</td>
          {"".join(f'<td class="c-num">{int(row[n]) or ""}</td>' for n in NIT_KEYS)}
          <td class="c-num" style="font-weight:500">{int(row['Toplam'])}</td>
        </tr>"""
    rows4 += f"""<tr class="tot"><td colspan="2">TOPLAM</td>
      {"".join(f'<td class="c-num">{int(bn[n].sum())}</td>' for n in NIT_KEYS)}
      <td class="c-num" style="font-weight:600">{int(bn['Toplam'].sum())}</td>
    </tr>"""
    nit_h4 = "".join(f'<th class="c-num">{k}</th>' for k in NIT_KISA)
    st.markdown(f"""
    <div class="panel" style="margin:24px 32px">
      <div class="panel-head"><span class="panel-title">Birim Analizi — {len(bn)} birim</span></div>
      <table class="styled-table"><thead><tr>
        <th class="c-idx">#</th><th>Birim Adı</th>{nit_h4}
        <th class="c-num">Toplam</th>
      </tr></thead><tbody>{rows4}</tbody></table>
    </div>""", unsafe_allow_html=True)

# ══ TAB 5: ARAŞTIRMACI ANALİZİ ═══════════════════════════════════════════════
with tab5:
    # Nitelik pivot
    nit_p = df.groupby("SORUMLUSU")["NİTELİĞİ"].value_counts().unstack(fill_value=0)
    for n in NIT_KEYS:
        if n not in nit_p.columns: nit_p[n] = 0

    # Karar pivot — bekleyen = KK1 boş
    bek_p = df[df["KURUL KARARI 1"].eq("")].groupby("SORUMLUSU").size().rename("BEKLEYEN")
    ona_p = df[df["KURUL KARARI 1"].eq("ONAY")].groupby("SORUMLUSU").size().rename("ONAY_S")
    duz_p = df[df["KURUL KARARI 1"].eq("DÜZELTME")].groupby("SORUMLUSU").size().rename("DÜZELTME_S")

    sor = nit_p.copy()
    sor = sor.join(ona_p, how="left").join(duz_p, how="left").join(bek_p, how="left")
    sor["TOPLAM"] = df.groupby("SORUMLUSU").size()
    sor = sor.fillna(0)
    for c in sor.columns:
        if c != "SORUMLUSU":
            sor[c] = pd.to_numeric(sor[c], errors="coerce").fillna(0).astype(int)
    sor = sor.reset_index().sort_values("TOPLAM", ascending=False).reset_index(drop=True)
    sor = sor[sor["SORUMLUSU"].ne("")]

    rows5 = ""
    for i, row in sor.iterrows():
        ona5 = int(row.get("ONAY_S", 0))
        duz5 = int(row.get("DÜZELTME_S", 0))
        bek5 = int(row.get("BEKLEYEN", 0))
        rows5 += f"""<tr>
          <td class="c-idx">{i+1:02d}</td><td>{row['SORUMLUSU']}</td>
          {"".join(f'<td class="c-num">{int(row[n]) or ""}</td>' for n in NIT_KEYS)}
          <td class="c-num" style="border-left:2px solid #E0DCD4;color:#2E7D32">{ona5 or ''}</td>
          <td class="c-num" style="color:#E65100">{duz5 or ''}</td>
          <td class="c-num" style="color:#C8502A">{bek5 or ''}</td>
          <td class="c-num" style="font-weight:500;border-left:2px solid #E0DCD4">{int(row['TOPLAM'])}</td>
        </tr>"""
    rows5 += f"""<tr class="tot"><td colspan="2">TOPLAM</td>
      {"".join(f'<td class="c-num">{int(sor[n].sum())}</td>' for n in NIT_KEYS)}
      <td class="c-num" style="border-left:2px solid #D0CBC0">{int(sor["ONAY_S"].sum())}</td>
      <td class="c-num">{int(sor["DÜZELTME_S"].sum())}</td>
      <td class="c-num">{int(sor["BEKLEYEN"].sum())}</td>
      <td class="c-num" style="font-weight:600;border-left:2px solid #D0CBC0">{int(sor["TOPLAM"].sum())}</td>
    </tr>"""
    nit_h5 = "".join(f'<th class="c-num">{k}</th>' for k in NIT_KISA)
    st.markdown(f"""
    <div class="panel" style="margin:24px 32px">
      <div class="panel-head">
        <span class="panel-title">Sorumlu Araştırmacı Analizi — {len(sor)} araştırmacı</span>
      </div>
      <div class="wide-wrap">
      <table class="styled-table"><thead><tr>
        <th class="c-idx">#</th><th>Sorumlu Araştırmacı</th>{nit_h5}
        <th class="c-num" style="border-left:2px solid #E0DCD4">Onay</th>
        <th class="c-num">Düzeltme</th><th class="c-num">Bekleyen</th>
        <th class="c-num" style="border-left:2px solid #E0DCD4">Toplam</th>
      </tr></thead><tbody>{rows5}</tbody></table>
      </div>
    </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <b>Mahsuni TÜRKATAR</b> &nbsp;·&nbsp; Hacettepe Üniversitesi &nbsp;·&nbsp;
  Sağlık Bilimleri Araştırma Etik Kurulu &nbsp;·&nbsp; {son_tarih}
</div>""", unsafe_allow_html=True)
