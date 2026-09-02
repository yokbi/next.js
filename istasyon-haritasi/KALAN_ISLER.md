# Kalan işler — İstasyon Bul

Bu dosya, `istasyon-haritasi/` projesinde yapılmayı bekleyen işleri kaydeder.
Kod tarafında yarım kalmış bir şey yok: şablon derlenmiş (`index.html`,
`arac/sablon.html` ile senkron), TODO/FIXME yok, açık inceleme yorumu yok.
Aşağıdaki maddelerin tamamı **veri veya ağ erişimi** kısıtından bekliyor;
kısıt kalktığında yapılacak kod değişikliği her madde için ayrıca yazıldı.

Referans PR: yokbi/next.js#1 — `claude/gas-stations-map-site-dgerak`

## Mevcut durum (ölçüm)

| Ölçüt | Değer |
| --- | ---: |
| İstasyon | 2362 |
| İl | 77 (Ardahan, Artvin, Hakkari, Iğdır'da liste boş) |
| Markası okunabilen | 43 (%1,8) |
| Adı bilinen | 0 |
| Mahalle merkezine çözülen | 757 (%32,0) |
| İlçe merkezine çözülen | 1533 (%64,9) |
| İl merkezinde kalan | 72 (%3,0) |

## 1. İstasyon adı ve şirket bilgisi

**Sorun.** Kaynak PDF'te yalnızca İL, İLÇE, ADRES kolonları var. Kart başlıkları
adresten türetiliyor (`kisa_ad`, `arac/olustur.py:135`), marka ise yalnızca adres
metninde geçiyorsa yakalanıyor (`marka_bul`, `arac/olustur.py:127` + `MARKALAR`
tablosu satır 56). 2362 istasyonun 2319'unda rozet çıkmıyor.

**Çözüm yolları.**

- **A — kolonlu kaynak liste.** İstasyon adı ve şirket kolonlarını içeren bir PDF
  sürümü gelirse `pdf_oku` (satır 69) sütun sınırlarıyla çalıştığı için sadece
  `X_ILCE` / `X_ADRES` (satır 24) yanına yeni sütun eşikleri eklemek yeterli.
- **B — Overpass.** Türkiye'deki `amenity=fuel` noktaları çekilip listeyle
  eşleştirilir. OSM kayıtlarında `name`, `brand`, `operator` etiketleri bulunduğu
  için bu yol hem adı hem şirketi hem de gerçek koordinatı **tek sorguda** getirir;
  2. maddeyi de kapatır. Tercih edilen yol budur.

**Dokunulacak yerler.** Kayıt dizisi bugün 8 alan:
`[il, ilce, adres, kisa_ad, marka, lat, lon, kesinlik]`. Üretim
`veri_uret` (`arac/olustur.py:219`), tüketim tek noktada —
`arac/sablon.html:489-490`. Alan eklemek bu iki yeri değiştirmeyi gerektirir.

## 2. Koordinat hassasiyeti (sokak seviyesi)

**Sorun.** Kaynakta koordinat yok; her istasyona adresinden çözülebilen en dar
yönetsel birimin merkezi atanıyor (`konum_cozucu`, `arac/olustur.py:173`).
İstasyonların %68'i hâlâ ilçe veya il merkezinde duruyor. Kentsel ilçelerde sapma
kabul edilebilir (Kadıköy 0,3 km, Konak 0,9 km), kırsalda değil (Alanya 17 km).

**Not.** Yol tarifi bu koordinatları kullanmıyor — adres metnini Google
Haritalar'a gönderiyor. Yani hassasiyet yalnızca "yakınımdakiler" sıralamasını ve
harita nokta konumlarını etkiler, navigasyonu değil.

**Çözüm.** Adreslerin geocode edilmesi. Nominatim ile 2362 adres, saniyede 1
istek sınırında ≈40 dakika sürer. Overpass yolu (madde 1-B) seçilirse bu madde
kendiliğinden kapanır.

## 3. Engel: ağ erişimi

Sokak seviyesine inmenin önündeki tek engel çıkış politikası. Denenen ve
proxy'de **403** dönen sunucular: Nominatim, Photon, Overpass, Geoapify,
LocationIQ, OpenCage, OpenRouteService, TomTom, Geofabrik, GeoNames, HDX, İBB
açık veri. Erişilebilen kanallar yalnızca GitHub (raw + LFS), GitLab, npm, PyPI.

Bu kanallardan aranıp **işe yaramayan** kaynaklar (tekrar aranmasın diye):

| Kaynak | Neden olmadı |
| --- | --- |
| `melihkorkmaz/il-ilce-mahalle-geolocation-rest-api` | Koordinat yalnızca il/ilçe düzeyinde |
| `caglarsarikaya/turkey-geolocations` | Aynı — mahalle koordinatı yok |
| `ramdemi/TurkeyGeolocationRestApi` | Aynı |
| `bertugfahriozer/il_ilce_mahalle` | Aynı |
| npm `turkey-neighbourhoods` | Mahalle + posta kodu tam, koordinat yok; posta kodunu koordinata çevirecek erişilebilir kaynak da yok |
| `sahircansurmeli/istanbul-geojson` | 968 İstanbul mahallesi, ama ülke geneli OSM dosyası zaten kapsıyor — net kazanç 2 mahalle |
| TKGM mahalle servisi | Sorgu limiti düşük, sunucu kapalı |

**Yapılacak.** Ortam ayarlarında `overpass-api.de` (tercih) veya
`nominatim.openstreetmap.org` açılması isteniyor. Açıldığında madde 1 ve 2
birlikte kapatılabilir.

## 4. Küçük işler

- **Boş iller.** Ardahan, Artvin, Hakkari, Iğdır listede yok; haritada nötr renkte
  ve tıklanamaz çiziliyor. Kaynak listenin eksikliği mi yoksa gerçekten istasyon
  olmaması mı, doğrulanmadı.
- **PDF düzen bağımlılığı.** Ayıklama sabit sütun konumlarına dayanıyor
  (`X_ILCE=78`, `X_ADRES=145`, `arac/olustur.py:24`). Listenin düzeni değişirse bu
  değerler elle güncellenmeli; düzen değişimini fark eden bir doğrulama yok.
- **Güncelleme tarihi.** `main` içinde varsayılan olarak sabit yazılı
  (`arac/olustur.py`, `guncelleme` varsayılanı). Yeni PDF ile çalıştırırken
  argüman olarak geçilmezse eski tarih kalır.

## Yapılacak bir şey olmayanlar

Karışıklık olmasın diye: aşağıdakiler bilinçli tercih, eksik değil.

- Tek dosya / gömülü veri — dış kaynak (CDN, font, harita servisi) çağrılmaması
  kasıtlı; sayfa sunucusuz çalışsın diye.
- Test yok — proje statik bir sayfa ve üç yardımcı betikten ibaret; üretim
  betikleri çalıştırıldığında sayımları ekrana basıyor (`arac/olustur.py:263-268`).
