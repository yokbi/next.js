"""İstasyon listesi PDF'inden tek dosyalık siteyi üretir.

Kullanım:
    pip install pdfplumber
    python3 arac/olustur.py istasyon_listesi.pdf

Üretilenler (istasyon-haritasi/ altına):
    veri.json   ayıklanmış istasyon verisi
    index.html  veri gömülü, dışa bağımlılığı olmayan tek dosya
"""
import collections
import json
import os
import re
import sys

import pdfplumber

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SABLON = os.path.join(KOK, 'arac', 'sablon.html')

# PDF'te sütunlar sabit x konumlarında: İL 20, İLÇE 81, ADRES 149
X_ILCE, X_ADRES = 78, 145

IL_KOORD = {
    'ADANA': (37.00, 35.32), 'ADIYAMAN': (37.76, 38.28), 'AFYON': (38.76, 30.54),
    'AĞRI': (39.72, 43.05), 'AKSARAY': (38.37, 34.03), 'AMASYA': (40.65, 35.83),
    'ANKARA': (39.93, 32.86), 'ANTALYA': (36.90, 30.69), 'AYDIN': (37.85, 27.84),
    'BALIKESİR': (39.65, 27.89), 'BARTIN': (41.64, 32.34), 'BATMAN': (37.88, 41.13),
    'BAYBURT': (40.26, 40.22), 'BİLECİK': (40.14, 29.98), 'BİNGÖL': (38.88, 40.50),
    'BİTLİS': (38.40, 42.11), 'BOLU': (40.74, 31.61), 'BURDUR': (37.72, 30.29),
    'BURSA': (40.19, 29.06), 'ÇANAKKALE': (40.15, 26.41), 'ÇANKIRI': (40.60, 33.62),
    'ÇORUM': (40.55, 34.95), 'DENİZLİ': (37.78, 29.09), 'DİYARBAKIR': (37.91, 40.24),
    'DÜZCE': (40.84, 31.16), 'EDİRNE': (41.68, 26.56), 'ELAZIĞ': (38.68, 39.22),
    'ERZİNCAN': (39.75, 39.49), 'ERZURUM': (39.90, 41.27), 'ESKİŞEHİR': (39.78, 30.52),
    'GAZİANTEP': (37.07, 37.38), 'GİRESUN': (40.91, 38.39), 'GÜMÜŞHANE': (40.46, 39.48),
    'HATAY': (36.20, 36.16), 'ISPARTA': (37.76, 30.55), 'MERSİN': (36.81, 34.64),
    'İSTANBUL': (41.01, 28.98), 'İZMİR': (38.42, 27.14), 'KARS': (40.60, 43.09),
    'KASTAMONU': (41.39, 33.78), 'KAYSERİ': (38.73, 35.49), 'KIRIKKALE': (39.85, 33.52),
    'KIRKLARELİ': (41.74, 27.22), 'KIRŞEHİR': (39.15, 34.16), 'KİLİS': (36.72, 37.12),
    'KOCAELİ': (40.77, 29.95), 'KONYA': (37.87, 32.48), 'KÜTAHYA': (39.42, 29.99),
    'MALATYA': (38.35, 38.31), 'MANİSA': (38.61, 27.43), 'KAHRAMANMARAŞ': (37.58, 36.93),
    'MARDİN': (37.31, 40.74), 'MUĞLA': (37.22, 28.36), 'MUŞ': (38.73, 41.49),
    'NEVŞEHİR': (38.62, 34.71), 'NİĞDE': (37.97, 34.68), 'ORDU': (40.98, 37.88),
    'OSMANİYE': (37.07, 36.25), 'RİZE': (41.02, 40.52), 'SAKARYA': (40.78, 30.40),
    'SAMSUN': (41.29, 36.33), 'SİİRT': (37.93, 41.94), 'SİNOP': (42.03, 35.15),
    'SİVAS': (39.75, 37.02), 'ŞANLIURFA': (37.16, 38.79), 'ŞIRNAK': (37.52, 42.46),
    'TEKİRDAĞ': (40.98, 27.51), 'TOKAT': (40.31, 36.55), 'TRABZON': (41.00, 39.72),
    'TUNCELİ': (39.11, 39.55), 'UŞAK': (38.68, 29.41), 'VAN': (38.49, 43.38),
    'YALOVA': (40.65, 29.28), 'YOZGAT': (39.82, 34.80), 'ZONGULDAK': (41.46, 31.79),
    'KARABÜK': (41.20, 32.63), 'KARAMAN': (37.18, 33.22),
}

# Kaynak listede şirket kolonu yok; yalnızca adres metninde markası geçenler yakalanır.
MARKALAR = [
    ('TOTAL', 'Total'), ('OPET', 'Opet'), ('SHELL', 'Shell'),
    ('PETROL OFİSİ', 'Petrol Ofisi'), ('PETROL OFISI', 'Petrol Ofisi'),
    ('AYTEMİZ', 'Aytemiz'), ('SUNPET', 'Sunpet'), ('LUKOIL', 'Lukoil'),
    ('ALPET', 'Alpet'), ('TURKUAZ', 'Turkuaz'), ('KADOİL', 'Kadoil'),
    ('MOİL', 'Moil'), ('BP', 'BP'),
]

TR_KUCUK = str.maketrans('IİŞĞÜÖÇ', 'ıişğüöç')
TR_BUYUK = str.maketrans('ıişğüöç', 'IİŞĞÜÖÇ')
MAH_RE = re.compile(r'^(.*?)\s+(MAH\.?|MAHALLESİ|MAHALLESI|MH\.?|KÖYÜ|BELDESİ)\b')


