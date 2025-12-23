// Global State
let currentMode = '';
let capturedImage = null;
let camera = null;
let settings = {
    voiceSpeed: 1.0,
    vibration: true,
    autoSpeak: true
};

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    setupEventListeners();
    checkBrowserSupport();
});

// Check Browser Support
function checkBrowserSupport() {
    if (!('mediaDevices' in navigator)) {
        console.warn('Camera API not supported');
    }

    if (!('speechSynthesis' in window)) {
        console.warn('Speech Synthesis not supported');
    }

    // Request notification permission for better UX
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Voice speed slider
    const voiceSpeedSlider = document.getElementById('voiceSpeed');
    const voiceSpeedValue = document.getElementById('voiceSpeedValue');

    voiceSpeedSlider.addEventListener('input', (e) => {
        settings.voiceSpeed = parseFloat(e.target.value);
        voiceSpeedValue.textContent = settings.voiceSpeed.toFixed(1) + 'x';
        saveSettings();
    });

    // Vibration toggle
    document.getElementById('vibration').addEventListener('change', (e) => {
        settings.vibration = e.target.checked;
        saveSettings();
        if (e.target.checked) vibrate(50);
    });

    // Auto speak toggle
    document.getElementById('autoSpeak').addEventListener('change', (e) => {
        settings.autoSpeak = e.target.checked;
        saveSettings();
    });
}

// Mode Selection
function selectMode(mode) {
    currentMode = mode;
    vibrate(30);

    // Update camera title based on mode
    const title = {
        'shelf': 'Raf Tarama',
        'navigation': 'Mağaza Navigasyonu',
        'ocr': 'Metin Okuma'
    };
    document.getElementById('cameraTitle').textContent = title[mode];

    // Update instruction text
    const instruction = {
        'shelf': 'Kamerayı rafa doğrultun ve fotoğraf çekin',
        'navigation': 'Kamerayı mağaza içine doğrultun',
        'ocr': 'Kamerayı metin içeren yüzeye doğrultun'
    };
    document.getElementById('instructionText').textContent = instruction[mode];

    showScreen('cameraScreen');
    initCamera();
}

// Screen Management
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

function goHome() {
    vibrate(30);

    // Stop any ongoing speech
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }

    stopCamera();
    capturedImage = null;
    currentMode = '';
    showScreen('homeScreen');

    // Reset camera screen
    document.getElementById('preview').innerHTML = '';
    document.getElementById('preview').classList.remove('active');
    document.getElementById('analyzeBtn').style.display = 'none';
    document.getElementById('captureBtn').style.display = 'flex';
}

// Camera Functions
async function initCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'environment',
                width: { ideal: 1920 },
                height: { ideal: 1080 }
            }
        });

        const videoElement = document.getElementById('camera');
        videoElement.srcObject = stream;
        camera = stream;

    } catch (error) {
        console.error('Camera access error:', error);
        speak('Kamera erişimi sağlanamadı. Lütfen izinleri kontrol edin.');
        showNotification('Kamera hatası', 'Kamera erişimi için izin gerekli');
    }
}

function stopCamera() {
    if (camera) {
        camera.getTracks().forEach(track => track.stop());
        camera = null;
    }
}

function capturePhoto() {
    vibrate(50);

    const video = document.getElementById('camera');
    const canvas = document.getElementById('canvas');
    const preview = document.getElementById('preview');

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw video frame to canvas
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert to blob
    canvas.toBlob((blob) => {
        capturedImage = blob;

        // Show preview
        const img = document.createElement('img');
        img.src = URL.createObjectURL(blob);
        preview.innerHTML = '';
        preview.appendChild(img);
        preview.classList.add('active');

        // Hide camera, show analyze button
        video.style.display = 'none';
        stopCamera();

        document.getElementById('captureBtn').style.display = 'none';
        document.getElementById('analyzeBtn').style.display = 'flex';

        speak('Fotoğraf çekildi. Analiz etmek için butona basın.');
    }, 'image/jpeg', 0.9);
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    vibrate(50);

    capturedImage = file;

    // Show preview
    const preview = document.getElementById('preview');
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    preview.innerHTML = '';
    preview.appendChild(img);
    preview.classList.add('active');

    // Hide camera
    const video = document.getElementById('camera');
    video.style.display = 'none';
    stopCamera();

    document.getElementById('captureBtn').style.display = 'none';
    document.getElementById('analyzeBtn').style.display = 'flex';

    speak('Fotoğraf seçildi. Analiz etmek için butona basın.');
}

