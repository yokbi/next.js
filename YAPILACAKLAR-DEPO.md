# Yapılacaklar — depo düzeyi (yokbi/next.js)

> Bu dosya **deponun kendisiyle** ilgili işleri kaydeder.
> `istasyon-haritasi` projesinin **kendi içindeki** kalan işleri ayrı bir dosyada:
> [`istasyon-haritasi/KALAN_ISLER.md`](istasyon-haritasi/KALAN_ISLER.md)
> (o dosya bu denetimde kontrol edildi ve **doğru** bulundu — bkz. `DEPO-DURUMU.md` §2)

---

## F1 🟡 `istasyon-haritasi`'nı kendi deposuna taşıyın

**Sorun.** İstasyon Bul, Next.js ile **hiçbir teknik ilişkisi olmayan** bağımsız
bir proje: tek bir statik HTML dosyası + üç Python betiği. Şu anda 25.000
dosyalık bir framework fork'unun içinde duruyor.

Bunun somut maliyetleri:

- **Görünmezlik.** Deponun kök `readme.md`'si Next.js'i anlatıyor. Depoya giren
  biri (altı ay sonra siz dahil) projenizin varlığını fark etmiyor.
- **Klonlama maliyeti.** Next.js'in tüm geçmişi çekiliyor — yüzlerce MB, dakikalar.
  Oysa proje 900 KB.
- **Upstream riski.** İleride `git pull upstream canary` yaparsanız binlerce
  dosyalık bir merge'ün içinde kendi işiniz kayboluyor.
- **Yayınlama zorluğu.** Sayfayı GitHub Pages / Netlify'a koymak istediğinizde
  kök dizin framework kaynağı olduğu için yapılandırma gerekiyor.

**Yapılacak — yeni depo oluşturup taşıyın:**

```bash
# 1) Yeni bir depo açın (GitHub'da): örn. yokbi/istasyon-bul

# 2) Yalnızca proje klasörünü, geçmişiyle birlikte çıkarın
git clone https://github.com/yokbi/next.js /tmp/nextjs-fork
cd /tmp/nextjs-fork
git checkout canary
git subtree split --prefix=istasyon-haritasi -b istasyon-only

# 3) Yeni depoya gönderin
git push https://github.com/yokbi/istasyon-bul istasyon-only:main
```

`git subtree split`, o klasöre dokunan **6 commit'inizi de** korur — geçmiş
kaybolmaz.

**4) Sonrasında:** Yayınlamak isterseniz yeni depoda GitHub Pages'i açmanız
yeterli (Settings → Pages → Branch: `main` / root). Sayfa dış kaynak
çağırmadığı için hiçbir ek yapılandırma gerekmez ve doğrudan çalışır — üstelik
`https://` üzerinden servis edileceği için **konum izni sorunu da ortadan kalkar**
(bkz. `DEPO-DURUMU.md` §3'teki `file://` notu).

**5) Bu depoda:** Taşıma doğrulandıktan sonra `istasyon-haritasi/` klasörü
silinebilir ve fork temiz bir Next.js fork'u olarak kalır (ya da fork da
tamamen silinebilir — F3'e bakın).

---

## F2 🟢 Varsayılan dal `canary` — `main` değil

**Durum.** Fork olduğu için varsayılan dal upstream'in dalı: `canary`.
`git clone` bunu çeker. Bu bir hata değil, fork'un doğal sonucudur.

**Dikkat edilecek:** `main` varsayan komutlar, betikler veya CI yapılandırmaları
bu depoda çalışmaz. Örneğin `git push origin main` diye bir alışkanlığınız varsa
burada hata verir.

F1 yapılırsa yeni depo `main` kullanacağı için bu madde kendiliğinden kapanır.

---

## F3 🟢 Fork'un geleceğine karar verin

**Durum.** Fork `v16.0.2-canary.16` temel alınmış. Next.js canary **günde birkaç
kez** sürüm çıkarır, yani fork her gün biraz daha geride kalıyor.

Bu bugün bir sorun **değil** — framework koduna hiç dokunmadınız
(`DEPO-DURUMU.md` §4'te doğrulandı, `istasyon-haritasi/` dışında değişikliğiniz
yok) ve framework'ü kullanmıyorsunuz.

**F1 tamamlandıktan sonra seçenekler:**

- **A — Fork'u silin.** Next.js'e katkı vermeyi planlamıyorsanız fork'un bir
  işlevi kalmıyor. Depo listenizde 25.000 dosyalık bir yük olarak duruyor.
- **B — Arşivleyin.** Silmek istemiyorsanız salt-okunur yapın.
- **C — Tutun ve güncel tutun.** Yalnızca Next.js'e katkı vermeyi düşünüyorsanız
  anlamlı. O durumda upstream'i uzak olarak ekleyin:
  ```bash
  git remote add upstream https://github.com/vercel/next.js
  git fetch upstream
  git merge upstream/canary
  ```

**Öneri:** F1 yapıldıktan sonra **A**. Katkı vermek isterseniz o gün yeniden
fork'lamak birkaç saniye sürer.

---

## F4 🟢 Kök `readme.md`'ye dokunulmadı — bilinçli

**Not (yapılacak iş değil, karar kaydı).** Bu denetimde kök `readme.md`
**değiştirilmedi**, oysa diğer depolarda README yazıldı.

Sebebi: o dosya Vercel'in resmî Next.js README'sidir. Değiştirilirse
upstream'den her `merge`'de çakışır (conflict). Onun yerine
[`DEPO-DURUMU.md`](DEPO-DURUMU.md) adında ayrı bir dosya eklendi ve deponun
gerçekte ne olduğunu o anlatıyor.

F1 tamamlanıp proje kendi deposuna taşındığında, orada `istasyon-haritasi/README.md`
zaten kök README olarak doğru yere oturacak.

---

## Öncelik sırası önerisi

1. **F1** — projeyi kendi deposuna taşı *(en yüksek fayda; `git subtree split` ile geçmiş korunur)*
2. **F3** — taşıma doğrulandıktan sonra fork'u sil veya arşivle
3. **F2** — F1 ile kendiliğinden çözülür
