# Depo Durumu — yokbi/next.js

> **Bu dosya deponun kök `readme.md`'sinin yerine geçmez.** Kökteki `readme.md`
> Vercel'in Next.js framework'ünün resmî README'sidir ve öyle kalmalıdır —
> upstream ile birleştirme (merge) yaparken çakışmaması için ona dokunulmadı.
> Bu dosya, **sizin bu depoda ne yaptığınızı** anlatır.

**Denetim tarihi:** 2026-09-07 · **Varsayılan dal:** `canary` (⚠️ `main` değil)

---

## 1. Bu depo nedir?

İki şeydir, bir arada:

| | |
|---|---|
| **1. Fork** | [`vercel/next.js`](https://github.com/vercel/next.js) fork'u — `v16.0.2-canary.16` temel alınmış |
| **2. Kendi projeniz** | `istasyon-haritasi/` — **Türkiye akaryakıt istasyonu arama sayfası**. Next.js ile ilgisi yok, sadece bu depoda duruyor. |

> ### ⚠️ Sizin işiniz burada
> ```
> istasyon-haritasi/
> ```
> Deponun geri kalan **~25.000 dosyası** Next.js framework kaynağıdır ve size ait
> değildir. Bir şey aramaya `istasyon-haritasi/` klasöründen başlayın.

---

## 2. `istasyon-haritasi` — İstasyon Bul

İstasyon listesi PDF'inden üretilen, **telefonda kullanılmak üzere** tasarlanmış
**tek dosyalık** istasyon arama sayfası.

| Ölçüm | Değer | Doğrulandı |
|---|---:|:---:|
| İstasyon | 2362 | ✅ |
| İl | 77 | ✅ |
| Markası okunabilen | 43 (%1,8) | ✅ |
| Mahalle merkezine çözülen | 757 (%32,0) | ✅ |
| İlçe merkezine çözülen | 1533 (%64,9) | ✅ |
| İl merkezinde kalan | 72 (%3,0) | ✅ |
| İlçe koordinat tablosu | 974 ilçe | ✅ |
| Mahalle koordinat tablosu | 4944 mahalle | ✅ |
| Veri güncelleme tarihi | 27.07.2026 | ✅ |

Bu sayıların hepsi bu denetimde `veri.json`, `ilce_konum.json` ve
`mahalle_konum.json` dosyaları okunarak **yeniden sayıldı** ve
`istasyon-haritasi/README.md` ile `KALAN_ISLER.md`'de yazanlarla **birebir
tuttu.** Mevcut dokümantasyon doğrudur.

### Özellikler
Arama (Türkçe karakter duyarsız), il/ilçe süzme, "yakınımdakiler" (konumla
uzaklık sıralaması), gerçek il sınırlı Türkiye haritası (istasyon sayısına göre
boyalı), ile dokununca ilçe kırılımına yakınlaşma, Google Haritalar'a yol tarifi.

### Teknik özelliği
`index.html` **kendi kendine yeter** (341 KB): veri içine gömülü, hiçbir dış
kaynak (CDN, font, harita servisi) çağırmaz. **Sunucu gerekmez, `npm install`
gerekmez.** Dosyayı açmak yeterli.

---

## 3. Çalıştırma

### İstasyon Bul (sizin projeniz) — 3 saniye

```bash
./run-istasyon-haritasi-mac-intel.sh          # Intel Mac
./run-istasyon-haritasi-mac-apple-silicon.sh  # Apple Silicon
run-istasyon-haritasi-windows.bat             # Windows
```

Ya da doğrudan:

```bash
open istasyon-haritasi/index.html
```

**Bağımlılık yok, derleme yok, kurulum yok.** Yarın Intel Mac'te test etmek
istediğiniz şey buysa, tek yapmanız gereken dosyayı açmak.

> **Konum özelliği notu:** "Yakınımdakiler", tarayıcının Geolocation API'sini
> kullanır. Modern tarayıcılar bunu `file://` üzerinden **engelleyebilir**
> (güvenli bağlam şartı). Konum çalışmazsa betikler yerine yerel sunucu deneyin:
> ```bash
> cd istasyon-haritasi && python3 -m http.server 8080
> # sonra: http://localhost:8080/
> ```
> `localhost` güvenli bağlam sayılır ve konum izni sorulur.

### Next.js framework'ünün kendisi

Bunu çalıştırmanız **muhtemelen gerekmiyor** — burası sizin uygulamanız değil,
framework'ün kaynak kodu. Yine de gerekirse (Node ≥ 20, pnpm; ilk kurulum uzun
sürer ve Rust/Turbopack derlemesi ister):

