# İstasyon Bul

İstasyon listesi PDF'inden üretilen, telefonda kullanılmak üzere tasarlanmış tek
dosyalık istasyon arama sayfası. **2362 istasyon, 77 il.**

`index.html` kendi kendine yeter: veri içine gömülüdür, dış kaynak (CDN, font,
harita servisi) çağırmaz. Dosyayı açmak yeterli, sunucu gerekmez.

## Ne yapar

- **Arama** — il, ilçe, mahalle veya cadde adına göre; Türkçe karakter duyarsız
  (`kadikoy` yazınca Kadıköy bulunur).
- **İl / ilçe süzme** — istasyon sayıları seçeneklerde görünür.
- **Yakınımdakiler** — telefonun konumunu alır, istasyonları yakınlıktan uzağa sıralar.
- **İl dağılım haritası** — her il gerçek enlem/boylamına göre bir daire; daire
  büyüklüğü o ildeki istasyon sayısı. Daireye dokununca o il süzülür.
- **Yol tarifi** — adresi Google Haritalar'a yol tarifi olarak açar; başlangıç
  noktası telefonun anlık konumudur. "Haritada aç" adresi haritada gösterir.

## Kaynak veride olmayanlar

PDF'te yalnızca **İL, İLÇE, ADRES** kolonları var — istasyon adı ve şirket/marka
kolonu yok. Bu yüzden:

- Kart başlıkları adresten üretilir (öncelikle mahalle adı).
- Marka rozeti yalnızca markası adres metninde geçen **43** istasyonda görünür
  (ör. "... Cad. TOTAL PETROL NO:259"). Kalanlarda rozet çıkmaz.
- İstasyonların nokta koordinatı yoktur. Uzaklıklar **il merkezine** göre kabaca
  hesaplanır ve `≈` ile gösterilir; yol tarifi ise koordinattan değil, adres
  metninden alınır (haritalar adresi kendi çözer).

Adı ve şirketi gerçekten göstermek için kaynak listenin bu kolonları içeren bir
sürümü gerekir; geldiğinde `arac/olustur.py` içindeki ayıklama bu alanları da
taşıyacak şekilde genişletilebilir.

## Yeniden üretme

```bash
pip install pdfplumber
python3 arac/olustur.py istasyon_listesi.pdf [guncelleme_tarihi]
```

`veri.json` ve `index.html` yeniden yazılır. Ayıklama PDF'teki sabit sütun
konumlarına dayanır (İL x≈20, İLÇE x≈81, ADRES x≈149); listenin düzeni değişirse
`X_ILCE` / `X_ADRES` değerleri güncellenmelidir.

## Dosyalar

| Dosya | İçerik |
| --- | --- |
| `index.html` | Yayına hazır sayfa (veri gömülü) |
| `veri.json` | Ayıklanmış istasyon verisi |
| `arac/olustur.py` | PDF → veri.json → index.html |
| `arac/sablon.html` | Veri gömülmeden önceki sayfa şablonu (`__VERI__`) |
