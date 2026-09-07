#!/usr/bin/env bash
#
# run-istasyon-haritasi-mac-intel.sh
#
# "İstasyon Bul" sayfasını açar — bu deponun içindeki SİZE AİT proje.
# (Deponun geri kalanı Vercel'in Next.js framework fork'udur; bkz. DEPO-DURUMU.md)
#
# Intel Mac (x86_64) için yazıldı; Apple Silicon ve Linux'ta da aynen çalışır.
#
# Kullanım:
#   ./run-istasyon-haritasi-mac-intel.sh            # dosyayı doğrudan açar (en hızlı)
#   ./run-istasyon-haritasi-mac-intel.sh --sunucu   # yerel sunucuyla açar
#
# NEDEN --sunucu seçeneği var:
#   Sayfanın "yakınımdakiler" özelliği tarayıcının Geolocation API'sini kullanır.
#   Modern tarayıcılar konum erişimini "güvenli bağlam" ile sınırlar ve file://
#   çoğu tarayıcıda güvenli bağlam SAYILMAZ. Konum çalışmazsa --sunucu ile açın;
#   localhost güvenli bağlam sayılır ve konum izni sorulur.
#
# Bağımlılık: yok. npm install / pnpm install GEREKMEZ.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJE_DIR="$SCRIPT_DIR/istasyon-haritasi"

BOLD="$(tput bold 2>/dev/null || true)"; RESET="$(tput sgr0 2>/dev/null || true)"
YELLOW="$(tput setaf 3 2>/dev/null || true)"; GREEN="$(tput setaf 2 2>/dev/null || true)"

if [[ ! -f "$PROJE_DIR/index.html" ]]; then
  echo "HATA: $PROJE_DIR/index.html bulunamadı." >&2
  echo "  Yanlış dalda olabilirsiniz. Varsayılan dal 'canary' (main DEĞİL):" >&2
  echo "    git checkout canary" >&2
  exit 1
fi

BOYUT="$(du -h "$PROJE_DIR/index.html" | cut -f1)"
echo "${BOLD}İstasyon Bul${RESET} — 2362 istasyon, 77 il  (index.html: $BOYUT, veri gömülü)"
echo

MOD="${1:-}"

if [[ "$MOD" == "--sunucu" ]]; then
  if ! command -v python3 >/dev/null 2>&1; then
    echo "HATA: python3 bulunamadı (--sunucu için gerekli)." >&2
    echo "  macOS: xcode-select --install" >&2
    exit 1
  fi
  PORT=8080
  if command -v lsof >/dev/null 2>&1 && lsof -i ":$PORT" >/dev/null 2>&1; then
    PORT=8081
  fi
  URL="http://localhost:${PORT}/"
  echo "${GREEN}==>${RESET} Yerel sunucu: $URL   (Ctrl+C ile durdurun)"
  echo "    Konum izni bu modda sorulur — 'yakınımdakiler' böyle test edilir."
  echo
  cd "$PROJE_DIR"
  python3 -m http.server "$PORT" >/dev/null 2>&1 &
  SRV=$!
  trap 'kill "$SRV" 2>/dev/null || true' EXIT INT TERM
  sleep 1
  command -v open >/dev/null 2>&1 && open "$URL" || echo "Tarayıcıda açın: $URL"
  wait "$SRV"
else
  echo "${GREEN}==>${RESET} Dosya doğrudan açılıyor (sunucusuz)."
  echo "${YELLOW}    Not:${RESET} 'yakınımdakiler' konum özelliği file:// üzerinden"
  echo "    çalışmayabilir. Çalışmazsa şunu deneyin:"
  echo "      ./$(basename "${BASH_SOURCE[0]}") --sunucu"
  echo
  if command -v open >/dev/null 2>&1; then
    open "$PROJE_DIR/index.html"
  else
    echo "Tarayıcıda açın: file://$PROJE_DIR/index.html"
  fi
fi
