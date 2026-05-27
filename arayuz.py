import streamlit as st
import pandas as pd  # <--- BU EKSİKTİ!
import google.generativeai as genai
import os

# Artık os.environ ile uğraşmana gerek yok, Streamlit bunu otomatik görüyor:
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# 1. Sayfa Tasarımı
st.set_page_config(page_title="Gelişmiş Film Robotum", layout="wide")
st.title("🎬 Benim Film Robotum (Yapay Zeka Destekli)")
st.markdown("Filtreleri kullanabilir veya **Yapay Zekaya nasıl bir film izlemek istediğini** söyleyebilirsin!")

# 2. Veriyi Yükleme
@st.cache_data
def veriyi_getir():
    df = pd.read_csv("filmler.csv")
    df['FHD Puanı'] = pd.to_numeric(df['FHD Puanı'], errors='coerce')
    df['IMDb Puanı'] = pd.to_numeric(df['IMDb Puanı'], errors='coerce') 
    df['Yıl'] = pd.to_numeric(df['Yıl'], errors='coerce')               
    
    df = df.dropna(subset=['Yıl'])
    df['Yıl'] = df['Yıl'].astype(int)
    return df

df = veriyi_getir()

# 3. Sol Menü (Filtreleme Seçenekleri)
st.sidebar.header("🔍 Gelişmiş Filtrele")

arama = st.sidebar.text_input("Film Adı Ara:")
tur_arama = st.sidebar.text_input("Tür Ara (Örn: Aksiyon):")

min_puan_imdb, max_puan_imdb = st.sidebar.slider(
    "IMDb Puan Aralığı", 
    min_value=0.0, max_value=10.0, value=(5.0, 10.0), step=0.1
)

min_yil_db = int(df['Yıl'].min())
max_yil_db = int(df['Yıl'].max())
yil_araligi = st.sidebar.slider(
    "Film Yılı Aralığı", 
    min_value=min_yil_db, 
    max_value=max_yil_db, 
    value=(min_yil_db, max_yil_db), 
    step=1
)

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

filtrelenmis_df = filtrelenmis_df[(filtrelenmis_df['IMDb Puanı'] >= min_puan_imdb) & (filtrelenmis_df['IMDb Puanı'] <= max_puan_imdb)]
filtrelenmis_df = filtrelenmis_df[(filtrelenmis_df['Yıl'] >= yil_araligi[0]) & (filtrelenmis_df['Yıl'] <= yil_araligi[1])]
filtrelenmis_df = filtrelenmis_df[(filtrelenmis_df['FHD Puanı'] >= min_puan_fhd) & (filtrelenmis_df['FHD Puanı'] <= max_puan_fhd)]

# --- YENİ: GEMINI İLE DOĞAL DİL ARAMA ---
st.divider()
st.subheader("🤖 Gemini Film Asistanına Sor")

kullanici_girdisi = st.text_area(
    "Nasıl bir film izlemek istiyorsun?", 
    placeholder="Bana uzayda geçen ama çok karanlık olmayan, sonu mutlu biten bir macera filmi öner...",
    key="film_arama_kutusu"
)

if st.button("Yapay Zekaya Sor"):
    if not kullanici_girdisi:
        st.warning("Lütfen önce nasıl bir film aradığınızı yazın.")
    else:
        with st.spinner('Gemini film veritabanını inceliyor...'):
            top_10_film = filtrelenmis_df.sort_values(by='IMDb Puanı', ascending=False).head(2000)
            
            film_listesi_metni = ""
            for index, row in top_10_film.iterrows():
                film_listesi_metni += f"- Film Adı: {row['Film Adı']}, Tür: {row['Tür']}, Yıl: {row['Yıl']}, IMDb: {row['IMDb Puanı']}, Link: {row['Link']}\n"
            
            try:
                hazir_mesaj = f"""

Sen profesyonel bir film eleştirmeni ve öneri robotusun.
Kullanıcı şu tarz bir film arıyor: "{kullanici_girdisi}"

Aşağıda benim veritabanımda bulunan popüler filmler yer alıyor:
{film_listesi_metni}

Bu listedeki filmler arasından kullanıcının isteğine EN UYGUN olanları seç (Kullanıcı kaç film istediyse o kadar, belirtmediyse en fazla 3 tane öner). 
Önerdiğin her film için, neden bu filmi izlemesi gerektiğini kullanıcının isteğine atıfta bulunarak 1-2 cümleyle açıkla ve sonuna filmin izleme linkini ekle. 
Eğer listede isteğe uygun HİÇBİR film yoksa, listeye en yakın olanları seçip nedenini belirt.

"""
                # İŞTE BURAYI SENİN YENİ MODELİNE GÖRE GÜNCELLEDİK!
                model = genai.GenerativeModel('gemini-2.5-flash')
                cevap = model.generate_content(hazir_mesaj)
                
                st.success("İşte Gemini'nin Senin İçin Seçtiği Film:")
                st.info(cevap.text)
            
            except Exception as e:
                st.error(f"Hata detayı: {e}")

st.divider()

# 5. Sonuçları Ekranda Gösterme
st.subheader(f"Listelenen Toplam Film Sayısı: {len(filtrelenmis_df)}")
st.dataframe(
    filtrelenmis_df[['Film Adı', 'Tür', 'Yıl', 'IMDb Puanı', 'FHD Puanı', 'Link']], 
    column_config={
        "Link": st.column_config.LinkColumn("İzleme Linki")
    },
    use_container_width=True
)

try:
                # ... model çağrısı ...
                cevap = model.generate_content(hazir_mesaj)
                st.success("İşte Gemini'nin Senin İçin Seçtiği Film:")
                st.info(cevap.text)
            
            except Exception as e:
                if "429" in str(e):
                    st.error("Günlük ücretsiz limitimizi doldurduk. Lütfen yarın tekrar deneyin!")
                else:
                    st.error(f"Bir hata oluştu: {e}")
