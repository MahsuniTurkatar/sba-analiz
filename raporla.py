import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Sayfa ayarlarını mobil ve web uyumlu yapalım
st.set_page_config(page_title="SBA 2026 Rapor", layout="wide")

# CSS ile grafik alanlarını ve mobil görünümü güzelleştirelim
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_label_with_html=True)

st.title("📊 SBA 2026 Kurul Analiz Sistemi")

# --- TÜM HOCALARIN VERİLERİ (Görselden Tek Tek İşlendi) ---
veriler = {
    "Dr. Öğr. Üyesi Müge DEMİR": {"Atanan": 31, "ONAY": 18, "DÜZELTME": 11, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Doç. Dr. Kübra AYKAÇ": {"Atanan": 30, "ONAY": 14, "DÜZELTME": 9, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Doç. Dr. Burcu ERSÖZ ALAN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 6, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Gözde GİRGİN": {"Atanan": 28, "ONAY": 18, "DÜZELTME": 5, "KAEK": 0, "GÖRÜŞ": 1, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Nazmiye Ebru ORTAÇ ERSOY": {"Atanan": 28, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Melih Önder BABAOĞLU": {"Atanan": 28, "ONAY": 12, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 1, "RET": 1, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. M. Özgür UYANIK": {"Atanan": 27, "ONAY": 17, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Ayşe Nurten AKARSU": {"Atanan": 22, "ONAY": 11, "DÜZELTME": 4, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Doç. Dr. Ekim GÜMELER": {"Atanan": 17, "ONAY": 11, "DÜZELTME": 4, "KAEK": 1, "GÖRÜŞ": 0, "RET": 1, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Yavuz AYHAN": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 8, "KAEK": 0, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Doç. Dr. Tolga ÇAKMAK": {"Atanan": 17, "ONAY": 9, "DÜZELTME": 5, "KAEK": 1, "GÖRÜŞ": 1, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0},
    "Prof. Dr. Ayşe KİN İŞLER": {"Atanan": 17, "ONAY": 12, "DÜZELTME": 3, "KAEK": 2, "GÖRÜŞ": 0, "RET": 0, "KAPSAM DIŞI": 0, "GERİ ÇEKİLDİ": 0}
}

# --- SEÇİM ALANI ---
secilen_uye = st.selectbox("👤 Analiz İçin Raportör Seçiniz:", ["Genel Durum"] + sorted(veriler.keys()))

if secilen_uye == "Genel Durum":
    st.metric("📈 Kurul Toplam Başvuru", "145")
    st.info("Raportör bazlı detayları görmek için yukarıdan isim seçebilirsiniz.")
else:
    uye_data = veriler[secilen_uye]
    
    # Şık Metrik Kartları
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Dosya Yükü", f"{uye_data['Atanan']} Adet")
    with c2:
        tamamlanan = sum([uye_data[k] for k in ["ONAY", "DÜZELTME", "KAEK", "GÖRÜŞ", "RET"]])
        st.metric("Karar Alınan", f"{tamamlanan} Adet")

    # --- ŞIK VE MOBİL UYUMLU GRAFİK (PLOTLY) ---
    kategoriler = ["ONAY", "DÜZELTME", "KAEK", "GÖRÜŞ", "RET", "KAPSAM DIŞI", "GERİ ÇEKİLDİ"]
    degerler = [uye_data[k] for k in kategoriler]
    
    # Sadece 0'dan büyükleri filtreleyelim (Grafik temizliği)
    temiz_kat = [k for k, v in zip(kategoriler, degerler) if v > 0]
    temiz_deg = [v for v in degerler if v > 0]

    fig = go.Figure(go.Bar(
        x=temiz_deg,
        y=temiz_kat,
        orientation='h',
        marker=dict(color='#3498db', line=dict(color='#2980b9', width=1.5)),
        text=temiz_deg,
        textposition='outside'
    ))

    fig.update_layout(
        title=f"<b>{secilen_uye} - Karar Dağılımı</b>",
        xaxis_title="Dosya Sayısı",
        yaxis=dict(autorange="reversed"),
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    # Streamlit üzerinde interaktif grafik
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("📱 Bu panel mobil cihazlar için optimize edilmiştir.")
