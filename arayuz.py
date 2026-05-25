#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:54:31 2026

@author: ahri
"""
import streamlit as st
import pandas as pd

# 1. Sayfa Tasarımı
st.set_page_config(page_title="Gelişmiş Film Robotum", layout="wide")
st.title("🎬 Benim Film Robotum (Gelişmiş Versiyon)")
st.markdown("FHD Puanı, IMDb Puanı ve Film Yılına göre filtreleme yapın.")

# 2. Veriyi Yükleme (Güncellenmiş CSV dosyasını okuyoruz)
@st.cache_data
def veriyi_getir():
    df = pd.read_csv("filmler.csv")
    # Puanları ve yılı sayısal veriye çevir
    df['FHD Puanı'] = pd.to_numeric(df['FHD Puanı'], errors='coerce')
    df['IMDb Puanı'] = pd.to_numeric(df['IMDb Puanı'], errors='coerce') # YENİ
    df['Yıl'] = pd.to_numeric(df['Yıl'], errors='coerce')               # YENİ
    
    # Yılı temiz göster (Örn: 2023.0 yerine 2023), NaN olanları es geç
    df = df.dropna(subset=['Yıl'])
    df['Yıl'] = df['Yıl'].astype(int)
    return df

df = veriyi_getir()

# 3. Sol Menü (Filtreleme Seçenekleri)
st.sidebar.header("🔍 Gelişmiş Filtrele")

# Arama Kutusu
arama = st.sidebar.text_input("Film Adı Ara:")

# Tür Arama Kutusu
tur_arama = st.sidebar.text_input("Tür Ara (Örn: Aksiyon):")

# --- YENİ FİLTRE 1: IMDb Puan Slider'ı ---
min_puan_imdb, max_puan_imdb = st.sidebar.slider(
    "IMDb Puan Aralığı", 
    min_value=0.0, max_value=10.0, value=(5.0, 10.0), step=0.1
)

# --- YENİ FİLTRE 2: Film Yılı Slider'ı ---
# Veritabanımızdaki en eski ve en yeni yılı bulalım
min_yil_db = df['Yıl'].min()
max_yil_db = df['Yıl'].max()

# Slider'ı veritabanındaki yıllara göre ayarla
yil_araligi = st.sidebar.slider(
    "Film Yılı Aralığı", 
    min_value=int(min_yil_db), 
    max_value=int(max_yil_db), 
    value=(int(min_yil_db), int(max_yil_db)), 
    step=1
)

# FHD Puan Kaydırma Çubuğu (Varsayılan olarak kalsın)
min_puan_fhd, max_puan_fhd = st.sidebar.slider(
    "FHD Puan Aralığı", 
    min_value=0.0, max_value=10.0, value=(5.0, 10.0), step=0.1
)

# 4. Veriyi Filtreleme Mantığı
filtrelenmis_df = df.copy()

if arama:
    filtrelenmis_df = filtrelenmis_df[filtrelenmis_df['Film Adı'].str.contains(arama, case=False, na=False)]

if tur_arama:
    filtrelenmis_df = filtrelenmis_df[filtrelenmis_df['Tür'].str.contains(tur_arama, case=False, na=False)]

# Sayısal filtreleri uygula
# 1. IMDb Puanı
filtrelenmis_df = filtrelenmis_df[(filtrelenmis_df['IMDb Puanı'] >= min_puan_imdb) & (filtrelenmis_df['IMDb Puanı'] <= max_puan_imdb)]
# 2. Yıl
filtrelenmis_df = filtrelenmis_df[(filtrelenmis_df['Yıl'] >= yil_araligi[0]) & (filtrelenmis_df['Yıl'] <= yil_araligi[1])]
# 3. FHD Puanı
filtrelenmis_df = filtrelenmis_df[(filtrelenmis_df['FHD Puanı'] >= min_puan_fhd) & (filtrelenmis_df['FHD Puanı'] <= max_puan_fhd)]


# 5. Sonuçları Ekranda Gösterme
st.subheader(f"Listelenen Film Sayısı: {len(filtrelenmis_df)}")

# Şık bir tablo olarak göster (Yeni sütunlar IMDb ve Yıl tabloya eklendi)
st.dataframe(
    filtrelenmis_df[['Film Adı', 'Tür', 'Yıl', 'IMDb Puanı', 'FHD Puanı']], 
    use_container_width=True
)