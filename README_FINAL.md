# 🚁 BAYKAR İHA Tespit ve Takip Sistemi

YOLOv8 + ByteTrack ile İHA görüntülerinden nesne tespiti ve takibi.

## ✨ Özellikler

- ✅ **Nesne Tespiti**: 10 farklı sınıf (araç, insan, bisiklet, vb.)
- ✅ **Tracking**: ByteTrack ile çoklu nesne takibi
- ✅ **Gerçek Zamanlı**: Webcam/RTSP stream desteği
- ✅ **GPU Hızlandırma**: CUDA desteği
- ✅ **Kolay Kullanım**: Komut satırı ve Python API
- ✅ **Production Ready**: JSON çıktı, batch processing

## 🚀 Hızlı Başlangıç

### 1. Komut Satırı

```bash
# Ana programı çalıştır
python run_detection.py
```

### 2. Python Kodu

```python
from src.api.detection_api import UAVDetectionSystem

# Sistem oluştur
system = UAVDetectionSystem()

# Görüntü tespiti
result = system.detect_image('image.jpg')
print(f"Tespit: {result['count']} nesne")

# Video tracking
result = system.track_video('video.mp4')
print(f"Takip: {result['unique_tracks']} hedef")

# Gerçek zamanlı
system.detect_realtime(source=0)  # Webcam
```

## 📊 Model Performansı

```
Precision:  51.05% ✅
Recall:     41.19% ⚠️
mAP50:      41.62% ⚠️
mAP50-95:   24.86%
```

**En İyi Sınıflar:**
- Bicycle: 81.3%
- Awning-tricycle: 59.8%
- Car: 46.7%

## 📁 Proje Yapısı

```
📦 Proje
├─ 🏆 runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt  # Model
├─ 🚀 run_detection.py                    # Ana program
├─ 📚 src/api/detection_api.py            # API
├─ 📖 examples/usage_examples.py          # Örnekler
├─ 📋 USAGE_GUIDE_FINAL.md                # Detaylı kılavuz
└─ 📊 PROJECT_STATUS.md                   # Proje durumu
```

## 🎯 Kullanım Senaryoları

### Senaryo 1: Tek Görüntü

```bash
python run_detection.py
# Seçim: 1
# Görüntü: test.jpg
```

### Senaryo 2: Video Tracking

```bash
python run_detection.py
# Seçim: 2
# Video: video.mp4
```

### Senaryo 3: Gerçek Zamanlı

```bash
python run_detection.py
# Seçim: 3
# Kaynak: Webcam
```

### Senaryo 4: Toplu İşlem

```bash
python run_detection.py
# Seçim: 4
# Klasör: test_images/
```

## 🔧 Ayarlar

### Confidence Threshold

```python
# Daha hassas (daha fazla tespit)
system = UAVDetectionSystem(conf_threshold=0.15)

# Dengeli - ÖNERİLEN
system = UAVDetectionSystem(conf_threshold=0.25)

# Seçici (daha az yanlış alarm)
system = UAVDetectionSystem(conf_threshold=0.5)
```

### Device Seçimi

```python
# Otomatik (GPU varsa GPU)
system = UAVDetectionSystem(device='auto')

# GPU zorla
system = UAVDetectionSystem(device='0')

# CPU zorla
system = UAVDetectionSystem(device='cpu')
```

## 📚 Dokümantasyon

- **Kullanım Kılavuzu**: `USAGE_GUIDE_FINAL.md`
- **Kod Örnekleri**: `examples/usage_examples.py`
- **Proje Durumu**: `PROJECT_STATUS.md`
- **API Dokümantasyonu**: `src/api/detection_api.py`

## ⚡ Performans

**GPU (RTX 3050 Ti):**
- Görüntü: ~0.05s (20 FPS)
- Video: ~20-30 FPS

**CPU:**
- Görüntü: ~0.5s (2 FPS)
- Video: ~2-5 FPS

## 🎨 Tespit Edilen Sınıflar

| Sınıf | Açıklama |
|-------|----------|
| pedestrian | Yaya |
| people | İnsan grubu |
| bicycle | Bisiklet |
| car | Araba |
| van | Minibüs |
| truck | Kamyon |
| tricycle | Üç tekerlekli |
| awning-tricycle | Tenteli üç tekerlekli |
| bus | Otobüs |
| motor | Motosiklet |

## 🐛 Sorun Giderme

### GPU kullanılmıyor?

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

### Çok az tespit?

Confidence threshold'u düşürün: `conf_threshold=0.15`

### Çok fazla yanlış alarm?

Confidence threshold'u yükseltin: `conf_threshold=0.4`

## 📦 Gereksinimler

```
ultralytics>=8.0.0
opencv-python>=4.8.0
torch>=2.0.0
numpy>=1.24.0
```

## 🚀 Gelişmiş Kullanım

### REST API

```python
from flask import Flask, request, jsonify
from src.api.detection_api import UAVDetectionSystem

app = Flask(__name__)
system = UAVDetectionSystem()

@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    result = system.detect_image(file)
    return jsonify(result)
```

### Docker

```bash
docker build -t baykar-uav .
docker run -it --gpus all baykar-uav
```

### RTSP Stream

```python
system = UAVDetectionSystem()
system.detect_realtime(source='rtsp://ip:port/stream')
```

## 📈 Sonraki Adımlar

1. ✅ Model hazır ve çalışıyor
2. ⏳ Gerçek senaryolarda test et
3. ⏳ Gerekirse modeli iyileştir (`train_yolo_hybrid.py`)
4. ⏳ Production deployment (Docker, API)

## 🎓 Öğrenilenler

- YOLOv8 eğitimi ve optimizasyonu
- ByteTrack entegrasyonu
- GPU bellek yönetimi
- VisDrone veri seti
- Production deployment

## 📞 Hızlı Komutlar

```bash
# Model değerlendirme
python quick_evaluation.py

# Hızlı demo
python quick_demo.py

# Ana program
python run_detection.py

# Örnekler
python examples/usage_examples.py

# Model iyileştirme (gerekirse)
python src/training/train_yolo_hybrid.py
```

---

**🎯 Model hazır! Kullanıma başlayabilirsiniz.**

**Başarılar! 🚀**
