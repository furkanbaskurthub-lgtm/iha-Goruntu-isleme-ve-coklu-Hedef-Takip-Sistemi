# BAYKAR İHA Tespit Sistemi - Kullanım Kılavuzu

## 🚀 Hızlı Başlangıç

### 1. Basit Kullanım (Komut Satırı)

```bash
# Ana programı çalıştır
python run_detection.py
```

Menüden seçim yap:
- 1: Tek görüntü tespiti
- 2: Video tracking
- 3: Gerçek zamanlı (webcam/stream)
- 4: Toplu işlem (klasör)

### 2. Python Kodunda Kullanım

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
```

---

## 📋 Detaylı Kullanım

### Görüntü Tespiti

```python
from src.api.detection_api import UAVDetectionSystem

# Sistem oluştur
system = UAVDetectionSystem(
    model_path='runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt',
    conf_threshold=0.25,  # Confidence eşiği (0.1-0.9)
    iou_threshold=0.5,    # NMS IoU eşiği
    device='auto'         # 'auto', '0' (GPU), 'cpu'
)

# Tespit yap
result = system.detect_image(
    image_path='test.jpg',
    save_result=True,      # Sonucu kaydet
    output_dir='outputs'   # Çıktı klasörü
)

# Sonuçlar
print(f"Tespit sayısı: {result['count']}")
print(f"İşlem süresi: {result['processing_time']:.3f}s")
print(f"Kaydedilen: {result['saved_image']}")

# Detaylar
for det in result['detections']:
    print(f"{det['class']}: {det['confidence']:.2f} @ {det['center']}")
```

### Video Tracking

```python
# Video işle
result = system.track_video(
    video_path='video.mp4',
    save_result=True,
    output_dir='outputs',
    show_progress=True
)

# Sonuçlar
print(f"Frame sayısı: {result['total_frames']}")
print(f"Toplam tespit: {result['total_detections']}")
print(f"Takip edilen: {result['unique_tracks']}")
print(f"İşlem hızı: {result['fps']:.1f} FPS")
```

### Gerçek Zamanlı Tespit

```python
# Webcam
system.detect_realtime(source=0)

# RTSP stream
system.detect_realtime(source='rtsp://username:password@ip:port/stream')

# Video dosyası (gerçek zamanlı görüntüleme)
system.detect_realtime(source='video.mp4')
```

### Hedef Bilgisi Alma

```python
# Görüntüde tespit yap
result = system.detect_image('image.jpg')

# Belirli sınıftaki hedefleri al
cars = system.get_target_info(result['detections'], 'car')
trucks = system.get_target_info(result['detections'], 'truck')

print(f"Araç sayısı: {len(cars)}")

# İlk aracın bilgileri
if cars:
    car = cars[0]
    print(f"Konum: {car['position']}")
    print(f"Güven: {car['confidence']:.2f}")
    print(f"Boyut: {car['size']}")
```

---

## 🎯 Kullanım Senaryoları

### Senaryo 1: Tek Görüntü Analizi

```bash
python run_detection.py
# Seçim: 1
# Görüntü yolu: test_images/drone_view.jpg
```

Sonuç:
- Tespit edilen nesneler görüntü üzerinde işaretlenir
- JSON dosyası oluşturulur (koordinatlar, sınıflar, güven skorları)
- `outputs/` klasörüne kaydedilir

### Senaryo 2: Video Analizi ve Tracking

```bash
python run_detection.py
# Seçim: 2
# Video yolu: videos/uav_flight.mp4
```

Sonuç:
- Her frame'de tespit yapılır
- Nesneler frame'ler arası takip edilir (ByteTrack)
- Her nesneye unique ID atanır
- İşlenmiş video `outputs/tracked_*.mp4` olarak kaydedilir

### Senaryo 3: Gerçek Zamanlı İzleme

```bash
python run_detection.py
# Seçim: 3
# Seçim: 1 (Webcam)
```

Sonuç:
- Webcam görüntüsü gerçek zamanlı işlenir
- FPS bilgisi gösterilir
- 'q' tuşu ile çıkış

### Senaryo 4: Toplu Analiz

```bash
python run_detection.py
# Seçim: 4
# Klasör yolu: test_images/
```

Sonuç:
- Klasördeki tüm görüntüler işlenir
- Her görüntü için ayrı sonuç dosyası
- Toplam istatistikler gösterilir

---

## 🔧 Parametreler ve Ayarlar

### Confidence Threshold (conf_threshold)

Tespit güven eşiği. Düşük değer = daha fazla tespit (daha fazla yanlış alarm)

```python
# Düşük (daha hassas, daha fazla tespit)
system = UAVDetectionSystem(conf_threshold=0.15)

# Orta (dengeli) - ÖNERİLEN
system = UAVDetectionSystem(conf_threshold=0.25)

