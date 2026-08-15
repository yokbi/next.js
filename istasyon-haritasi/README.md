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
| `arac/olustur.py` | PDF → veri.json → index.html |
| `arac/harita_uret.py` | GeoJSON → harita.json |
| `arac/konum_uret.py` | GeoJSON → ilce_konum.json |
| `arac/sablon.html` | Sayfa şablonu (`__VERI__`, `__HARITA__` yer tutucuları) |

## Konum verisi

Kaynak listede koordinat yok, adresler de geocode edilmedi (bu ortamda geocoding
servislerine çıkış kapalı). Bunun yerine her istasyona **ilçesinin merkez
koordinatı** atanır:

- **2287 istasyon (%96,8)** ilçe merkezine oturur. İlçe merkezi olarak OSM'in
  `admin_centre` / `label` düğümü — yani gerçek kasaba merkezi — kullanılır;
  bu düğüm 974 ilçenin 211'inde var, kalanında ilçe poligonunun ağırlık merkezine
  düşülür.
- **75 istasyon** ilçesi eşleşmediği için il merkezinde kalır (büyükşehirlerde
  "Merkez" adlı bir ilçe bulunmadığı durumlar).

Pratik doğruluk kentsel ilçelerde yüksek, kırsalda düşüktür: Kadıköy 0,3 km,
Konak 0,9 km sapma verirken, dağlara kadar uzanan Alanya'da sapma 17 km'ye
çıkabiliyor. Bu yüzden uzaklıklar arayüzde `≈` ile gösteriliyor.

**Yol tarifi bu koordinatları kullanmaz** — adres metnini Google Haritalar'a
gönderir, adresi harita servisi kendi çözer. Yani navigasyon, koordinat
hassasiyetinden bağımsız olarak tam adrese gider.

İlçe koordinat tablosu (`ilce_konum.json`, 974 kayıt) şöyle üretilir:

```bash
curl -sSL -o il4.geojson  https://media.githubusercontent.com/media/izzetkalic/geojsons-of-turkey/master/geojsons/turkey-admin-level-4.geojson
curl -sSL -o ilce.geojson https://media.githubusercontent.com/media/izzetkalic/geojsons-of-turkey/master/geojsons/turkey-admin-level-6.geojson
python3 arac/konum_uret.py il4.geojson ilce.geojson
```

İlçeler ile eşleşirken adları normalleşir (Türkçe harfler sadeleşir), `Afyon →
Afyonkarahisar` gibi ad farkları eşanlam tablosundan çözülür, `Merkez` ise il
adını taşıyan ilçeye bağlanır.

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
