@echo off
REM run-istasyon-haritasi-windows.bat
REM
REM "Istasyon Bul" sayfasini acar - bu deponun icindeki SIZE AIT proje.
REM (Deponun geri kalani Vercel'in Next.js framework fork'udur; bkz. DEPO-DURUMU.md)
REM
REM Kullanim:
REM   run-istasyon-haritasi-windows.bat            dosyayi dogrudan acar
REM   run-istasyon-haritasi-windows.bat --sunucu   yerel sunucuyla acar
REM
REM NEDEN --sunucu: "yakinimdakiler" ozelligi Geolocation API kullanir ve
REM tarayicilar konumu "guvenli baglam" ile sinirlar; file:// cogu tarayicida
REM guvenli baglam SAYILMAZ. Konum calismazsa --sunucu ile acin.
REM
REM Bagimlilik: yok. npm install / pnpm install GEREKMEZ.

setlocal
cd /d "%~dp0"

if not exist "istasyon-haritasi\index.html" (
  echo HATA: istasyon-haritasi\index.html bulunamadi.
  echo   Yanlis dalda olabilirsiniz. Varsayilan dal 'canary' ^(main DEGIL^):
  echo     git checkout canary
  pause
  exit /b 1
)

echo Istasyon Bul - 2362 istasyon, 77 il ^(veri gomulu^)
echo.

if "%1"=="--sunucu" goto sunucu

echo ==^> Dosya dogrudan aciliyor ^(sunucusuz^).
echo     Not: 'yakinimdakiler' konum ozelligi file:// uzerinden calismayabilir.
echo     Calismazsa: run-istasyon-haritasi-windows.bat --sunucu
echo.
start "" "istasyon-haritasi\index.html"
goto son

:sunucu
where python >nul 2>&1
if errorlevel 1 (
  echo HATA: python bulunamadi ^(--sunucu icin gerekli^).
  echo   https://www.python.org/downloads/windows/
  pause
  exit /b 1
)
echo ==^> Yerel sunucu: http://localhost:8080/   ^(Ctrl+C ile durdurun^)
echo     Konum izni bu modda sorulur.
echo.
start "" "http://localhost:8080/"
cd istasyon-haritasi
python -m http.server 8080

:son