# Yüksek (daha seçici, daha az yanlış alarm)
system = UAVDetectionSystem(conf_threshold=0.5)
```

**Öneriler:**
- Genel kullanım: 0.25
- Kritik uygulamalar (hedefi kaçırmamak önemli): 0.15-0.20
- Az yanlış alarm istiyorsanız: 0.4-0.5

### IOU Threshold (iou_threshold)

NMS (Non-Maximum Suppression) için IoU eşiği.

```python
# Daha az overlap toleransı
system = UAVDetectionSystem(iou_threshold=0.3)

# Orta - ÖNERİLEN
system = UAVDetectionSystem(iou_threshold=0.5)

# Daha fazla overlap toleransı
system = UAVDetectionSystem(iou_threshold=0.7)
```

### Device (device)

İşlemci seçimi.

```python
# Otomatik (GPU varsa GPU, yoksa CPU)
system = UAVDetectionSystem(device='auto')

# GPU zorla
system = UAVDetectionSystem(device='0')

# CPU zorla
system = UAVDetectionSystem(device='cpu')
```

---

## 📊 Çıktı Formatları

### JSON Çıktısı

```json
{
  "detections": [
    {
      "class": "car",
      "class_id": 4,
      "confidence": 0.85,
      "bbox": [100, 200, 300, 400],
      "center": [200, 300],
      "width": 200,
      "height": 200
    }
  ],
  "count": 1,
  "processing_time": 0.05,
  "image_size": [1920, 1080],
  "model": "best.pt",
  "confidence_threshold": 0.25
}
```

### Görüntü Çıktısı

- Orijinal görüntü üzerine bounding box'lar çizilir
- Her box'ta: sınıf ismi + güven skoru
- Farklı sınıflar farklı renklerle gösterilir

### Video Çıktısı

- Her frame işlenmiş halde
- Tracking ID'leri gösterilir
- FPS bilgisi (opsiyonel)

---

## 🎨 Tespit Edilen Sınıflar

| ID | Sınıf | Açıklama |
|----|-------|----------|
| 0 | ignored | Göz ardı edilen |
| 1 | pedestrian | Yaya |
| 2 | people | İnsan grubu |
| 3 | bicycle | Bisiklet |
| 4 | car | Araba |
| 5 | van | Minibüs |
| 6 | truck | Kamyon |
| 7 | tricycle | Üç tekerlekli |
| 8 | awning-tricycle | Tenteli üç tekerlekli |
| 9 | bus | Otobüs |
| 10 | motor | Motosiklet |

---

## ⚡ Performans İpuçları

### GPU Kullanımı

```python
# GPU kullan (çok daha hızlı)
system = UAVDetectionSystem(device='0')
```

**Beklenen hızlar:**
- GPU (RTX 3050 Ti): ~20-30 FPS
- CPU: ~2-5 FPS

### Batch Processing

Birden fazla görüntü için:

```python
system = UAVDetectionSystem()

for image_path in image_list:
    result = system.detect_image(image_path, save_result=False)
    # save_result=False daha hızlı
```

### Video İşleme

```python
# Progress gösterme kapalı = daha hızlı
result = system.track_video('video.mp4', show_progress=False)
```

---

## 🐛 Sorun Giderme

### Problem: GPU kullanılmıyor

```python
import torch
print(torch.cuda.is_available())  # True olmalı
```

Çözüm: PyTorch CUDA versiyonunu yükleyin
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### Problem: Çok az tespit

Çözüm: Confidence threshold'u düşürün
```python
system = UAVDetectionSystem(conf_threshold=0.15)
```

### Problem: Çok fazla yanlış alarm

Çözüm: Confidence threshold'u yükseltin
```python
system = UAVDetectionSystem(conf_threshold=0.4)
```

### Problem: Video işleme yavaş

Çözümler:
1. GPU kullanın (`device='0'`)
2. Progress göstermeyi kapatın (`show_progress=False`)
3. Daha düşük çözünürlükte işleyin

---

## 📚 Örnek Kodlar

Daha fazla örnek için:
```bash
python examples/usage_examples.py
```

12 farklı kullanım senaryosu:
1. Basit tespit
2. Detaylı bilgiler
3. Hedef bulma
4. Video tracking
5. Özel threshold
6. Webcam
7. RTSP stream
8. Toplu işlem
9. JSON kullanımı
10. Koordinat takibi
11. Performans optimizasyonu
12. Hata yönetimi

---

## 🚀 Production Deployment

### Docker ile Çalıştırma

```bash
# Docker image oluştur
docker build -t baykar-uav-detection .

# Çalıştır
docker run -it --gpus all baykar-uav-detection
```

### API Servisi

```python
# Flask/FastAPI ile REST API oluştur
from flask import Flask, request, jsonify
from src.api.detection_api import UAVDetectionSystem

app = Flask(__name__)
system = UAVDetectionSystem()

@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    result = system.detect_image(file)
    return jsonify(result)

app.run(host='0.0.0.0', port=5000)
```

---

## 📞 Destek

Sorularınız için:
- Kod örnekleri: `examples/usage_examples.py`
- Proje durumu: `PROJECT_STATUS.md`
- API dokümantasyonu: `src/api/detection_api.py`

---

**🎯 Başarılar! Model hazır ve kullanıma hazır.**
