"""Yönetsel sınırlardan konum tabloları üretir.

Kullanım:
    curl -sSL -o il4.geojson   https://media.githubusercontent.com/media/izzetkalic/geojsons-of-turkey/master/geojsons/turkey-admin-level-4.geojson
    curl -sSL -o ilce.geojson  https://media.githubusercontent.com/media/izzetkalic/geojsons-of-turkey/master/geojsons/turkey-admin-level-6.geojson
    curl -sSL -o mah.geojson   https://media.githubusercontent.com/media/izzetkalic/geojsons-of-turkey/master/geojsons/turkey-admin-level-8.geojson
    python3 arac/konum_uret.py il4.geojson ilce.geojson [mah.geojson]

Çıktılar:
    ilce_konum.json     {"il|ilce": [enlem, boylam], ...}          974 ilçe
    mahalle_konum.json  {"ilce|mahalle": [enlem, boylam], ...}     ~4900 mahalle

İlçe merkezi olarak OSM'in admin_centre/label düğümü (gerçek kasaba merkezi)
kullanılır; düğüm yoksa en büyük parçanın ağırlık merkezine düşülür. Mahalleler
konumlarına göre ilçeye bağlanır, böylece aynı adı taşıyan mahalleler karışmaz.
"""
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR_KUCUK = str.maketrans('IİŞĞÜÖÇ', 'ıişğüöç')
# "Yenice Mahallesi" / "Akpınar Mah." / "Karaköy Köyü" -> çekirdek ad
EK_RE = re.compile(r'\s*(mahallesi|mahalle|mah\.?|mh\.?|köyü|koyu|beldesi)\s*$', re.I)


def norm(s):
    s = s.translate(TR_KUCUK).lower()
    s = (s.replace('ı', 'i').replace('ş', 's').replace('ğ', 'g')
          .replace('ü', 'u').replace('ö', 'o').replace('ç', 'c'))
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return ''.join(ch for ch in s if ch.isalnum())


def sade_mah(ad):
    """Mahalle adından tür ekini kırpar (üst üste gelen ekler dahil)."""
    onceki = None
    while onceki != ad:
        onceki = ad
        ad = EK_RE.sub('', ad).strip()
    return norm(ad)


def halkalar(geom):
    if geom['type'] == 'Polygon':
        return [geom['coordinates'][0]]
    if geom['type'] == 'MultiPolygon':
        return [poly[0] for poly in geom['coordinates']]
    return []


def alan_ve_merkez(halka):
    """Shoelace ile alan ve ağırlık merkezi."""
    a = cx = cy = 0.0
    for i in range(len(halka) - 1):
        x0, y0 = halka[i][0], halka[i][1]
        x1, y1 = halka[i + 1][0], halka[i + 1][1]
        capraz = x0 * y1 - x1 * y0
        a += capraz
        cx += (x0 + x1) * capraz
        cy += (y0 + y1) * capraz
    if abs(a) < 1e-12:
        xs = [p[0] for p in halka]
        ys = [p[1] for p in halka]
        return 0.0, (sum(xs) / len(xs), sum(ys) / len(ys))
    a *= 0.5
    return abs(a), (cx / (6 * a), cy / (6 * a))


def poligon_merkezi(geom):
    en_iyi = (-1.0, None)
    for halka in halkalar(geom):
        alan, merkez = alan_ve_merkez(halka)
        if alan > en_iyi[0]:
            en_iyi = (alan, merkez)
    return en_iyi[1]


def icinde_mi(nokta, halka):
    x, y = nokta
    icinde = False
    j = len(halka) - 1
    for i in range(len(halka)):
        xi, yi = halka[i][0], halka[i][1]
        xj, yj = halka[j][0], halka[j][1]
        if (yi > y) != (yj > y):
            if x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                icinde = not icinde
        j = i
    return icinde


