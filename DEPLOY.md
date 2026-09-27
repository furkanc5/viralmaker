# ViralMaker deploy

## GitHub Pages

1. GitHub repository ayarlarında **Settings > Pages > Source** olarak **GitHub Actions** seç.
2. `main` branch'ine push yap. `.github/workflows/deploy-pages.yml` siteyi otomatik yayınlar.

Arka plan silme işlemi `@imgly/background-removal` ile doğrudan ziyaretçinin tarayıcısında yapılır. Python API, `BACKGROUND_API_URL` veya ayrı bir sunucu gerekmez. İlk işlemde yaklaşık 40-80 MB model dosyası indirilir ve tarayıcı cache'ine alınır.

## Lisans notu

`@imgly/background-removal` AGPL lisanslıdır. Ticari veya kapalı kaynak bir kullanım planlanıyorsa IMG.LY lisans koşulları ayrıca incelenmelidir.
