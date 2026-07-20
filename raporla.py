import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="H.Ü. Sağlık Bilimleri Araştırma Etik Kurulu 2026 Analiz Portalı", layout="wide", page_icon="🔬")

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

# Global renk haritası — tüm sekmelerde kullanılır
G_CLR = {'ONAY':    ('#E8F5E9','#2E7D32'),
         'DÜZELTME':('#FFF8E1','#E65100'),
         'GÖRÜŞ':   ('#E3F2FD','#1565C0'),
         'KAEK':    ('#EDE7F6','#4527A0'),
         'RET':     ('#FFEBEE','#C62828'),
         'KAPSAM DIŞI':('#F5F5F5','#616161'),
         'GERİ ÇEKİLDİ':('#FFF9C4','#795548'),
         '':('#FFF3E0','#C8502A')}

# ── VERİ ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_excel(EXCEL_FILE, sheet_name="Başvuru", header=0)
    df = df[df["SBA NUMARASI"].notna() &
            df["SBA NUMARASI"].astype(str).str.startswith("SBA")].copy()
    # Sadece gerçek dolu satırlar (ADI veya KURUL TARİHİ dolu)
    df = df[df["ADI"].notna() & df["ADI"].astype(str).str.strip().ne("") &
            ~df["ADI"].astype(str).isin(["nan","None","0"])].copy()
    # Tarih sütunlarını ÖNCE dönüştür (ham datetime iken)
    for tc in ["KURUL TARİHİ", "BAŞVURU TARİHİ"]:
        if tc in df.columns:
            df[tc] = pd.to_datetime(df[tc], errors="coerce").dt.strftime("%d/%m/%Y").fillna("")
    # Sonra tüm sütunları string olarak temizle
    for c in df.columns:
        df[c] = df[c].apply(lambda x:
            str(x).strip() if pd.notna(x) and str(x).strip() not in
            ('nan','None','0.0') else '')
    # DÜZELTME R sütunu yoksa boş ekle
    if "DÜZELTME R" not in df.columns:
        df["DÜZELTME R"] = ""
    return df

