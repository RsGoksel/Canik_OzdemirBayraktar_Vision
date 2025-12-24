# Vision Assistant - Görme Engelliler İçin Görsel Asistan

## 📋 Proje Açıklaması

Vision Assistant, görme engelli kullanıcılar için geliştirilmiş akıllı bir görsel asistan uygulamasıdır. Google Gemini AI kullanarak görüntü analizi yapar ve sesli geri bildirim sağlar.

### 🎯 Ana Özellikler

1. **Raf Tarama**: Market raflarındaki ürünleri analiz eder, fiyat ve içerik bilgilerini sesli olarak bildirir
2. **Mağaza Navigasyonu**: Mağaza içinde yön talimatları verir ve kullanıcıyı yönlendirir
3. **Metin Okuma (OCR)**: Etiketlerdeki metinleri okur

### ✨ Erişilebilirlik Özellikleri

- 🔊 **Türkçe Sesli Geri Bildirim** (Text-to-Speech)
- 📳 **Titreşim Feedback** (Mobil cihazlarda)
- ⚙️ **Ayarlanabilir Konuşma Hızı**
- 🎨 **Yüksek Kontrastlı Arayüz**
- 🔘 **Büyük, Dokunmaya Uygun Butonlar**
- ⌨️ **Klavye Kısayolları** (Erişilebilirlik için)

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- Modern web tarayıcısı (Chrome, Firefox, Safari, Edge)
- Google Gemini API Key

### Backend Kurulumu

```bash
# Backend dizinine git
cd backend

# Sanal ortam oluştur (opsiyonel ama önerilir)
python -m venv venv

# Sanal ortamı aktifleştir
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### Frontend Kurulumu

Frontend için ek kurulum gerekmez. Statik HTML/CSS/JS dosyalarıdır.

## 🎮 Kullanım

### Uygulamayı Başlatma

```bash
# Backend dizininden FastAPI sunucusunu başlat
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Tarayıcıdan şu adrese gidin:
```
http://localhost:8000
```

### Mobil Cihazdan Erişim

Aynı ağdaki mobil cihazdan erişmek için:
```
http://<BILGISAYAR_IP>:8000
```

## 📱 Kullanım Kılavuzu

### 1. Raf Tarama Modu

1. Ana sayfadan "Raf Tarama" butonuna bas
2. Kamerayı rafa doğrult veya galeriden fotoğraf seç
3. Fotoğraf çek veya yükle
4. "Analiz Et" butonuna bas
5. Sesli geri bildirimi dinle

**Ne Öğrenirsin:**
- Rafta hangi ürünler var
- Ürünlerin fiyatları
- İçerik bilgileri (gramaj, adet)
- Ürünlerin konumu (üst/alt raf, sağ/sol)
- İndirim ve promosyon bilgileri

### 2. Mağaza Navigasyonu Modu

1. Ana sayfadan "Mağaza Navigasyonu" butonuna bas
2. Kamerayı mağaza içine doğrult
3. Fotoğraf çek
4. "Analiz Et" butonuna bas
5. Yön talimatlarını dinle

**Ne Öğrenirsin:**
- Bulunduğun alan (koridor, kasa, reyon)
- Yön talimatları (sağa/sola dön, ilerle, dur)
- Hangi ürünlerin nerede olduğu
- Engeller ve uyarılar

### 3. Metin Okuma Modu

1. Ana sayfadan "Metin Okuma" butonuna bas
2. Kamerayı metin içeren yüzeye doğrult
3. Fotoğraf çek
4. Metni sesli olarak dinle

## ⚙️ Ayarlar

### Konuşma Hızı
Sesli geri bildirimin hızını 0.5x - 2.0x arasında ayarlayabilirsin.

### Titreşim Geri Bildirimi
Buton basımlarında titreşim almak için aç/kapa.

### Otomatik Sesli Okuma
Sonuç ekranında otomatik olarak sesli okumayı aktif/deaktif et.

## 🛠️ Teknoloji Stack

### Backend
- **FastAPI**: Modern, hızlı Python web framework
- **Google Gemini AI**: Görüntü analizi ve yapay zeka
- **Pillow**: Görüntü işleme
- **Uvicorn**: ASGI sunucu

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Glassmorphism, gradients, animations
- **Vanilla JavaScript**: Kamera API, Speech Synthesis API
- **Web Speech API**: Türkçe text-to-speech
- **MediaDevices API**: Kamera erişimi

## 📂 Proje Yapısı

```
irfan_hoca/
├── backend/
│   ├── main.py              # FastAPI ana uygulama
│   ├── gemini_service.py    # Gemini AI entegrasyonu
│   └── requirements.txt     # Python bağımlılıkları
└── frontend/
    ├── index.html           # Ana HTML
    ├── style.css            # Stil dosyası
    └── app.js               # JavaScript logic
```

## 🔑 API Endpoints

### POST `/api/analyze-shelf`
Raf görüntüsünü analiz eder.

**Request:** Multipart form-data (image file)  
**Response:**
```json
{
  "success": true,
  "analysis": "Analiz sonucu...",
  "type": "shelf"
}
```

### POST `/api/analyze-navigation`
Mağaza navigasyon talimatları verir.

**Request:** Multipart form-data (image file)  
**Response:**
```json
{
  "success": true,
  "analysis": "Navigasyon talimatları...",
  "type": "navigation"
}
```

### POST `/api/extract-text`
Görüntüden metin çıkarır (OCR).

**Request:** Multipart form-data (image file)  
**Response:**
```json
{
  "success": true,
  "text": "Çıkarılan metin...",
  "type": "ocr"
}
```

## 🎨 Tasarım Özellikleri

- **Glassmorphism**: Modern cam efekti
- **Dark Theme**: Göz dostu karanlık tema
- **Smooth Animations**: Yumuşak geçişler
- **Gradient Backgrounds**: Dinamik arka planlar
- **High Contrast**: Yüksek kontrast erişilebilirlik
- **Large Touch Targets**: 44x44px minimum dokunma alanları

## 🔒 Güvenlik

- CORS yapılandırması (production'da origin belirtin)
- HTTPS kullanımı önerilir (özellikle kamera erişimi için)
- API key'i environment variable olarak saklanmalı (production için)

## 📱 Tarayıcı Uyumluluğu

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile Safari (iOS 14+)
- ✅ Chrome Mobile (Android 9+)

## 🚧 Gelecek Geliştirmeler

- [ ] PWA desteği (offline çalışma)
- [ ] Fotoğraf geçmişi
- [ ] Favoriler/Alışveriş listesi
- [ ] Çoklu dil desteği
- [ ] Sesli komut ile kontrol
- [ ] QR kod tarama
- [ ] Ürün karşılaştırma

## 📄 Lisans

Bu proje Samsun Canik Keşif Kampüsü dahilinde eğitim amaçlı geliştirilmiştir.

## 🤝 Katkıda Bulunma

İrfan GÜMÜŞ 
Kadir Göksel GÜNDÜZ

---

**Not**: Bu uygulama görme engelli kullanıcıların günlük yaşamlarını kolaylaştırmak amacıyla geliştirilmiştir. Sürekli iyileştirme ve geri bildirim için açığız.
