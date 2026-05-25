# 🎬 Film Kazıyıcı & İnteraktif Filtreleme Platformu (Film Robotum)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fullhd-film-robotu.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-Automation-green.svg)](https://www.selenium.dev/)

## 📌 Proje Hakkında
Bu proje, uçtan uca otomatik bir web veri çekme (scraping) ve görselleştirme hattıdır. Bir film izleme sitesinden film verilerini (Film Adı, IMDb Puanı, FHD Puanı, Çıkış Yılı ve Türü) dinamik olarak çeker, elde edilen ham veriyi temizler ve interaktif, canlı bir web arayüzü üzerinden kullanıcıya sunar.

Bu platform; ölçeklenebilir otomasyon pratiklerini, dinamik DOM (Sayfa Yapısı) yönetimini ve veri yapılandırma yeteneklerini sergilemek amacıyla geliştirilmiştir.

## 🚀 Canlı Demo
Canlı uygulamayı buradan deneyebilirsiniz: **[Film Filtreleme Platformu](https://fullhd-film-robotu.streamlit.app/)**

## 🛠️ Kullanılan Teknolojiler ve Araçlar
* **Veri Çekme / Otomasyon:** Python, Selenium WebDriver, BeautifulSoup (bs4)
* **Veri İşleme ve Temizleme:** Pandas, Regex (re)
* **Ön Yüz (Front-End) / Canlıya Alma:** Streamlit, Streamlit Community Cloud

## 🎯 QA ve SDET Vurguları (Nasıl Geliştirdim?)
Kalite güvencesi (QA) ve hatasız otomasyon mimarilerine odaklanan bir geliştirici olarak, bu projede çeşitli dayanıklı (resilient) stratejiler uyguladım:
* **Dinamik Bekleme Stratejileri:** Koda sabitlenmiş (hard-coded) kör beklemeler olan `time.sleep()` yerine, elementlerin tam olarak yüklendiğinden emin olmak ve veri çekme hızını maksimuma çıkarmak için Selenium'un `WebDriverWait` (Akıllı/Açık Beklemeler) özelliğini kullandım.
* **DOM Tutarsızlıklarının Yönetimi:** Veri çekme mantığını, değişken HTML yapılarını idare edebilecek şekilde güncelledim (örneğin; çıkış yılını, sitede "Yıl" veya "Yapım" gibi farklı etiketlerle yer alsa bile tespit edip çekebilecek bir yapı kurdum).
* **Veri Temizleme (Sanitization):** Çekilen karmaşık metinleri Pandas ve Regex kullanarak işledim; hassas arayüz filtrelemesi yapabilmek için metinleri doğru sayısal verilere (float/int) dönüştürdüm.
* **Sürekli Dağıtım (CI/CD Yaklaşımı):** Kesintisiz güncellemeler ve projenin canlıda kalması için GitHub deposunu Streamlit Cloud sunucularına bağladım.

## 📂 Proje Yapısı
* `FULLHD_VERİ_ÇEKME.py`: Temel otomasyon betiği. Sayfalar arasında gezinir, belirli elementleri bekler, HTML'i ayrıştırır ve veriyi dışa aktarır.
* `arayuz.py`: İnteraktif kaydırma çubukları ve arama işlevleri sunan Streamlit ön yüz uygulaması.
* `filmler.csv`: Veri çekme botu tarafından oluşturulan yapılandırılmış veritabanı.
* `requirements.txt`: Bulut sunucusunda (Streamlit Cloud) uygulamanın çalışması için gereken kütüphane listesi.

