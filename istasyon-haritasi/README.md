# İstasyon Bul

İstasyon listesi PDF'inden üretilen, telefonda kullanılmak üzere tasarlanmış tek
dosyalık istasyon arama sayfası. **2362 istasyon, 77 il.**

`index.html` kendi kendine yeter: veri içine gömülüdür, dış kaynak (CDN, font,
harita servisi) çağırmaz. Dosyayı açmak yeterli, sunucu gerekmez.

## Ne yapar

- **Arama** — il, ilçe, mahalle veya cadde adına göre; Türkçe karakter duyarsız
  (`kadikoy` yazınca Kadıköy bulunur).
- **İl / ilçe süzme** — istasyon sayıları seçeneklerde görünür.
- **Yakınımdakiler** — telefonun konumunu alır, istasyonları gerçek uzaklığa göre
  yakından uzağa sıralar ve her kartta ≈ km yazar.
- **Türkiye haritası** — açılışta gelen görünüm. Gerçek il sınırları çizilir, her
  il o ildeki istasyon sayısına göre boyanır (tek renk, açıktan koyuya).
  Aramada harita da yeniden boyanır, yani sonuçların hangi illerde toplandığı
  bir bakışta görünür.
- **İle dokununca yakınlaşma** — harita o ilin sınırlarına oturur, ilçe merkezleri
  istasyon sayısına göre büyüyen noktalar olarak çıkar. Noktaya dokunmak o ilçeyi
  süzer. Etiketler yalnızca çakışmayan ilçelere yazılır; kalanların adı dokununca
  başlıkta görünür. "Türkiye geneli" düğmesi görünümü sıfırlar.
- **Yol tarifi** — adresi Google Haritalar'a yol tarifi olarak açar; başlangıç
  noktası telefonun anlık konumudur. "Haritada aç" adresi haritada gösterir.

## Kaynak veride olmayanlar

PDF'te yalnızca **İL, İLÇE, ADRES** kolonları var — istasyon adı ve şirket/marka
kolonu yok. Bu yüzden:

- Kart başlıkları adresten üretilir (öncelikle mahalle adı).
- Marka rozeti yalnızca markası adres metninde geçen **43** istasyonda görünür
  (ör. "... Cad. TOTAL PETROL NO:259"). Kalanlarda rozet çıkmaz.
- İstasyonların nokta koordinatı yoktur; aşağıdaki "Konum verisi" bölümüne bakın.

Adı ve şirketi gerçekten göstermek için kaynak listenin bu kolonları içeren bir
sürümü gerekir; geldiğinde `arac/olustur.py` içindeki ayıklama bu alanları da
taşıyacak şekilde genişletilebilir.

## Yeniden üretme

```bash
pip install pdfplumber
python3 arac/olustur.py istasyon_listesi.pdf [guncelleme_tarihi]
```

`veri.json` ve `index.html` yeniden yazılır; `harita.json` olduğu gibi gömülür. Ayıklama PDF'teki sabit sütun
konumlarına dayanır (İL x≈20, İLÇE x≈81, ADRES x≈149); listenin düzeni değişirse
`X_ILCE` / `X_ADRES` değerleri güncellenmelidir.

## Dosyalar

| Dosya | İçerik |
| --- | --- |
| `index.html` | Yayına hazır sayfa (veri gömülü) |
| `veri.json` | Ayıklanmış istasyon verisi |
| `harita.json` | Sadeleştirilmiş il sınırları (SVG path) |
| `ilce_konum.json` | İlçe merkezi koordinatları (974 ilçe) |
| `mahalle_konum.json` | Mahalle merkezi koordinatları (4944 mahalle) |
| `arac/olustur.py` | PDF → veri.json → index.html |
| `arac/harita_uret.py` | GeoJSON → harita.json |
| `arac/konum_uret.py` | GeoJSON → ilce_konum.json + mahalle_konum.json |
| `arac/sablon.html` | Sayfa şablonu (`__VERI__`, `__HARITA__` yer tutucuları) |

## Konum verisi

Kaynak listede koordinat yok. Her istasyona, adresinden çözülebilen **en dar
yönetsel birimin** merkezi atanır:

| Kesinlik | İstasyon | Oran | Kaynak |
| --- | ---: | ---: | --- |
| Mahalle merkezi | 757 | %32,0 | OSM `admin_level=8` sınırları |
| İlçe merkezi | 1533 | %64,9 | OSM `admin_level=6`; 211 ilçede gerçek `admin_centre` düğümü |
| İl merkezi | 72 | %3,0 | İlçe eşleşmediğinde (büyükşehirde "Merkez" adresleri) |