function retakePhoto() {
    vibrate(30);

    const video = document.getElementById('camera');
    const preview = document.getElementById('preview');

    preview.innerHTML = '';
    preview.classList.remove('active');
    video.style.display = 'block';

    document.getElementById('analyzeBtn').style.display = 'none';
    document.getElementById('captureBtn').style.display = 'flex';

    capturedImage = null;

    initCamera();
    showScreen('cameraScreen');
}

// Analysis Functions
async function analyzeImage() {
    if (!capturedImage) {
        speak('Lütfen önce bir fotoğraf çekin');
        return;
    }

    // Stop any ongoing speech before starting analysis
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }

    vibrate(30);
    showLoading(true);

    try {
        const formData = new FormData();
        formData.append('file', capturedImage, 'image.jpg');

        let endpoint = '';
        switch (currentMode) {
            case 'shelf':
                endpoint = `${API_BASE_URL}/analyze-shelf`;
                break;
            case 'navigation':
                endpoint = `${API_BASE_URL}/analyze-navigation`;
                break;
            case 'ocr':
                endpoint = `${API_BASE_URL}/extract-text`;
                break;
        }

        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        showLoading(false);

        if (data.success) {
            displayResult(data.analysis || data.text);
            vibrate([50, 100, 50]); // Success pattern
        } else {
            throw new Error('Analysis failed');
        }

    } catch (error) {
        console.error('Analysis error:', error);
        showLoading(false);
        speak('Analiz sırasında bir hata oluştu. Lütfen tekrar deneyin.');
        showNotification('Hata', 'Analiz başarısız oldu');
        vibrate([100, 50, 100, 50, 100]); // Error pattern
    }
}

function displayResult(text) {
    const resultText = document.getElementById('resultText');
    resultText.textContent = text;

    showScreen('resultScreen');

    // Auto speak if enabled
    if (settings.autoSpeak) {
        setTimeout(() => speakResult(), 500);
    }
}

// Text-to-Speech
function speak(text) {
    if ('speechSynthesis' in window) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'tr-TR';
        utterance.rate = settings.voiceSpeed;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        window.speechSynthesis.speak(utterance);
    }
}

function speakResult() {
    const resultText = document.getElementById('resultText').textContent;
    if (resultText) {
        vibrate(30);

        // Stop any ongoing speech first
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }

        // Wait a bit then speak
        setTimeout(() => speak(resultText), 100);
    }
}

// Settings
function toggleSettings() {
    vibrate(30);

    // Stop speech when opening settings
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }

    const panel = document.getElementById('settingsPanel');
    panel.classList.toggle('active');
}

function loadSettings() {
    const saved = localStorage.getItem('visionAssistantSettings');
    if (saved) {
        settings = JSON.parse(saved);

        document.getElementById('voiceSpeed').value = settings.voiceSpeed;
        document.getElementById('voiceSpeedValue').textContent = settings.voiceSpeed.toFixed(1) + 'x';
        document.getElementById('vibration').checked = settings.vibration;
        document.getElementById('autoSpeak').checked = settings.autoSpeak;
    }
}

function saveSettings() {
    localStorage.setItem('visionAssistantSettings', JSON.stringify(settings));
}

// Utility Functions
function vibrate(pattern) {
    if (settings.vibration && 'vibrate' in navigator) {
        navigator.vibrate(pattern);
    }
}

function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.classList.add('active');
    } else {
        overlay.classList.remove('active');
    }
}

function showNotification(title, body) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, { body, icon: '/static/icon.png' });
    }
}

// PWA Support (for future offline capability)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Service worker registration can be added here for offline support
        console.log('PWA support available');
    });
}

// Keyboard Shortcuts for Accessibility
document.addEventListener('keydown', (e) => {
    // Space or Enter to capture when on camera screen
    if ((e.key === ' ' || e.key === 'Enter') &&
        document.getElementById('cameraScreen').classList.contains('active')) {
        e.preventDefault();
        if (capturedImage) {
            analyzeImage();
        } else {
            capturePhoto();
        }
    }

    // Escape to go home
    if (e.key === 'Escape') {
        goHome();
    }
});

// Prevent accidental navigation
window.addEventListener('beforeunload', (e) => {
    if (capturedImage && !document.getElementById('resultScreen').classList.contains('active')) {
        e.preventDefault();
        e.returnValue = '';
        return '';
    }
});
