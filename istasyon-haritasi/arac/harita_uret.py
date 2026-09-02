"""GeoJSON il sınırlarını sadeleştirip harita.json (SVG path) üretir.

Kullanım:
    curl -o tr.json https://raw.githubusercontent.com/alpers/Turkey-Maps-GeoJSON/master/tr-cities.json
    python3 arac/harita_uret.py [tolerans] [geojson_yolu]
"""
import json
import math
import os
import sys

TOLERANS = float(sys.argv[1]) if len(sys.argv) > 1 else 0.012
EN, BOY, KENAR = 1000.0, 0.0, 8.0  # BOY orandan hesaplanır

geo = json.load(open(sys.argv[2] if len(sys.argv) > 2 else 'tr.json', encoding='utf-8'))
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
veri = json.load(open(os.path.join(KOK, 'veri.json'), encoding='utf-8'))
il_sira = {il['ad']: i for i, il in enumerate(veri['iller'])}

# --- ad eşleşmesi ---
geo_adlar = {f['properties']['name'] for f in geo['features']}
eslesmeyen = sorted(set(il_sira) - geo_adlar)
if eslesmeyen:
    print('EŞLEŞMEYEN (veri -> geojson):', eslesmeyen)
istasyonsuz = sorted(geo_adlar - set(il_sira))
print('istasyonu olmayan il:', istasyonsuz)


def rdp(noktalar, tol):
    """Douglas-Peucker sadeleştirme."""
    if len(noktalar) < 3:
        return noktalar
    ilk, son = noktalar[0], noktalar[-1]
    dx, dy = son[0] - ilk[0], son[1] - ilk[1]
    uzunluk = math.hypot(dx, dy)
    en_uzak, en_i = -1.0, 0
    for i in range(1, len(noktalar) - 1):
        p = noktalar[i]
        if uzunluk == 0:
            d = math.hypot(p[0] - ilk[0], p[1] - ilk[1])
        else:
            d = abs(dy * p[0] - dx * p[1] + son[0] * ilk[1] - son[1] * ilk[0]) / uzunluk
        if d > en_uzak:
            en_uzak, en_i = d, i
    if en_uzak > tol:
        sol = rdp(noktalar[:en_i + 1], tol)
        sag = rdp(noktalar[en_i:], tol)
        return sol[:-1] + sag
    return [ilk, son]


# --- sınırlar ---
xmin = ymin = 1e9
xmax = ymax = -1e9
for f in geo['features']:
    g = f['geometry']
    poligonlar = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
    for poly in poligonlar:
        for halka in poly:
            for lon, lat in halka:
                xmin, xmax = min(xmin, lon), max(xmax, lon)
                ymin, ymax = min(ymin, lat), max(ymax, lat)

K = math.cos(math.radians((ymin + ymax) / 2))  # enlem düzeltmesi
gen = (xmax - xmin) * K
yuk = ymax - ymin
olcek = (EN - 2 * KENAR) / gen
BOY = yuk * olcek + 2 * KENAR


def yansit(lon, lat):
    return (KENAR + (lon - xmin) * K * olcek,
            KENAR + (ymax - lat) * olcek)


sonuc = {}
toplam_nokta = 0
for f in geo['features']:
    ad = f['properties']['name']
    g = f['geometry']
    poligonlar = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
    parcalar = []
    for poly in poligonlar:
        for halka in poly:
            ekran = [yansit(lon, lat) for lon, lat in halka]
            sade = rdp(ekran, TOLERANS * olcek)
            if len(sade) < 4:
                continue
            toplam_nokta += len(sade)
            d = 'M' + ' '.join(
                ('%.1f %.1f' % (x, y)) for x, y in sade
            ).replace(' ', ',', 1)
            # "M x,y x2 y2 ..." yerine düzgün L komutları
            d = 'M%.1f %.1f' % sade[0] + ''.join('L%.1f %.1f' % (x, y) for x, y in sade[1:]) + 'Z'
            parcalar.append(d)
    sonuc[ad] = ''.join(parcalar)

cikti = {
    'en': round(EN, 1),
    'boy': round(BOY, 1),
    'kenar': [round(xmin, 4), round(ymin, 4), round(xmax, 4), round(ymax, 4)],
    'k': round(K, 6),
    'olcek': round(olcek, 4),
    'iller': sonuc,
}
hedef = os.path.join(KOK, 'harita.json')
json.dump(cikti, open(hedef, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('nokta:', toplam_nokta, '| boyut KB:',
      round(len(open(hedef, encoding='utf-8').read().encode()) / 1024, 1))
print('viewBox: 0 0 %.1f %.1f' % (EN, BOY))