df = load()

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
.card{background:#fff;border:1px solid #E0DCD4;border-radius:12px;padding:20px 22px;position:relative;overflow:hidden;transition:transform .15s,box-shadow .15s}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(26,24,20,.07)}
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
.stTabs [data-baseweb="tab-list"]{background:#FAF8F4!important;border-bottom:2px solid #E0DCD4!important;padding:0 32px!important;gap:0!important;overflow-x:auto!important;flex-wrap:nowrap!important}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar{height:0}
.stTabs [data-baseweb="tab"]{border-bottom:3px solid transparent!important;background:transparent!important;padding:14px 20px!important;opacity:1!important;visibility:visible!important;flex-shrink:0!important;margin-bottom:-2px!important}
.stTabs [data-baseweb="tab"] p{color:#1A1814!important;font-family:'DM Sans',sans-serif!important;font-size:.88rem!important;font-weight:600!important;opacity:1!important;visibility:visible!important;display:block!important;margin:0!important;letter-spacing:.02em!important}
.stTabs [data-baseweb="tab"][aria-selected="true"]{border-bottom:3px solid #C8502A!important}
.stTabs [data-baseweb="tab"][aria-selected="true"] p{color:#C8502A!important}
.stTabs [data-baseweb="tab"]:hover p{color:#1A1814!important}
.stTabs [data-baseweb="tab-panel"]{padding:0!important}
.footer{text-align:center;padding:20px;border-top:1px solid #E0DCD4;font-family:'IBM Plex Mono',monospace;font-size:.72rem;color:#8C8880;margin-top:16px}
.footer b{color:#1A1814}

/* SEKME (TAB) BAŞLIKLARI — büyük, net, hatasız tıklama alanı */
.stTabs [data-baseweb="tab-list"]{gap:2px!important}
.stTabs [data-baseweb="tab"]{border-radius:8px 8px 0 0!important}
.stTabs [data-baseweb="tab"]:hover{background:#F0EDE8!important}
.stTabs [data-baseweb="tab-highlight"]{background:transparent!important}

</style>
""", unsafe_allow_html=True)

# ── TOPBAR ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand"><div class="brand-dot"></div>H.Ü. SBA Etik Kurul</div>
  <div class="topbar-center">
    <b>H.Ü. Sağlık Bilimleri Araştırma Etik Kurulu</b> &nbsp;/&nbsp; 2026 Analiz Portalı
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
  <div class="page-title">H.Ü. Sağlık Bilimleri Araştırma Etik Kurulu 2026 Analiz Portalı</div>
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
    <div class="card-sub">{pct(bireysel,toplam_b,False)} oranı</div>
  </div>
  <div class="card">
    <div class="card-num">{uzmanlik}</div>
    <div class="card-label">Uzmanlık Tezi</div>
    <div class="card-sub">{pct(uzmanlik,toplam_b,False)} oranı</div>
  </div>
  <div class="card">
    <div class="card-num">{yuksek}</div>
    <div class="card-label">Y. Lisans Tezi</div>
    <div class="card-sub">{pct(yuksek,toplam_b,False)} oranı</div>
  </div>
  <div class="card">
    <div class="card-num">{doktora}</div>
    <div class="card-label">Doktora Tezi</div>
    <div class="card-sub">{pct(doktora,toplam_b,False)} oranı</div>
  </div>
  <div class="card">
    <div class="card-num">{bekleyen}</div>
    <div class="card-label">Bekleyen Dosya</div>
    <div class="card-sub">{pct(bekleyen,toplam_b,False)} oranı</div>
  </div>
</div>""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
# ── NAVİGASYON MENÜSÜ ─────────────────────────────────────────────────────────
# Not: Menü artık Streamlit'in yerleşik st.tabs bileşeniyle çalışır.
# Manuel session_state + st.rerun akışında oluşabilecek gecikme, çift tıklama ve
# (Grafikler sekmesinde olduğu gibi) yanlışlıkla iki kez render edilme türü
# sorunlar tamamen ortadan kalkar; sekme geçişleri anında ve kesintisiz olur.
MENU_ITEMS = {
    0: ("📊", "Karar Çizelgesi",  "Raportör bazında karar dökümü"),
    1: ("👥", "Raportör Analizi", "Tek raportörün tüm dosya geçmişi"),
    2: ("🗓", "Gündem Sayıları",  "Toplantı bazlı giriş/çıkış özeti"),
    3: ("🏢", "Birim Analizi",    "Anabilim dalı bazında başvuru sayıları"),
    4: ("👤", "Araştırmacı",      "Sorumlu araştırmacı bazında başvurular"),
    5: ("🔄", "Sonuçlar",         "KK1→KK2 geçiş matrisi ve tur geçmişi"),
    6: ("📈", "Grafikler",        "Genel istatistik ve trend görselleri"),
}
tabs = st.tabs([f"{ikon}  {yazi}" for ikon, yazi, _ in MENU_ITEMS.values()])

for _idx, (_ikon, _yazi, _aciklama) in MENU_ITEMS.items():
    with tabs[_idx]:
        st.markdown(
            f"<div style='padding:18px 32px 4px'>"
            f"<span style='font-family:\"DM Serif Display\",serif;font-size:1.35rem;color:#1A1814'>{_ikon} {_yazi}</span>"
            f"<span style='font-family:\"IBM Plex Mono\",monospace;font-size:.78rem;color:#8C8880;margin-left:14px'>{_aciklama}</span>"
            f"</div>", unsafe_allow_html=True)

# ══ TAB 1: KARAR ÇİZELGESİ ═══════════════════════════════════════════════════
with tabs[0]:
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
with tabs[1]:
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

        # DÜZELTME R hesapla (kartlar için)
        duz_r_say_kart = int((df["DÜZELTME R"] == sec).sum())
        r3_say_kart = int(
            ((df["DÜZELTME R"] == sec) &
             (df["RAPORTÖR 1"] != sec) &
             (df["RAPORTÖR 2"] != sec)).sum()
        )
        r3_kart_etiket = "R3: " + str(r3_say_kart) if r3_say_kart else "Hepsi R1/R2"
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;padding:24px 32px 0">
          <div class="card primary"><div class="card-num">{dosya}</div><div class="card-label">Atanan Dosya</div></div>
          <div class="card"><div class="card-num">{genel}</div><div class="card-label">Karar Verilen</div><div class="card-sub">{pct(genel,dosya,False)}</div></div>
          <div class="card"><div class="card-num">{bek}</div><div class="card-label">Bekleyen</div><div class="card-sub">{pct(bek,dosya,False)}</div></div>
          <div class="card" style="border-left:3px solid #C8502A"><div class="card-num" style="color:#C8502A">{duz_r_say_kart}</div><div class="card-label">Düzeltme Okuyan</div><div class="card-sub">{r3_kart_etiket}</div></div>
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

        # ── DÜZELTME OKUYAN (DÜZELTME R) PANELİ ──────────────────────────────────
        duz_r_df = df[df["DÜZELTME R"] == sec].copy()
        duz_r_say = len(duz_r_df)

        # R3: bu raportör R1/R2 değil ama DÜZELTME R olarak atanmış
        r3_df = duz_r_df[
            (duz_r_df["RAPORTÖR 1"] != sec) &
            (duz_r_df["RAPORTÖR 2"] != sec)
        ]
        r3_say = len(r3_df)

        if duz_r_say > 0:
            duz_r_rows = ""
            for i_r, (_, sr) in enumerate(duz_r_df.iterrows(), 1):
                r1_v   = str(sr.get("RAPORTÖR 1","") or "")
                r2_v   = str(sr.get("RAPORTÖR 2","") or "")
                is_r3  = (r1_v != sec and r2_v != sec)
                bg_r   = "#EDE7F6" if is_r3 else "#FFF3E0"
                r1_k   = r1_v.split()[-1] if r1_v else ""
                r2_k   = r2_v.split()[-1] if r2_v else ""
                rol_str = "R3" if is_r3 else "R1/R2"
                r3_bg  = "background:#4527A0;color:#fff" if is_r3 else "background:#E8F5E9;color:#2E7D32"
                kk1_v  = str(sr.get("KURUL KARARI 1","") or "")
                kk2_v  = str(sr.get("KURUL KARARI 2","") or "")
                kb, kc  = G_CLR.get(kk1_v, ("#F5F5F5","#616161"))
                kb2,kc2 = G_CLR.get(kk2_v, ("#F5F5F5","#616161"))
                sba_no  = str(sr.get("SBA NUMARASI","") or "")
                ad_v    = str(sr.get("ADI","") or "")[:60]
                sor_v   = str(sr.get("SORUMLUSU","") or "")
                tar_v   = str(sr.get("KURUL TARİHİ","") or "")
                kk1_lbl = kk1_v if kk1_v else "—"
                kk2_lbl = kk2_v if kk2_v else "—"

                duz_r_rows += (
                    '<tr style="background:' + bg_r + '">'
                    '<td class="c-idx">' + str(i_r) + '</td>'
                    '<td class="c-num" style="font-weight:600">' + sba_no + '</td>'
                    '<td style="font-size:.85rem;max-width:240px;white-space:normal">' + ad_v + '</td>'
                    '<td style="font-size:.82rem">' + sor_v + '</td>'
                    '<td class="c-num" style="font-size:.8rem">' + r1_k + ' / ' + r2_k + '</td>'
                    '<td class="c-num"><span style="background:' + kb + ';color:' + kc + ';padding:2px 8px;border-radius:4px;font-size:.78rem;font-weight:600">' + kk1_lbl + '</span></td>'
                    '<td class="c-num"><span style="background:' + kb2 + ';color:' + kc2 + ';padding:2px 8px;border-radius:4px;font-size:.78rem;font-weight:600">' + kk2_lbl + '</span></td>'
                    '<td class="c-num">' + tar_v + '</td>'
                    '<td class="c-num"><span style="' + r3_bg + ';padding:2px 8px;border-radius:4px;font-size:.75rem;font-weight:600">' + rol_str + '</span></td>'
                    '</tr>'
                )

            r3_uyari_html = ""
            if r3_say > 0:
                r3_uyari_html = (
                    '<div style="background:#EDE7F6;border-left:3px solid #4527A0;'
                    'padding:10px 16px;margin:0 32px 8px;border-radius:6px;'
                    'font-size:.82rem;color:#4527A0">'
                    '<b>&#9888; ' + str(r3_say) + ' adet R3 dosyas&#305; var</b>'
                    ' &#8212; Bu raport&#246;r, as&#305;l R1/R2 raport&#246;r de&#287;il, '
                    '3. raport&#246;r olarak atanm&#305;&#351;t&#305;r.</div>'
                )

            r3_etiket_html = ""
            if r3_say:
                r3_etiket_html = (
                    ' &nbsp;&middot;&nbsp; <b style="color:#4527A0">'
                    + str(r3_say) + ' R3</b>'
                )

            panel_html = (
                r3_uyari_html
                + '<div class="panel" style="margin:0 32px 16px">'
                + '<div class="panel-head">'
                + '<span class="panel-title">&#128203; D&uuml;zeltme Okuyan &mdash; '
                + str(duz_r_say) + ' dosya</span>'
                + '<span style="font-size:.72rem;color:#8C8880">'
                + 'D&Uuml;ZELTME R s&uuml;tunu &middot; Bu raport&ouml;r&uuml;n ad&#305;n&#305;n ge&ccedil;ti&#287;i d&uuml;zeltme dosyalar&#305;'
                + r3_etiket_html
                + '</span></div>'
                + '<div class="wide-wrap">'
                + '<table class="styled-table"><thead><tr>'
                + '<th class="c-idx">#</th>'
                + '<th class="c-num">SBA No</th>'
                + '<th>Ara&#351;t&#305;rma Ad&#305;</th>'
                + '<th>Sorumlusu</th>'
                + '<th class="c-num">R1 / R2</th>'
                + '<th class="c-num">KK1</th>'
                + '<th class="c-num">KK2</th>'
                + '<th class="c-num">Kurul Tarihi</th>'
                + '<th class="c-num">Rol</th>'
                + '</tr></thead><tbody>'
                + duz_r_rows
                + '</tbody></table></div>'
                + '<div class="panel-footer">'
                + '<span>R3 = R1/R2 raport&ouml;rlerden ba&#287;&#305;ms&#305;z, 3. raport&ouml;r olarak atanm&#305;&#351;</span>'
                + '<span>' + sec + '</span>'
                + '</div></div>'
            )
            st.markdown(panel_html, unsafe_allow_html=True)

        # ── DOSYA LİSTESİ — karara göre gruplandı ────────────────────────────────
        G_SIRA = ['ONAY','DÜZELTME','GÖRÜŞ','KAEK','RET','KAPSAM DIŞI','']
        G_LBL  = {'ONAY':'✅ ONAY','DÜZELTME':'📝 DÜZELTME','GÖRÜŞ':'💬 GÖRÜŞ',
                   'KAEK':'🏛 KAEK','RET':'❌ RET','KAPSAM DIŞI':'🚫 KAPSAM DIŞI',
                   '':'⏳ BEKLİYOR'}
        # G_CLR global olarak tanımlı

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
with tabs[2]:
        # ── Sayılar sayfasından GÜNDEM GİRİŞLERİ (yeni + düzeltme + dilekçe) ─────
        try:
            sg = pd.read_excel(EXCEL_FILE, sheet_name="Sayılar", header=2)
            sg.columns = ["S.NO","Gündem Tarihleri","Başvuru","Düzeltme","Dilekçe","Toplam"]
            sg = sg[sg["Gündem Tarihleri"].notna() & sg["Başvuru"].notna()].copy()
            sg["_s"] = pd.to_datetime(sg["Gündem Tarihleri"], errors="coerce")
            sg = sg[sg["_s"].notna()].sort_values("_s").reset_index(drop=True)
            sg["Tarih_fmt"] = sg["_s"].dt.strftime("%d/%m/%Y")
            for c3 in ["Başvuru","Düzeltme","Dilekçe","Toplam"]:
                sg[c3] = pd.to_numeric(sg[c3], errors="coerce").fillna(0).astype(int)
        except:
            sg = pd.DataFrame(columns=["S.NO","Gündem Tarihleri","Başvuru","Düzeltme","Dilekçe","Toplam","_s","Tarih_fmt"])

        # ── Başvuru sayfasından KARARLAR (o kurula atanmış yeni dosyaların kararları) ─
        gundem_kar = df[df["KURUL TARİHİ"].ne("")].groupby("KURUL TARİHİ").agg(
            Y_Bas    =("SBA NUMARASI","count"),
            Onay     =("KURUL KARARI 1", lambda x:(x=="ONAY").sum()),
            KK1_Duz  =("KURUL KARARI 1", lambda x:(x=="DÜZELTME").sum()),
            Görüş    =("KURUL KARARI 1", lambda x:(x=="GÖRÜŞ").sum()),
            KAEK     =("KURUL KARARI 1", lambda x:(x=="KAEK").sum()),
            Ret      =("KURUL KARARI 1", lambda x:(x=="RET").sum()),
            Bekleyen =("KURUL KARARI 1", lambda x:(x=="").sum()),
        ).reset_index()
        try:
            gundem_kar["_s"] = pd.to_datetime(gundem_kar["KURUL TARİHİ"], dayfirst=True, errors="coerce")
            gundem_kar = gundem_kar.sort_values("_s")
            gundem_kar["Tarih_fmt"] = gundem_kar["_s"].dt.strftime("%d/%m/%Y")
        except: pass

        # Harita: tarih → karar bilgileri
        kar_map = {}
        for _, r in gundem_kar.iterrows():
            kar_map[r["Tarih_fmt"]] = r

        # Özet toplamlar (Sayılar sayfasından)
        top_yeni = int(sg["Başvuru"].sum())
        top_duz_g = int(sg["Düzeltme"].sum())
        top_dil   = int(sg["Dilekçe"].sum())
        top_toplam= int(sg["Toplam"].sum())
        top_ona   = int(gundem_kar["Onay"].sum())
        top_bek   = int(gundem_kar["Bekleyen"].sum())
        kararli   = top_yeni - top_bek

        # ── ÖZET KARTLAR ─────────────────────────────────────────────────────────
        kart_html = (
            '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;padding:20px 32px 8px">'
            '<div class="card primary">'
            '<div class="card-num">' + str(top_toplam) + '</div>'
            '<div class="card-label">Toplam Gündem</div>'
            '<div class="card-sub">' + str(kurul_sayisi) + ' toplanti · 2026</div>'
            '</div>'
            '<div class="card" style="border-top:3px solid #1B3A4B">'
            '<div class="card-num" style="color:#1B3A4B">' + str(top_yeni) + '</div>'
            '<div class="card-label">Yeni Başvuru</div>'
            '<div class="card-sub">Sayılar sayfasından</div>'
            '</div>'
            '<div class="card" style="border-top:3px solid #E65100">'
            '<div class="card-num" style="color:#E65100">' + str(top_duz_g) + '</div>'
            '<div class="card-label">Düzeltme Gelen</div>'
            '<div class="card-sub">Önceki kuruldan</div>'
            '</div>'
            '<div class="card" style="border-top:3px solid #795548">'
            '<div class="card-num" style="color:#795548">' + str(top_dil) + '</div>'
            '<div class="card-label">Dilekçe</div>'
            '<div class="card-sub">Tekrar değerlendirme</div>'
            '</div>'
            '<div class="card" style="border-top:3px solid #2E7D32">'
            '<div class="card-num" style="color:#2E7D32">' + str(top_ona) + '</div>'
            '<div class="card-label">Onay (yeni dos.)</div>'
            '<div class="card-sub">%' + str(round(top_ona/kararli*100,1) if kararli else 0) + ' kararlı içinde</div>'
            '</div>'
            '</div>'
        )
        st.markdown(kart_html, unsafe_allow_html=True)

        # ── ANA TABLO ─────────────────────────────────────────────────────────────
        rows3 = ""
        for si3, (_, row) in enumerate(sg.iterrows(), 1):
            tarih  = row["Tarih_fmt"]
            yeni   = int(row["Başvuru"])
            duz_g  = int(row["Düzeltme"])
            dil    = int(row["Dilekçe"])
            toplam = int(row["Toplam"])

            # Kararlar — o tarihe atanmış yeni dosyalardan
            kr = kar_map.get(tarih, None)
            ona  = int(kr["Onay"])     if kr is not None else 0
            kk1d = int(kr["KK1_Duz"]) if kr is not None else 0
            gor  = int(kr["Görüş"])    if kr is not None else 0
            kaek = int(kr["KAEK"])     if kr is not None else 0
            ret  = int(kr["Ret"])      if kr is not None else 0
            bek  = int(kr["Bekleyen"]) if kr is not None else 0
            kar  = yeni - bek
            ona_pct  = "%" + str(round(ona/kar*100,1))  if kar else "—"
            kk1d_pct = "%" + str(round(kk1d/kar*100,1)) if kar else "—"

            bg_row = "background:#FFFBF0" if bek else ""

            rows3 += (
                '<tr style="' + bg_row + '">'
                '<td class="c-num" style="color:#8C8880">' + str(si3) + '</td>'
                '<td class="c-num" style="font-weight:500">' + tarih + '</td>'
                '<td class="c-num" style="font-weight:700;color:#1B3A4B">' + str(yeni) + '</td>'
                '<td class="c-num" style="color:#E65100;font-weight:' + ('700' if duz_g else '400') + '">' + (str(duz_g) if duz_g else '—') + '</td>'
                '<td class="c-num" style="color:#795548">' + (str(dil) if dil else '—') + '</td>'
                '<td class="c-num" style="font-weight:700;border-left:2px solid #E0DCD4">' + str(toplam) + '</td>'
                '<td class="c-num" style="color:#2E7D32;font-weight:' + ('700' if ona else '400') + ';border-left:2px solid #E0DCD4">' + (str(ona) if ona else '—') + '</td>'
                '<td class="c-num" style="color:#8C8880;font-size:.78rem">' + ona_pct + '</td>'
                '<td class="c-num" style="color:#E65100;font-weight:' + ('700' if kk1d else '400') + '">' + (str(kk1d) if kk1d else '—') + '</td>'
                '<td class="c-num" style="color:#8C8880;font-size:.78rem">' + kk1d_pct + '</td>'
                '<td class="c-num" style="color:#1565C0">' + (str(gor) if gor else '') + '</td>'
                '<td class="c-num" style="color:#4527A0">' + (str(kaek) if kaek else '') + '</td>'
                '<td class="c-num" style="color:#C62828">' + (str(ret) if ret else '') + '</td>'
                '<td class="c-num" style="color:#C8502A;font-weight:' + ('700' if bek else '400') + '">' + (str(bek) if bek else '—') + '</td>'
                '</tr>'
            )

        top_kk1d = int(gundem_kar["KK1_Duz"].sum())
        top_gor  = int(gundem_kar["Görüş"].sum())
        top_kaek = int(gundem_kar["KAEK"].sum())
        top_ret  = int(gundem_kar["Ret"].sum())

        rows3 += (
            '<tr class="tot">'
            '<td colspan="2">TOPLAM</td>'
            '<td class="c-num">' + str(top_yeni) + '</td>'
            '<td class="c-num" style="color:#E65100">' + str(top_duz_g) + '</td>'
            '<td class="c-num" style="color:#795548">' + str(top_dil) + '</td>'
            '<td class="c-num" style="font-weight:700;border-left:2px solid #D0CBC0">' + str(top_toplam) + '</td>'
            '<td class="c-num" style="color:#2E7D32;border-left:2px solid #D0CBC0">' + str(top_ona) + '</td>'
            '<td class="c-num" style="color:#8C8880;font-size:.78rem">%' + str(round(top_ona/kararli*100,1) if kararli else 0) + '</td>'
            '<td class="c-num" style="color:#E65100">' + str(top_kk1d) + '</td>'
            '<td class="c-num" style="color:#8C8880;font-size:.78rem">%' + str(round(top_kk1d/kararli*100,1) if kararli else 0) + '</td>'
            '<td class="c-num" style="color:#1565C0">' + str(top_gor) + '</td>'
            '<td class="c-num" style="color:#4527A0">' + str(top_kaek) + '</td>'
            '<td class="c-num" style="color:#C62828">' + str(top_ret) + '</td>'
            '<td class="c-num" style="color:#C8502A">' + str(top_bek) + '</td>'
            '</tr>'
        )

        panel3_html = (
            '<div class="panel" style="margin:0 32px 24px">'
            '<div class="panel-head">'
            '<span class="panel-title">2026 G&#252;ndem Say&#305;lar&#305; &#8212; Kurul Bazl&#305;</span>'
            '<span style="font-size:.72rem;color:#8C8880">'
            'Say&#305;lar sayfas&#305;ndan girenler &#183; Ba&#351;vuru sayfas&#305;ndan kararlar'
            '</span></div>'
            '<div class="wide-wrap">'
            '<table class="styled-table"><thead>'
            '<tr>'
            '<th class="c-num">#</th>'
            '<th class="c-num">Tarih</th>'
            '<th class="c-num" style="color:#1B3A4B">Yeni</th>'
            '<th class="c-num" style="color:#E65100">D&#252;z. Gelen</th>'
            '<th class="c-num" style="color:#795548">Dile&#231;e</th>'
            '<th class="c-num" style="border-left:2px solid #E0DCD4;font-weight:700">Toplam Giren</th>'
            '<th class="c-num" style="color:#2E7D32;border-left:2px solid #E0DCD4">Onay</th>'
            '<th class="c-num" style="color:#8C8880;font-size:.78rem">%*</th>'
            '<th class="c-num" style="color:#E65100">D&#252;z. Karar</th>'
            '<th class="c-num" style="color:#8C8880;font-size:.78rem">%*</th>'
            '<th class="c-num" style="color:#1565C0">G&#246;r&#252;&#351;</th>'
            '<th class="c-num" style="color:#4527A0">KAEK</th>'
            '<th class="c-num" style="color:#C62828">Ret</th>'
            '<th class="c-num" style="color:#C8502A">Bekleyen</th>'
            '</tr>'
            '<tr style="background:#F7F5F2">'
            '<th colspan="2"></th>'
            '<th class="c-num" style="font-size:.7rem;color:#1B3A4B">Sayılar say.</th>'
            '<th class="c-num" style="font-size:.7rem;color:#E65100">Sayılar say.</th>'
            '<th class="c-num" style="font-size:.7rem;color:#795548">Sayılar say.</th>'
            '<th class="c-num" style="font-size:.7rem;border-left:2px solid #E0DCD4">= toplam</th>'
            '<th class="c-num" style="font-size:.7rem;color:#2E7D32;border-left:2px solid #E0DCD4">Başvuru say.</th>'
            '<th class="c-num" style="font-size:.7rem;color:#8C8880">yeni dos. %</th>'
            '<th class="c-num" style="font-size:.7rem;color:#E65100">Başvuru say.</th>'
            '<th class="c-num" style="font-size:.7rem;color:#8C8880">yeni dos. %</th>'
            '<th class="c-num" style="font-size:.7rem">Başvuru say.</th>'
            '<th class="c-num" style="font-size:.7rem">Başvuru say.</th>'
            '<th class="c-num" style="font-size:.7rem">Başvuru say.</th>'
            '<th class="c-num" style="font-size:.7rem">karar yok</th>'
            '</tr>'
            '</thead><tbody>' + rows3 + '</tbody></table>'
            '</div>'
            '<div class="panel-footer">'
            '<span>* Y&#252;zde = yeni dosyalar i&#231;inde kararl&#305; olanlar&#305;n oran&#305; (bekleyenler hari&#231;) &#183; &#x1F7E1; Bekleyen olan toplant&#305;lar</span>'
            '<span>Son g&#252;ncelleme: ' + son_tarih + '</span>'
            '</div></div>'
        )
        st.markdown(panel3_html, unsafe_allow_html=True)

# ══ TAB 4: BİRİM ANALİZİ ═════════════════════════════════════════════════════
with tabs[3]:
        bn = df.groupby("BİRİMİ")["NİTELİĞİ"].value_counts().unstack(fill_value=0)
        for n in NIT_KEYS:
            if n not in bn.columns: bn[n] = 0
        bn = bn[NIT_KEYS]; bn["Toplam"] = bn.sum(axis=1)
        bn = bn.sort_values("Toplam", ascending=False).reset_index()

        rows4 = ""
        for i, row in bn.iterrows():
            bg4 = "#F7FAFB" if i%2==0 else "#FFFFFF"
            rows4 += (
                '<tr style="background:' + bg4 + '">'
                '<td class="c-idx">' + f'{i+1:02d}' + '</td>'
                '<td style="font-size:.88rem">' + str(row['BİRİMİ']) + '</td>'
                + ''.join('<td class="c-num">' + (str(int(row[n])) if int(row[n]) else '') + '</td>' for n in NIT_KEYS)
                + '<td class="c-num" style="font-weight:600;border-left:2px solid #E0DCD4">' + str(int(row['Toplam'])) + '</td>'
                '</tr>'
            )
        rows4 += (
            '<tr class="tot"><td colspan="2">TOPLAM</td>'
            + ''.join('<td class="c-num">' + str(int(bn[n].sum())) + '</td>' for n in NIT_KEYS)
            + '<td class="c-num" style="font-weight:600;border-left:2px solid #D0CBC0">' + str(int(bn['Toplam'].sum())) + '</td>'
            '</tr>'
        )
        nit_h4 = ''.join('<th class="c-num">' + k + '</th>' for k in NIT_KISA)

        st.markdown(
            '<div class="panel" style="margin:24px 32px">'
            '<div class="panel-head">'
            '<span class="panel-title">Birim Analizi &mdash; ' + str(len(bn)) + ' birim</span>'
            '<span style="font-size:.72rem;color:#8C8880">B&uuml;y&uuml;kten k&uuml;&ccedil;&uuml;&#287;e s&iacute;ral&iacute;</span>'
            '</div>'
            '<div style="max-height:600px;overflow-y:auto">'
            '<table class="styled-table" style="width:100%">'
            '<thead style="position:sticky;top:0;z-index:10">'
            '<tr><th class="c-idx">#</th><th>Birim Ad&#305;</th>' + nit_h4
            + '<th class="c-num" style="border-left:2px solid #E0DCD4">Toplam</th>'
            '</tr></thead>'
            '<tbody>' + rows4 + '</tbody>'
            '</table></div></div>',
            unsafe_allow_html=True
        )

# ══ TAB 5: ARAŞTIRMACI ANALİZİ ═══════════════════════════════════════════════
with tabs[4]:
        nit_p = df.groupby("SORUMLUSU")["NİTELİĞİ"].value_counts().unstack(fill_value=0)
        for n in NIT_KEYS:
            if n not in nit_p.columns: nit_p[n] = 0

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
            bg5  = "#F7FAFB" if i%2==0 else "#FFFFFF"
            rows5 += (
                '<tr style="background:' + bg5 + '">'
                '<td class="c-idx">' + f'{i+1:02d}' + '</td>'
                '<td style="font-size:.85rem">' + str(row['SORUMLUSU']) + '</td>'
                + ''.join('<td class="c-num">' + (str(int(row[n])) if int(row[n]) else '') + '</td>' for n in NIT_KEYS)
                + '<td class="c-num" style="border-left:2px solid #E0DCD4;color:#2E7D32">' + (str(ona5) if ona5 else '') + '</td>'
                + '<td class="c-num" style="color:#E65100">' + (str(duz5) if duz5 else '') + '</td>'
                + '<td class="c-num" style="color:#C8502A">' + (str(bek5) if bek5 else '') + '</td>'
                + '<td class="c-num" style="font-weight:600;border-left:2px solid #E0DCD4">' + str(int(row['TOPLAM'])) + '</td>'
                '</tr>'
            )
        rows5 += (
            '<tr class="tot"><td colspan="2">TOPLAM</td>'
            + ''.join('<td class="c-num">' + str(int(sor[n].sum())) + '</td>' for n in NIT_KEYS)
            + '<td class="c-num" style="border-left:2px solid #D0CBC0">' + str(int(sor["ONAY_S"].sum())) + '</td>'
            + '<td class="c-num">' + str(int(sor["DÜZELTME_S"].sum())) + '</td>'
            + '<td class="c-num">' + str(int(sor["BEKLEYEN"].sum())) + '</td>'
            + '<td class="c-num" style="font-weight:600;border-left:2px solid #D0CBC0">' + str(int(sor["TOPLAM"].sum())) + '</td>'
            '</tr>'
        )
        nit_h5 = ''.join('<th class="c-num">' + k + '</th>' for k in NIT_KISA)

        st.markdown(
            '<div class="panel" style="margin:24px 32px">'
            '<div class="panel-head">'
            '<span class="panel-title">Sorumlu Ara&#351;t&#305;rmac&#305; Analizi &mdash; ' + str(len(sor)) + ' ara&#351;t&#305;rmac&#305;</span>'
            '<span style="font-size:.72rem;color:#8C8880">B&uuml;y&uuml;kten k&uuml;&ccedil;&uuml;&#287;e s&iacute;ral&iacute;</span>'
            '</div>'
            '<div style="max-height:600px;overflow-y:auto">'
            '<table class="styled-table" style="width:100%">'
            '<thead style="position:sticky;top:0;z-index:10">'
            '<tr><th class="c-idx">#</th><th>Sorumlu Ara&#351;t&#305;rmac&#305;</th>' + nit_h5
            + '<th class="c-num" style="border-left:2px solid #E0DCD4">Onay</th>'
            + '<th class="c-num">D&uuml;zeltme</th>'
            + '<th class="c-num">Bekleyen</th>'
            + '<th class="c-num" style="border-left:2px solid #E0DCD4">Toplam</th>'
            '</tr></thead>'
            '<tbody>' + rows5 + '</tbody>'
            '</table></div></div>',
            unsafe_allow_html=True
        )


# ══ TAB 6: SONUÇLAR ══════════════════════════════════════════════════════════
with tabs[5]:
        KARARLAR_TUM6 = ['ONAY','DÜZELTME','GÖRÜŞ','KAEK','RET','KAPSAM DIŞI','GERİ ÇEKİLDİ']
        K_BG6 = {'ONAY':'#E8F5E9','DÜZELTME':'#FFF8E1','GÖRÜŞ':'#E3F2FD','KAEK':'#EDE7F6',
                  'RET':'#FFEBEE','KAPSAM DIŞI':'#F5F5F5','GERİ ÇEKİLDİ':'#FFF9C4'}
        K_FG6 = {'ONAY':'#2E7D32','DÜZELTME':'#E65100','GÖRÜŞ':'#1565C0','KAEK':'#4527A0',
                  'RET':'#C62828','KAPSAM DIŞI':'#616161','GERİ ÇEKİLDİ':'#795548'}

        d6 = df.copy()
        for c6 in ['KURUL KARARI 1','KURUL KARARI 2','KURUL KARARI 3','KURUL KARARI 4']:
            d6[c6] = d6[c6].fillna('').astype(str).str.strip().replace({'nan':'','0':'','None':''})
        kk2_var6 = d6[d6['KURUL KARARI 2'].ne('')]

        st.markdown("""<div style="padding:20px 32px 8px">
          <div style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:#1A1814;margin-bottom:4px">Karar Akış Analizi</div>
          <div style="font-size:.82rem;color:#8C8880;font-family:'IBM Plex Mono',monospace">
            KK1 → KK2 geçiş matrisi &nbsp;·&nbsp; Birden fazla tur geçiren dosyaların tam karar zinciri
          </div></div>""", unsafe_allow_html=True)

        def rozet6(k):
            bg = K_BG6.get(k,'#F5F5F5')
            fg = K_FG6.get(k,'#616161')
            return '<span style="background:' + bg + ';color:' + fg + ';padding:3px 10px;border-radius:6px;font-weight:600;font-size:.82rem;display:inline-block">' + k + '</span>'

        mat_rows6 = ''
        for k1 in KARARLAR_TUM6:
            sub = kk2_var6[kk2_var6['KURUL KARARI 1']==k1]
            if sub.empty: continue
            cells = ''
            for k2 in KARARLAR_TUM6:
                v = int((sub['KURUL KARARI 2']==k2).sum())
                if v:
                    cells += '<td class="c-num">' + rozet6(k2) + '<br><b>' + str(v) + '</b></td>'
                else:
                    cells += '<td class="c-num" style="color:#E0DCD4">—</td>'
            mat_rows6 += '<tr><td>' + rozet6(k1) + '</td>' + cells + '<td class="c-num" style="font-weight:700;border-left:2px solid #E0DCD4">' + str(len(sub)) + '</td></tr>'

        k2_hdrs6 = ''.join('<th class="c-num" style="font-size:.7rem">' + k + '</th>' for k in KARARLAR_TUM6)

        st.markdown(
            '''<div class="panel" style="margin:8px 32px 20px">
          <div class="panel-head">
            <span class="panel-title">KK1 → KK2 Geçiş Matrisi</span>
            <span style="font-size:.72rem;color:#8C8880;font-family:'IBM Plex Mono',monospace">''' +
            str(len(kk2_var6)) + ''' dosya 2. tura girdi &nbsp;·&nbsp; Satır = ilk karar &nbsp;·&nbsp; Sütun = 2. karar
            </span>
          </div>
          <div class="wide-wrap">
          <table class="styled-table"><thead><tr>
            <th>KK1 ↓ / KK2 →</th>''' + k2_hdrs6 + '''
            <th class="c-num" style="border-left:2px solid #E0DCD4">Toplam</th>
          </tr></thead><tbody>''' + mat_rows6 + '''</tbody></table>
          </div>
          <div class="panel-footer">
            <span>Satır: ilk karar (KK1) &nbsp;·&nbsp; Sütun: düzeltme sonrası 2. karar (KK2) &nbsp;·&nbsp; Örnek: DÜZELTME satırı → ONAY sütunu = düzeltme yapıp onay alan dosya sayısı</span>
          </div>
        </div>''',
            unsafe_allow_html=True)

        cok_tur6 = d6[d6['KURUL KARARI 2'].ne('')].sort_values('SBA NUMARASI').reset_index(drop=True)
        tur_rows6 = ''
        for i6, (_, s6) in enumerate(cok_tur6.iterrows(), 1):
            kk = [s6.get('KURUL KARARI ' + str(t),'') for t in range(1,5)]
            tur_say6 = sum(1 for k in kk if k)
            bg6 = '#F7FAFB' if i6%2==1 else '#FFFFFF'
            zincir = ''
            for ki6, kk_v in enumerate(kk):
                if kk_v:
                    zincir += rozet6(kk_v)
                    if ki6 < 3 and kk[ki6+1]:
                        zincir += ' <span style="color:#B0BEC5;font-size:1rem;margin:0 4px">→</span> '
            tur_rows6 += (
                '<tr style="background:' + bg6 + '">'
                '<td class="c-idx">' + str(i6) + '</td>'
                '<td class="c-num" style="font-weight:600">' + s6.get('SBA NUMARASI','') + '</td>'
                '<td style="font-size:.82rem;color:#5A7A8A">' + s6.get('NİTELİĞİ','') + '</td>'
                '<td style="font-size:.82rem">' + s6.get('SORUMLUSU','') + '</td>'
                '<td style="white-space:normal;padding:8px 16px">' + zincir + '</td>'
                '<td class="c-num" style="color:#8C8880;font-size:.8rem">' + str(tur_say6) + ' tur</td>'
                '</tr>'
            )

        st.markdown(
            '''<div class="panel" style="margin:0 32px 24px">
          <div class="panel-head">
            <span class="panel-title">Dosya Tur Geçmişi — ''' + str(len(cok_tur6)) + ''' dosya</span>
            <span style="font-size:.72rem;color:#8C8880;font-family:'IBM Plex Mono',monospace">
              2+ tur geçiren dosyalar · Karar zinciri soldan sağa
            </span>
          </div>
          <div class="wide-wrap">
          <table class="styled-table"><thead><tr>
            <th class="c-idx">#</th>
            <th class="c-num">SBA No</th>
            <th>Niteliği</th>
            <th>Sorumlusu</th>
            <th>Karar Zinciri</th>
            <th class="c-num">Tur</th>
          </tr></thead><tbody>''' + tur_rows6 + '''</tbody></table>
          </div>
          <div class="panel-footer">
            <span>KK1 → KK2 → KK3 → KK4 sırasıyla</span>
          </div>
        </div>''',
            unsafe_allow_html=True)


# ══ TAB 7: GRAFİKLER ══════════════════════════════════════════════════════════
with tabs[6]:
        onay_s  = int(df['KURUL KARARI 1'].eq('ONAY').sum())
        duz_s   = int(df['KURUL KARARI 1'].eq('DÜZELTME').sum())
        gorus_s = int(df['KURUL KARARI 1'].eq('GÖRÜŞ').sum())
        kaek_s  = int(df['KURUL KARARI 1'].eq('KAEK').sum())
        ret_s   = int(df['KURUL KARARI 1'].eq('RET').sum())
        kap_s   = int(df['KURUL KARARI 1'].eq('KAPSAM DIŞI').sum())
        kk2_say = int(df['KURUL KARARI 2'].ne('').sum())

        d7 = df.copy()
        for c7 in ['KURUL KARARI 1','NİTELİĞİ','KURUL TARİHİ','KURUL KARARI 2']:
            d7[c7] = d7[c7].fillna('').astype(str).str.strip().replace({'nan':'','None':''})

        KARARLAR7 = ['ONAY','DÜZELTME','GÖRÜŞ','KAEK','RET','KAPSAM DIŞI','GERİ ÇEKİLDİ']
        KAR_CLR7  = {'ONAY':'#2A7A4F','DÜZELTME':'#E65100','GÖRÜŞ':'#1565C0',
                     'KAEK':'#5E35B1','RET':'#C62828','KAPSAM DIŞI':'#78909C',
                     'GERİ ÇEKİLDİ':'#6D4C41'}
        NIT_CLR7  = {'Bireysel Araştırma':'#1565C0','Uzmanlık Tezi':'#2A7A4F',
                     'Yüksek Lisans Tezi':'#E65100','Doktora Tezi':'#5E35B1'}

        # ── Özet satır ───────────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="padding:20px 32px 16px;border-bottom:1px solid #E0DCD4">
          <div style="display:flex;align-items:baseline;gap:16px;margin-bottom:14px">
            <span style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:#1A1814">Grafik Raporu</span>
            <span style="font-family:'IBM Plex Mono',monospace;font-size:.82rem;color:#8C8880">{toplam_b} başvuru · {kurul_sayisi} toplantı · {son_tarih}</span>
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            {''.join([
                f'<div style="background:{bg};border-radius:8px;padding:10px 16px;border-top:3px solid {bc};min-width:80px;flex:1">'
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:1.5rem;font-weight:700;color:{bc}">{val}</div>'
                f'<div style="font-size:.7rem;color:#8C8880;margin-top:2px;letter-spacing:.05em">{lbl}</div>'
                f'<div style="font-size:.72rem;color:{bc};font-family:IBM Plex Mono,monospace">%{round(val/toplam_b*100,1) if toplam_b else 0}</div>'
                f'</div>'
                for val, lbl, bg, bc in [
                    (onay_s,  'ONAY',        '#E8F5E9','#2A7A4F'),
                    (duz_s,   'DÜZELTME',    '#FFF3E0','#E65100'),
                    (gorus_s, 'GÖRÜŞ',       '#E3F2FD','#1565C0'),
                    (kaek_s,  'KAEK',        '#EDE7F6','#5E35B1'),
                    (ret_s,   'RET',         '#FFEBEE','#C62828'),
                    (kap_s,   'KAPSAM DIŞI', '#ECEFF1','#78909C'),
                    (bekleyen,'BEKLİYOR',    '#FFF8E1','#F9A825'),
                ]
            ])}
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        # ── SATIR 1: Karar dağılımı (bar) + Nitelik (donut) ─────────────────────
        col_a, col_b = st.columns([3, 2])

        with col_a:
            kk1_v   = d7[d7['KURUL KARARI 1'].isin(KARARLAR7)]['KURUL KARARI 1'].value_counts()
            kk1_df7 = kk1_v.reset_index()
            kk1_df7.columns = ['Karar', 'Sayı']
            kk1_df7['Renk']  = kk1_df7['Karar'].map(KAR_CLR7)
            kk1_df7['Oran%'] = (kk1_df7['Sayı'] / kk1_df7['Sayı'].sum() * 100).round(1)
            kk1_df7 = kk1_df7.sort_values('Sayı', ascending=True)

            fig1 = go.Figure(go.Bar(
                x=kk1_df7['Sayı'], y=kk1_df7['Karar'], orientation='h',
                marker_color=kk1_df7['Renk'],
                text=kk1_df7.apply(lambda r: f"  {r['Sayı']}  (%{r['Oran%']})", axis=1),
                textposition='outside',
                textfont={'size':11,'family':'IBM Plex Mono','color':'#1A1814'},
                hovertemplate='<b>%{y}</b><br>Sayı: %{x}<extra></extra>',
                width=0.65,
            ))
            fig1.update_layout(
                title={'text':'Kurul Kararı Dağılımı (KK1)','font':{'size':13,'color':'#1A1814','family':'DM Sans'},'x':0},
                margin={'t':44,'b':10,'l':10,'r':130},
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=340,
                xaxis={'showgrid':True,'gridcolor':'#F0EDE8','showticklabels':False,'zeroline':False},
                yaxis={'tickfont':{'size':13,'family':'DM Sans','color':'#1A1814'}},
                showlegend=False,
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col_b:
            nit_v   = d7[d7['NİTELİĞİ'].ne('')]['NİTELİĞİ'].value_counts()
            nit_df7 = nit_v.reset_index()
            nit_df7.columns = ['Nitelik', 'Sayı']

            fig2 = px.pie(nit_df7, names='Nitelik', values='Sayı',
                          color='Nitelik', color_discrete_map=NIT_CLR7, hole=0.5)
            fig2.update_traces(
                texttemplate='%{percent:.0%}',
                textfont_size=12,
                hovertemplate='<b>%{label}</b><br>%{value} dosya · %{percent}<extra></extra>',
                marker={'line':{'color':'#fff','width':2}}
            )
            fig2.update_layout(
                title={'text':'Başvuru Türü','font':{'size':13,'color':'#1A1814','family':'DM Sans'},'x':0},
                legend={'orientation':'v','x':1.02,'y':0.5,
                        'font':{'size':11,'family':'DM Sans'}},
                margin={'t':44,'b':10,'l':10,'r':10},
                paper_bgcolor='rgba(0,0,0,0)', height=340,
                annotations=[dict(text=f'<b>{len(d7)}</b><br><span style="font-size:10px">dosya</span>',
                                  x=0.5, y=0.5, showarrow=False,
                                  font={'size':16,'color':'#1A1814','family':'IBM Plex Mono'})]
            )
            st.plotly_chart(fig2, use_container_width=True)

        # ── SATIR 2: Toplantı bazında trend ──────────────────────────────────────
        st.markdown("""<div style="padding:8px 0 4px;border-top:1px solid #F0EDE8;margin:0 0 4px">
          <span style="font-size:.78rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#8C8880">
            TOPLANTI BAZINDA KARAR AKIŞI</span>
        </div>""", unsafe_allow_html=True)

        d7['_TAR7'] = pd.to_datetime(d7['KURUL TARİHİ'], errors='coerce')
        g7 = d7[d7['_TAR7'].notna()].groupby('_TAR7').agg(
            Başvuru   =('SBA NUMARASI','count'),
            Onay      =('KURUL KARARI 1', lambda x:(x=='ONAY').sum()),
            Düzeltme  =('KURUL KARARI 1', lambda x:(x=='DÜZELTME').sum()),
            Görüş     =('KURUL KARARI 1', lambda x:(x=='GÖRÜŞ').sum()),
            Diğer     =('KURUL KARARI 1', lambda x:(~x.isin(['ONAY','DÜZELTME','GÖRÜŞ',''])).sum()),
            Bekleyen  =('KURUL KARARI 1', lambda x:(x=='').sum()),
        ).reset_index().sort_values('_TAR7')
        g7['Tarih'] = g7['_TAR7'].dt.strftime('%d/%m')
        g7['Onay%'] = (g7['Onay']/g7['Başvuru']*100).round(0).astype(int).astype(str)+'%'

        fig4 = go.Figure()
        for isim, renk in [('Onay','#2A7A4F'),('Düzeltme','#E65100'),
                            ('Görüş','#1565C0'),('Diğer','#78909C'),('Bekleyen','#CFD8DC')]:
            fig4.add_trace(go.Bar(
                name=isim, x=g7['Tarih'], y=g7[isim],
                marker_color=renk,
                text=g7[isim].where(g7[isim]>0,''),
                textposition='inside', textfont={'size':9,'color':'white'},
                hovertemplate=f'<b>%{{x}}</b><br>{isim}: %{{y}}<extra></extra>'
            ))
        # Toplam annotation + onay oranı çizgisi
        fig4.add_trace(go.Scatter(
            x=g7['Tarih'], y=g7['Onay']/g7['Başvuru']*100,
            name='Onay Oranı %', yaxis='y2',
            mode='lines+markers',
            line={'color':'#C8502A','width':2,'dash':'dot'},
            marker={'size':6,'color':'#C8502A'},
            hovertemplate='%{x}<br>Onay Oranı: %{y:.0f}%<extra></extra>'
        ))
        fig4.update_layout(
            barmode='stack',
            yaxis2={'overlaying':'y','side':'right','range':[0,100],
                    'ticksuffix':'%','showgrid':False,'tickfont':{'size':11,'color':'#C8502A'},
                    'title':{'text':'Onay Oranı','font':{'size':10,'color':'#C8502A'}}},
            legend={'orientation':'h','y':-0.14,'font':{'size':11,'family':'DM Sans'},
                    'bgcolor':'rgba(0,0,0,0)'},
            margin={'t':20,'b':70,'l':10,'r':70},
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=380,
            xaxis={'title':'Kurul Tarihi','tickfont':{'size':12,'family':'DM Sans'},
                   'gridcolor':'#F0EDE8','title_font':{'size':11,'color':'#8C8880'}},
            yaxis={'gridcolor':'#F0EDE8','title':'Dosya Sayısı',
                   'title_font':{'size':11,'color':'#8C8880'}},
            annotations=[
                dict(x=row['Tarih'], y=row['Başvuru']+1.5,
                     text=f"<b>{row['Başvuru']}</b>",
                     showarrow=False,
                     font={'size':10,'color':'#1A1814','family':'IBM Plex Mono'})
                for _, row in g7.iterrows()
            ]
        )
        st.plotly_chart(fig4, use_container_width=True)

        # ── SATIR 3: Raportör bar + KK1→KK2 akış ────────────────────────────────
        col_c, col_d = st.columns([3, 2])

        with col_c:
            st.markdown("""<div style="padding:4px 0;border-top:1px solid #F0EDE8">
              <span style="font-size:.78rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#8C8880">
                RAPORTÖR BAZINDA DOSYA DAĞILIMI</span>
            </div>""", unsafe_allow_html=True)

            rap_data7 = []
            for raptor in RAPORTORLER:
                mask7 = (d7['RAPORTÖR 1']==raptor)|(d7['RAPORTÖR 2']==raptor)
                rtop  = int(mask7.sum())
                rona  = int((d7[mask7]['KURUL KARARI 1']=='ONAY').sum())
                rduz  = int((d7[mask7]['KURUL KARARI 1']=='DÜZELTME').sum())
                rdig  = int((d7[mask7]['KURUL KARARI 1'].isin(['GÖRÜŞ','KAEK','RET','KAPSAM DIŞI'])).sum())
                rbek  = int((d7[mask7]['KURUL KARARI 1']=='').sum())
                kisa  = raptor.split()[-1]
                rap_data7.append({'Raportör':kisa, 'Tam Ad':raptor,
                                  'Onay':rona, 'Düzeltme':rduz, 'Diğer':rdig,
                                  'Bekleyen':rbek, 'Toplam':rtop})
            rap_df7 = pd.DataFrame(rap_data7).sort_values('Toplam', ascending=True)

            fig3 = go.Figure()
            for isim, renk in [('Onay','#2A7A4F'),('Düzeltme','#E65100'),
                                ('Diğer','#78909C'),('Bekleyen','#CFD8DC')]:
                fig3.add_trace(go.Bar(
                    name=isim, y=rap_df7['Raportör'], x=rap_df7[isim],
                    orientation='h', marker_color=renk,
                    text=rap_df7[isim].where(rap_df7[isim]>0,''),
                    textposition='inside',
                    textfont={'color':'white','size':9,'family':'IBM Plex Mono'},
                    hovertemplate=f'<b>%{{y}}</b><br>{isim}: %{{x}}<extra></extra>'
                ))
            fig3.update_layout(
                barmode='stack',
                legend={'orientation':'h','y':-0.08,'font':{'size':11,'family':'DM Sans'},
                        'bgcolor':'rgba(0,0,0,0)'},
                margin={'t':10,'b':50,'l':10,'r':80},
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=440,
                xaxis={'gridcolor':'#F0EDE8','title':'Dosya Sayısı','zeroline':False,
                       'title_font':{'size':11,'color':'#8C8880'}},
                yaxis={'tickfont':{'size':12,'family':'DM Sans','color':'#1A1814'}},
                annotations=[
                    dict(x=row['Toplam']+0.5, y=row['Raportör'],
                         text=f"<b>{row['Toplam']}</b>",
                         showarrow=False, xanchor='left',
                         font={'size':10,'color':'#1A1814','family':'IBM Plex Mono'})
                    for _, row in rap_df7.iterrows()
                ]
            )
            st.plotly_chart(fig3, use_container_width=True)

        with col_d:
            st.markdown("""<div style="padding:4px 0;border-top:1px solid #F0EDE8">
              <span style="font-size:.78rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#8C8880">
                KK1 → KK2 AKIŞ (2. tur)</span>
            </div>""", unsafe_allow_html=True)

            kk2_v7    = d7[d7['KURUL KARARI 2'].ne('')]
            akis_data7 = []
            for kar7 in ['DÜZELTME','GÖRÜŞ','KAEK','RET']:
                sub7 = kk2_v7[kk2_v7['KURUL KARARI 1']==kar7]
                if sub7.empty: continue
                tot7 = len(sub7)
                ona7 = int((sub7['KURUL KARARI 2']=='ONAY').sum())
                duz7 = int((sub7['KURUL KARARI 2']=='DÜZELTME').sum())
                dig7 = tot7 - ona7 - duz7
                akis_data7.append({
                    'KK1':kar7,'ONAY':ona7,'DÜZELTME':duz7,'Diğer':dig7,
                    'Toplam':tot7,'ONAY%':round(ona7/tot7*100,1)
                })
            akis_df7 = pd.DataFrame(akis_data7)

            if not akis_df7.empty:
                fig5 = go.Figure()
                for isim, renk in [('ONAY','#2A7A4F'),('DÜZELTME','#E65100'),('Diğer','#78909C')]:
                    vals = akis_df7[isim]
                    fig5.add_trace(go.Bar(
                        name=f'→ {isim}', x=akis_df7['KK1'], y=vals,
                        marker_color=renk,
                        text=vals.where(vals>0,''),
                        textposition='inside', textfont={'color':'white','size':11},
                        hovertemplate=f'<b>%{{x}}</b> → {isim}<br>%{{y}} dosya<extra></extra>'
                    ))
                fig5.update_layout(
                    barmode='stack',
                    legend={'orientation':'h','y':-0.14,'font':{'size':11,'family':'DM Sans'},
                            'bgcolor':'rgba(0,0,0,0)'},
                    margin={'t':10,'b':60,'l':10,'r':10},
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=440,
                    xaxis={'title':'1. Tur Kararı (KK1)','tickfont':{'size':13,'family':'DM Sans'},
                           'gridcolor':'#F0EDE8','title_font':{'size':11,'color':'#8C8880'}},
                    yaxis={'gridcolor':'#F0EDE8','title':'Dosya Sayısı',
                           'title_font':{'size':11,'color':'#8C8880'}},
                    annotations=[
                        dict(x=row['KK1'], y=row['Toplam']+0.5,
                             text=f"<b>{row['Toplam']}</b> dosya<br><span style='color:#2A7A4F'>%{row['ONAY%']} onay</span>",
                             showarrow=False,
                             font={'size':10,'color':'#1A1814','family':'IBM Plex Mono'})
                        for _, row in akis_df7.iterrows()
                    ]
                )
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.markdown("<div style='padding:40px;text-align:center;color:#8C8880'>Henüz 2. tur kararı girilmemiş.</div>",
                            unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <b>Mahsuni TÜRKATAR</b> &nbsp;·&nbsp; Hacettepe Üniversitesi &nbsp;·&nbsp;
  Sağlık Bilimleri Araştırma Etik Kurulu &nbsp;·&nbsp; {son_tarih}
</div>""", unsafe_allow_html=True)
