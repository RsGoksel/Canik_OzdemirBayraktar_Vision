# 🚀 Vision Assistant - Deployment Guide

## Hızlı Deploy (Railway.app)

### 1. GitHub'a Yükle

```bash
# Zaten yapıldı! ✅
git init
git add .
git commit -m "Initial commit"

# GitHub'a push et
git remote add origin <GITHUB_REPO_URL>
git branch -M main
git push -u origin main
```

### 2. Railway.app'e Deploy

1. **Railway.app'e Git**: https://railway.app/
2. **Login** yap (GitHub ile)
3. **New Project** > **Deploy from GitHub repo**
4. Repository'yi seç: `vision-assistant` (veya ne adlandırdıysan)
5. **Add variables** kısmında:
   ```
   GOOGLE_API_KEY=AIzaSyDoOcXuFOnynSSFmNVM1zGGGFLTllVw_R4
   ```
6. Deploy'a bas!

✅ **5 dakikada hazır!**

---

## Alternative: Render.com

### 1. Render.com'a Git

1. https://render.com/ > Sign up (GitHub ile)
2. **New** > **Web Service**
3. GitHub repo'yu bağla
4. Ayarlar:
   - **Name**: `vision-assistant`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   ```
   GOOGLE_API_KEY=AIzaSyDoOcXuFOnynSSFmNVM1zGGGFLTllVw_R4
   ```
6. **Create Web Service**

✅ **İlk deploy 5-10 dakika sürer**

---

## Alternative: Fly.io

```bash
# Fly CLI kur
# Windows: iwr https://fly.io/install.ps1 -useb | iex

# Login
fly auth login

# Deploy
fly launch
# İsim: vision-assistant
# Region: fra (Frankfurt)

# Environment variable ekle
fly secrets set GOOGLE_API_KEY=AIzaSyDoOcXuFOnynSSFmNVM1zGGGFLTllVw_R4

# Deploy
fly deploy
```

---

## 📱 Kullanım

Deploy sonrası alacağın URL:
- **Railway**: `https://vision-assistant-production.up.railway.app`
- **Render**: `https://vision-assistant.onrender.com`
- **Fly.io**: `https://vision-assistant.fly.dev`

Bu URL'i hocana gönder! 🎯

---

## 🔧 Önemli Notlar

### Ücretsiz Limitleri

**Railway**:
- $5/ay ücretsiz credit
- Sleep yok (7/24 aktif kalır)
- 500 saat/ay

**Render**:
- Ücretsiz plan var
- 15 dakika inaktivite sonrası sleep
- İlk istek 30-60 saniye sürebilir

**Fly.io**:
- 3 VM ücretsiz
- Her biri 256MB RAM

### API Key Güvenliği

❌ **ASLA** API key'i GitHub'a pushlamayın!
✅ Her zaman environment variable kullanın

---

## 🐛 Sorun Giderme

### Deploy Başarısız

1. **Logs kontrol et**: Railway/Render dashboard'da
2. **Python version**: `runtime.txt` doğru mu?
3. **Dependencies**: `requirements.txt` tam mı?

### Uygulama Açılmıyor

1. **Environment variable**: API key doğru mu?
2. **Port**: Railway/Render otomatik `$PORT` kullanıyor mu?
3. **Logs**: Hata mesajı var mı?

### Kamera Çalışmıyor

- HTTPS gerekli! (Railway/Render otomatik sağlar)
- HTTP'de kamera izni verilmez

---

## 📞 Hocana Gönder

```
Merhaba Hocam,

Vision Assistant uygulamasını test edebilirsiniz:
🔗 https://[DEPLOY_URL]

Özellikler:
- Raf tarama (fiyat, içerik tespiti)
- Mağaza navigasyonu
- Metin okuma (OCR)
- Türkçe sesli geri bildirim

Mobil cihazdan kullanım önerilir!

Saygılarımla
```

---

## 🎉 Tebrikler!

Uygulamanız artık 7/24 erişilebilir! 🚀
