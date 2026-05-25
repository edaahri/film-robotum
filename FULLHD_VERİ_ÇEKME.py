#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 22:34:48 2026

@author: ahri
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re

# WebDriver'ı başlat (Safari)
driver = webdriver.Safari()

film_verileri = []

baslangic_sayfasi = 1
bitis_sayfasi = 4  # Test için

print("Tür bug'ı düzeltilmiş Akıllı Tarama başlatılıyor...\n")

for sayfa in range(baslangic_sayfasi, bitis_sayfasi):
    if sayfa == 1:
        url = "https://www.fullhdfilmizlesene.life/"
    else:
        url = f"https://www.fullhdfilmizlesene.life/yeni-filmler/{sayfa}" 
        
    print(f"\n--- {sayfa}. SAYFA TARANIYOR ---")
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.tt"))
        )
        
        film_link_elementleri = driver.find_elements(By.CSS_SELECTOR, "a.tt")
        linkler = [element.get_attribute("href") for element in film_link_elementleri]
        
        for link in linkler:
            try:
                driver.get(link)
                
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "izle-titles"))
                )
                
                soup = BeautifulSoup(driver.page_source, "html.parser")
                
                # 1. Film Adı
                film_adi_elementi = soup.find("div", class_="izle-titles")
                film_adi = film_adi_elementi.text.strip() if film_adi_elementi else "Bilinmiyor"
                
                # 2. FHD Puanı
                fhd_puan_div = soup.find("div", class_="puanx-puan")
                fhd_puani = fhd_puan_div.text.replace("FHD", "").strip() if fhd_puan_div else "0.0"
                
                # 3. IMDb Puanı
                imdb_div = soup.find("div", class_="imdb-ic")
                imdb_puani = imdb_div.text.replace("IMDB", "").strip() if imdb_div else "0.0"
                
                # 4. BUG FIX: Film Yılı ve Türü (Artık kelime aramak yerine başlıkları doğrudan çekiyoruz)
                film_yili = "0000" 
                film_turu = "Bilinmiyor" 
                film_info_div = soup.find("div", class_="film-info")
                
                if film_info_div:
                    li_elementleri = film_info_div.find_all("li")
                    for li in li_elementleri:
                        dt_span = li.find("span", class_="dt")
                        dd_div = li.find("div", class_="dd")
                        
                        if dt_span and dd_div:
                            baslik = dt_span.text.strip()
                            icerik = dd_div.text.strip()
                            
                            # Eğer başlık kesinlikle "Yapım" ise yılı al
                            if baslik == "Yapım":
                                yila_ait_sayilar = re.findall(r'\d{4}', icerik) 
                                if yila_ait_sayilar:
                                    film_yili = yila_ait_sayilar[0]
                                    
                            # Eğer başlık kesinlikle "Tür" ise türleri al
                            elif baslik == "Tür":
                                film_turu = icerik
                
                film_verileri.append({
                    "Film Adı": film_adi,
                    "Tür": film_turu,
                    "FHD Puanı": fhd_puani,
                    "IMDb Puanı": imdb_puani, 
                    "Yıl": film_yili,          
                    "Link": link
                })
                print(f"Çekildi: {film_adi} (Tür: {film_turu})")
                
            except Exception as e:
                print(f"Hata oluştu ({link}): {e}")

    except Exception as e:
         print("Sayfa yüklenemedi veya film bulunamadı.")
         break

driver.quit()

df = pd.DataFrame(film_verileri)
df['FHD Puanı'] = pd.to_numeric(df['FHD Puanı'], errors='coerce')
df['IMDb Puanı'] = pd.to_numeric(df['IMDb Puanı'], errors='coerce') 
df['Yıl'] = pd.to_numeric(df['Yıl'], errors='coerce')               

dosya_adi = 'filmler.csv'
# mode='a' eski verilerin silinmeyip yenilerin en alta eklenmesini sağlar
# header=False ise 'Film Adı', 'Tür' gibi başlıkların 100. sayfanın ortasına tekrar yazılmasını engeller
#df.to_csv(dosya_adi, mode='a', index=False, header=False, encoding='utf-8-sig')
df.to_csv(dosya_adi, index=False, encoding='utf-8-sig')
print("\nTEBRİKLER! Hata giderildi ve veriler kaydedildi.")