import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Hacettepe SBA 2026", layout="wide")

# --- CSS: TABLO DARALTMA VE ORTALAMA ---
st.markdown("""
    <style>
    .stApp { background-color: #000814; }
    
    /* Üst Metrikler (190 ve 4) */
    div[data-testid="stMetric"] {
        background-color: #001d3d !important;
        border: 2px solid #ffc300 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
    }

    /* Nitelik Kutuları */
    .nitelik-konteyner {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin: 15px 0;
    }
    .nitelik-box {
        flex: 1;
        background-color: #001d3d;
        border: 1px solid #ffc300;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }
    .n-label { color: #ffffff; font-size: 0.9rem; }
    .n-value { color: #ffc300; font-weight: bold; font-size: 1.4rem; display: block; }

    /* Tabloyu Daraltma ve İçeriği Ortalama */
    .styled-table {
        margin-left: auto;
        margin-right: auto;
        width: 70% !important;
        border-collapse: collapse;
    }
    .styled-table td, .styled-table th {
        text-align: center !important;
        padding: 8px !important;
        border: 1px solid #ffc300;
    }
    
    h1, h2, h3, h4, label, .stTabs [data-baseweb="tab"] { color: #ffc300 !important; }
    p, span, div { color: #ffffff; }
    
    .footer {
        width: 100%;
        text-align: center;
        color: #ffc300;
        padding: 20px;
        border-top: 1px solid #ffc300;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETLERİ ---

# 1. Gündem Tablosu (S.No Öncesindeki İndex SİLİNDİ)
gundem_data = {
    "S.NO": ["1.", "2.", "3.", "4.", "TOPLAM"],
    "Gündem Tarihleri": ["06.01.2026", "20.01.2026", "04.0