```bash
corepack enable
pnpm install
pnpm build
```

Ayrıntı: `contributing.md`.

---

## 4. Dal envanteri

⚠️ **Varsayılan dal `canary`'dir, `main` değil.** `git clone` bunu çeker.

Bu depo upstream'in tüm dallarını taşıyor — **binlerce** dal var
(`01-02-Copy_58398`, `bgw/...`, `alexkirsz/...` gibi Vercel geliştiricilerinin
dalları). Bunların hiçbiri size ait değildir ve incelenmesi gerekmez.

**Size ait dallar:**

| Dal | Durum |
|---|---|
| `canary` | Varsayılan. Upstream + sizin 6 commit'iniz. |
| `claude/gas-stations-map-site-dgerak` | PR #1 — birleştirildi |
| `claude/remaining-work-code-xdoc7e` | PR #2 — birleştirildi |
| `claude/repo-audit-docs-e1dail` | Bu doküman turu |

**Sizin `canary` üzerindeki commit'leriniz** (upstream `v16.0.2-canary.16`'nın üstünde):

```
2c913dac  Add remaining-work notes for the station finder
592042f2  Açılışta konumu kendiliğinden iste
3e6b264c  Adresteki mahalle tanınan istasyonları mahalle merkezine taşı
6cea1d18  İstasyon konumlarını il merkezinden ilçe merkezine indir
4c62b364  Nokta dağılımı yerine gerçek Türkiye haritası göster
f04701c0  İstasyon listesi PDF'i için telefonda kullanılan arama sayfası ekle
```

Hepsi `istasyon-haritasi/` klasörüne dokunuyor. **Next.js framework kaynağında
hiçbir değişikliğiniz yok** — fork temiz.

---

## 5. Bulgular

### 🟡 F1 — Proje yanlış depoda duruyor
`istasyon-haritasi`, Next.js ile hiçbir teknik ilişkisi olmayan bağımsız bir
statik sayfadır (HTML + Python betikleri). 25.000 dosyalık bir framework fork'unun
içinde durması:

- Depoyu klonlamayı gereksiz yere ağırlaştırıyor
- Kök `readme.md` Next.js'i anlattığı için projenizi görünmez kılıyor
- Upstream'den `git pull` yaptığınızda gereksiz risk yaratıyor

→ `YAPILACAKLAR-DEPO.md` F1 (kendi deposuna taşıma adımları)

### 🟢 F2 — Varsayılan dal `canary`
Fork'un doğal sonucu, hata değil. Ama `main` bekleyen komutlar/CI şaşırır. → F2

### 🟢 F3 — Fork upstream'in gerisinde kalacak
`v16.0.2-canary.16` temel alınmış. Next.js canary günde birkaç kez sürüm çıkarır.
Bu bir sorun değil (framework kodunu kullanmıyorsunuz), ama depo büyüdükçe
git işlemleri yavaşlar. F1 çözülürse bu tamamen ortadan kalkar. → F3

---

## 6. Yarınki test için (Intel Mac)

```bash
git clone https://github.com/yokbi/next.js       # canary dalı gelir
cd next.js
./run-istasyon-haritasi-mac-intel.sh
```

> **Uyarı:** Bu klon büyüktür (Next.js'in tüm geçmişi). Sadece istasyon sayfasını
> denemek istiyorsanız çok daha hızlı yol:
> ```bash
> git clone --depth 1 https://github.com/yokbi/next.js
> ```

**Beklenen:** Tarayıcıda Türkiye haritası açılır, iller istasyon sayısına göre
boyalı. Arama kutusuna `kadikoy` yazınca (Türkçe karaktersiz) Kadıköy sonuçları
gelir. Bir ile dokununca ilçe kırılımına yakınlaşır.

**Test edilirken bakılacak:** Konum izni verildiğinde "yakınımdakiler" sıralaması
çalışıyor mu (`file://` kısıtı için yukarıdaki nota bakın).

---

Kalan işler (depo düzeyi): [`YAPILACAKLAR-DEPO.md`](YAPILACAKLAR-DEPO.md)
Kalan işler (proje içi): [`istasyon-haritasi/KALAN_ISLER.md`](istasyon-haritasi/KALAN_ISLER.md)
Proje dokümantasyonu: [`istasyon-haritasi/README.md`](istasyon-haritasi/README.md)