Mahalle çözümü şöyle çalışır: adresin başındaki mahalle/köy adı ("Kıcak
Mahallesi ...") ekinden arındırılıp normalleştirilir ve **istasyonun ilçesiyle
birlikte** aranır. Aynı ad ülke genelinde yüzlerce kez geçtiği için (Cumhuriyet,
Yeni, Merkez) ilçe kısıtı şart; mahallenin ilçesi de ad eşleşmesiyle değil,
merkez noktasının ilçe poligonuna düşmesiyle belirlenir.

Ölçülen kazanç: mahalleye çözülen istasyonlar ilçe merkezinden **medyan 4,6 km**
(%90'lık dilimde 14 km) uzağa taşındı. Örnek: Sultanahmet'ten bakınca en yakın
istasyon artık Fatih/Cankurtaran'da ≈0 km çıkıyor, önceden Kadıköy ile Fatih
arasındaki fark görünmüyordu.

Kalan sapma kaynağı: mahalleye çözülemeyen 1533 istasyon ilçe merkezinde duruyor.
Kentsel ilçelerde bu iyi (Kadıköy 0,3 km, Konak 0,9 km), kırsalda kötü (dağlara
uzanan Alanya'da 17 km).

**Yol tarifi bu koordinatları kullanmaz** — adres metnini Google Haritalar'a
gönderir, adresi harita servisi kendi çözer. Yani navigasyon, koordinat
hassasiyetinden bağımsız olarak tam adrese gider.

### Neden sokak seviyesine inilemedi

Sokak/kapı numarası hassasiyeti için adreslerin geocode edilmesi gerekir. Bu
ortamdan çıkış politikası buna izin vermiyor: Nominatim, Photon, Overpass,
Geoapify, LocationIQ, OpenCage, OpenRouteService, TomTom, Geofabrik, GeoNames,
HDX ve İBB açık veri sunucularının hepsi proxy'de 403 dönüyor. Erişilebilen tek
kanallar GitHub (raw + LFS), GitLab, npm ve PyPI.

Bu kanallardan aranan ve **işe yaramayan** kaynaklar:

- Ülke geneli mahalle koordinatı: `melihkorkmaz/il-ilce-mahalle-geolocation-rest-api`,
  `caglarsarikaya/turkey-geolocations`, `ramdemi/TurkeyGeolocationRestApi`,
  `bertugfahriozer/il_ilce_mahalle` — hepsinde koordinat yalnızca il/ilçe düzeyinde.
- npm `turkey-neighbourhoods`: ülke geneli mahalle + posta kodu listesi tam, ama
  koordinat yok. Posta kodunu koordinata çevirecek erişilebilir bir kaynak da yok
  (GeoNames posta kodu dosyası kapalı).
- `sahircansurmeli/istanbul-geojson`: İstanbul'un 968 mahallesi (dosya bozuk JSON,
  onarılabiliyor) — ancak ülke geneli OSM dosyası İstanbul'u zaten kapsadığı için
  yalnızca 2 yeni mahalle ekliyor.
- TKGM'nin mahalle servisi: sorgu limiti düşük ve sunucu kapalı.

Sokak seviyesine çıkmanın tek yolu bir geocoding sunucusuna izin verilmesi. Ortam
ayarlarında `nominatim.openstreetmap.org` (saniyede 1 istek, 2362 adres ≈ 40
dakika) veya `overpass-api.de` açılırsa:

- Nominatim ile adresler doğrudan koordinata çevrilebilir.
- Overpass ile Türkiye'deki `amenity=fuel` noktaları çekilip listeyle eşleştirilebilir;
  bu aynı zamanda **eksik olan istasyon adı ve şirket bilgisini de** getirir,
  çünkü OSM kayıtlarında `name`, `brand` ve `operator` etiketleri bulunur.

İkincisi tek sorguyla hem konumu hem kimliği çözdüğü için daha değerli.

### Tabloların üretimi

```bash
curl -sSL -o il4.geojson  https://media.githubusercontent.com/media/izzetkalic/geojsons-of-turkey/master/geojsons/turkey-admin-level-4.geojson
curl -sSL -o ilce.geojson https://media.githubusercontent.com/media/izzetkalic/geojsons-of-turkey/master/geojsons/turkey-admin-level-6.geojson
curl -sSL -o mah.geojson  https://media.githubusercontent.com/media/izzetkalic/geojsons-of-turkey/master/geojsons/turkey-admin-level-8.geojson
python3 arac/konum_uret.py il4.geojson ilce.geojson mah.geojson
```

`ilce_konum.json` (974 ilçe) ve `mahalle_konum.json` (4944 mahalle) yazılır.
Eşleşmede adlar normalleşir, `Afyon → Afyonkarahisar` gibi farklar eşanlam
tablosundan çözülür, `Merkez` il adını taşıyan ilçeye bağlanır.

## Harita verisi

İl sınırları [alpers/Turkey-Maps-GeoJSON](https://github.com/alpers/Turkey-Maps-GeoJSON)
veri kümesinden alınıp Douglas-Peucker ile sadeleştirildi (~1 km tolerans, 46 KB)
ve enlem düzeltmeli eş dikdörtgen izdüşümle SVG path'e çevrildi. Sınırların
yeniden üretimi `arac/harita_uret.py` ile yapılır:

```bash
curl -o tr.json https://raw.githubusercontent.com/alpers/Turkey-Maps-GeoJSON/master/tr-cities.json
python3 arac/harita_uret.py 0.012
```

Ardahan, Artvin, Hakkari ve Iğdır'da listede istasyon yok; bu iller haritada
nötr renkte ve tıklanamaz durumda çizilir.