def pdf_oku(yol):
    """Sütun x konumlarına göre İL / İLÇE / ADRES ayıklar."""
    satirlar = []
    with pdfplumber.open(yol) as pdf:
        for sayfa in pdf.pages:
            gruplar = collections.defaultdict(list)
            for w in sayfa.extract_words():
                gruplar[round(w['top'], 1)].append(w)
            for ust in sorted(gruplar):
                ws = sorted(gruplar[ust], key=lambda w: w['x0'])
                il = ' '.join(w['text'] for w in ws if w['x0'] < X_ILCE)
                ilce = ' '.join(w['text'] for w in ws if X_ILCE <= w['x0'] < X_ADRES)
                # Adres kelimeleri bazı satırlarda harf harf geliyor; boşluğu aradaki
                # mesafeden çıkarıyoruz.
                adres, onceki = '', None
                for w in [w for w in ws if w['x0'] >= X_ADRES]:
                    if onceki is not None and w['x0'] - onceki['x1'] > 0.8:
                        adres += ' '
                    adres += w['text']
                    onceki = w
                if not il.strip() or il.strip() == 'İL':
                    continue
                satirlar.append((il.strip(), ilce.strip(), re.sub(r'\s+', ' ', adres).strip()))
    return satirlar


TR_ALFABE = 'abcçdefgğhıijklmnoöprsştuüvyz'
TR_SIRA = {harf: i for i, harf in enumerate(TR_ALFABE)}


def tr_lower(s):
    return s.translate(TR_KUCUK).lower()


def sirala_anahtari(s):
    """Türk alfabesine göre sıralama anahtarı (Ağrı, Aksaray'dan önce gelir)."""
    return [TR_SIRA.get(ch, len(TR_ALFABE)) for ch in tr_lower(s)]


def baslik(s):
    """Türkçe'ye uygun başlık düzeni (I→ı, İ→i); sayı içeren parçalara dokunmaz."""
    parcalar = []
    for kelime in s.split(' '):
        if not kelime:
            continue
        if any(ch.isdigit() for ch in kelime):
            parcalar.append(kelime)
            continue
        kucuk = tr_lower(kelime)
        # "MAH.ATATÜRK" / "CEYHAN/ADANA" gibi bitişik yazımlarda her parça büyür
        parcalar.append(re.sub(
            r'(^|[./])([a-zçğıiöşü])',
            lambda m: m.group(1) + m.group(2).translate(TR_BUYUK).upper(),
            kucuk,
        ))
    return ' '.join(parcalar)


def marka_bul(adres):
    buyuk = adres.upper()
    for anahtar, ad in MARKALAR:
        if re.search(r'(?<![A-ZÇĞİÖŞÜ])' + re.escape(anahtar) + r'(?![A-ZÇĞİÖŞÜ])', buyuk):
            return ad
    return ''


def kisa_ad(adres):
    """Kart başlığı: adresteki en ayırt edici konum parçası."""
    m = MAH_RE.match(adres)
    if m and 1 <= len(m.group(1).split()) <= 4:
        return baslik(m.group(1).strip()) + ' Mah.'
    ilk = re.split(r'\s+(?:NO[:.]|NO\s|İÇ KAPI|,)', adres)[0]
    return baslik(' '.join(ilk.split()[:5]))


def veri_uret(satirlar, guncelleme):
    iller = sorted({s[0] for s in satirlar}, key=sirala_anahtari)
    eksik = [il for il in iller if il not in IL_KOORD]
    if eksik:
        raise SystemExit('Koordinatı bilinmeyen il: ' + ', '.join(eksik))
    sira = {ad: i for i, ad in enumerate(iller)}
    istasyonlar = []
    for il, ilce, adres in satirlar:
        adres = adres.strip(' ,')
        istasyonlar.append([sira[il], baslik(ilce), baslik(adres), kisa_ad(adres), marka_bul(adres)])
    return {
        'guncelleme': guncelleme,
        'iller': [{'ad': baslik(ad), 'lat': IL_KOORD[ad][0], 'lon': IL_KOORD[ad][1]} for ad in iller],
        'istasyonlar': istasyonlar,
    }


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    pdf_yolu = sys.argv[1]
    guncelleme = sys.argv[2] if len(sys.argv) > 2 else '27.07.2026'

    satirlar = pdf_oku(pdf_yolu)
    veri = veri_uret(satirlar, guncelleme)

    veri_metni = json.dumps(veri, ensure_ascii=False, separators=(',', ':'))
    if '</script>' in veri_metni:
        raise SystemExit('Veride </script> geçiyor, gömme güvenli değil.')

    with open(os.path.join(KOK, 'veri.json'), 'w', encoding='utf-8') as f:
        f.write(veri_metni)

    harita_metni = open(os.path.join(KOK, 'harita.json'), encoding='utf-8').read().strip()
    sablon = open(SABLON, encoding='utf-8').read()
    sayfa = sablon.replace('__VERI__', veri_metni).replace('__HARITA__', harita_metni)
    if '__VERI__' in sayfa or '__HARITA__' in sayfa:
        raise SystemExit('Şablondaki yer tutucular doldurulamadı.')
    with open(os.path.join(KOK, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(sayfa)

    markali = sum(1 for s in veri['istasyonlar'] if s[4])
    print('istasyon: %d | il: %d | markası okunabilen: %d'
          % (len(veri['istasyonlar']), len(veri['iller']), markali))


if __name__ == '__main__':
    main()