def main():
    il_yolu = sys.argv[1] if len(sys.argv) > 1 else 'il4.geojson'
    ilce_yolu = sys.argv[2] if len(sys.argv) > 2 else 'ilce.geojson'

    # --- iller ---
    il_kutu = []
    for f in json.load(open(il_yolu, encoding='utf-8'))['features']:
        if f['properties'].get('admin_level') != '4':
            continue
        hs = halkalar(f['geometry'])
        if not hs:
            continue
        xs = [p[0] for h in hs for p in h]
        ys = [p[1] for h in hs for p in h]
        il_kutu.append((f['properties']['name'], min(xs), min(ys), max(xs), max(ys), hs))
    print('il poligonu:', len(il_kutu))

    def il_bul_tek(nokta):
        x, y = nokta
        for ad, x0, y0, x1, y1, hs in il_kutu:
            if x0 <= x <= x1 and y0 <= y <= y1:
                for h in hs:
                    if icinde_mi(nokta, h):
                        return ad
        return None

    def il_bul(geom, merkez):
        """İl ataması.

        İl ve ilçe sınırları aynı OSM anlık görüntüsünden geldiği için merkez
        noktası çözülüyorsa doğrudan ona güvenilir. Sınır noktalarıyla oylama
        yalnızca merkez hiçbir ile düşmediğinde (kıyı girintileri) devrededir;
        sınır noktaları iki ile birden değdiği için tek başına güvenilmez.
        """
        ad = il_bul_tek(merkez)
        if ad:
            return ad
        oy = defaultdict(int)
        for halka in halkalar(geom):
            adim = max(1, len(halka) // 40)
            for p in halka[::adim]:
                a = il_bul_tek((p[0], p[1]))
                if a:
                    oy[a] += 1
        if oy:
            return max(oy.items(), key=lambda kv: kv[1])[0]
        en_iyi, en_az = None, 1e9
        for ad, x0, y0, x1, y1, hs in il_kutu:
            d = ((x0 + x1) / 2 - merkez[0]) ** 2 + ((y0 + y1) / 2 - merkez[1]) ** 2
            if d < en_az:
                en_az, en_iyi = d, ad
        return en_iyi

    ilce_veri = json.load(open(ilce_yolu, encoding='utf-8'))['features']

    # --- ilçe merkezi düğümleri (admin_centre / label) ---
    merkez_dugum = {}
    for f in ilce_veri:
        if f['geometry']['type'] != 'Point':
            continue
        for r in f['properties'].get('@relations', []):
            etiket = r.get('reltags', {})
            if etiket.get('admin_level') == '6' and etiket.get('name'):
                merkez_dugum[r['rel']] = tuple(f['geometry']['coordinates'][:2])

    # --- ilçeler ---
    tablo = {}
    dugumle = 0
    for f in ilce_veri:
        p = f['properties']
        if p.get('admin_level') != '6' or not p.get('name'):
            continue
        if f['geometry']['type'] not in ('Polygon', 'MultiPolygon'):
            continue
        agirlik = poligon_merkezi(f['geometry'])
        if not agirlik:
            continue
        rel = p.get('@id', '')
        rel_no = int(rel.split('/')[1]) if '/' in rel else None
        merkez = merkez_dugum.get(rel_no)
        if merkez:
            dugumle += 1
        else:
            merkez = agirlik
        il = il_bul(f['geometry'], agirlik)
        tablo['%s|%s' % (norm(il), norm(p['name']))] = [round(merkez[1], 5), round(merkez[0], 5)]

    hedef = os.path.join(KOK, 'ilce_konum.json')
    json.dump(tablo, open(hedef, 'w', encoding='utf-8'), ensure_ascii=False,
              separators=(',', ':'), sort_keys=True)
    print('ilçe: %d (%d tanesi gerçek merkez düğümü) | %s' % (len(tablo), dugumle, hedef))

    if len(sys.argv) > 3:
        mahalle_uret(sys.argv[3], ilce_veri)


def mahalle_uret(mah_yolu, ilce_veri):
    """Mahalleleri konumlarına göre ilçeye bağlayıp tablo üretir.

    Aynı ad Türkiye'de yüzlerce kez geçtiği için (Cumhuriyet, Yeni, Merkez)
    anahtar ilçeyle birlikte tutulur; mahallenin ilçesi ad eşleşmesiyle değil,
    merkez noktasının ilçe poligonuna düşmesiyle belirlenir.
    """
    ilce_kutu = []
    for f in ilce_veri:
        p = f['properties']
        if p.get('admin_level') != '6' or not p.get('name'):
            continue
        if f['geometry']['type'] not in ('Polygon', 'MultiPolygon'):
            continue
        hs = halkalar(f['geometry'])
        if not hs:
            continue
        xs = [q[0] for h in hs for q in h]
        ys = [q[1] for h in hs for q in h]
        ilce_kutu.append((norm(p['name']), min(xs), min(ys), max(xs), max(ys), hs))

    def ilce_bul(nokta):
        x, y = nokta
        for ad, x0, y0, x1, y1, hs in ilce_kutu:
            if x0 <= x <= x1 and y0 <= y <= y1:
                for h in hs:
                    if icinde_mi(nokta, h):
                        return ad
        return None

    tablo = {}
    for f in json.load(open(mah_yolu, encoding='utf-8'))['features']:
        p = f['properties']
        ad = p.get('name')
        if not ad:
            # etiket düğümlerinde ad, bağlı olduğu ilişkinin etiketlerinde durur
            for r in p.get('@relations', []):
                etiket = r.get('reltags', {})
                if etiket.get('admin_level') == '8' and etiket.get('name'):
                    ad = etiket['name']
                    break
        if not ad:
            continue
        g = f['geometry']
        if g['type'] == 'Point':
            nokta = (g['coordinates'][0], g['coordinates'][1])
        elif g['type'] in ('Polygon', 'MultiPolygon'):
            nokta = poligon_merkezi(g)
        else:
            continue
        if not nokta:
            continue
        ilce = ilce_bul(nokta)
        if not ilce:
            continue
        anahtar = '%s|%s' % (ilce, sade_mah(ad))
        if anahtar not in tablo:
            tablo[anahtar] = [round(nokta[1], 5), round(nokta[0], 5)]

    hedef = os.path.join(KOK, 'mahalle_konum.json')
    json.dump(tablo, open(hedef, 'w', encoding='utf-8'), ensure_ascii=False,
              separators=(',', ':'), sort_keys=True)
    print('mahalle: %d | %s' % (len(tablo), hedef))


if __name__ == '__main__':
    main()
