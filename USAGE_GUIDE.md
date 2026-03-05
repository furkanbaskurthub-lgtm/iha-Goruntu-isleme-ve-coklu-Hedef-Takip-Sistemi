# 📖 Kullanım Kılavuzu

## 🚀 Adım Adım Eğitim ve Test

### 1. Kurulum

```bash
# Sanal ortam oluştur
python -m venv venv

# Aktif et (Windows)
venv\Scripts\activate

# Aktif et (Linux/Mac)
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 2. Veri Setini Hazırla

VisDrone veri setini indirdikten sonra `data/raw/` klasörüne yerleştirin. Yapı şöyle olmalı:

```
data/raw/
├── VisDrone2019-DET-train/
├── VisDrone2019-DET-val/
└── VisDrone2019-DET-test-dev/
```

Veri setini YOLO formatına dönüştürün:

```bash
python src/data/prepare_visdrone.py
```

Bu işlem:
- Her veri seti için `labels/` klasörü oluşturur
- VisDrone annotation'larını YOLO formatına çevirir
- Ignored regions ve düşük skorlu nesneleri filtreler

### 3. Model Eğitimi

#### Hızlı Test (Küçük Model)
```bash
python src/training/train_yolo.py
```

Script içinde model seçimi:
```python
# Küçük model (hızlı test)
train_model(model_name='yolov8n.pt', epochs=50, batch=16)

# Orta model (önerilen)
train_model(model_name='yolov8s.pt', epochs=100, batch=16)

# Büyük model (en iyi doğruluk)
train_model(model_name='yolov8m.pt', epochs=150, batch=8)
```

#### Eğitim Parametreleri

| Parametre | Açıklama | Önerilen |
|-----------|----------|----------|
| model_name | Başlangıç modeli | yolov8s.pt |
| epochs | Epoch sayısı | 100-150 |
| imgsz | Görüntü boyutu | 640 |
| batch | Batch size | 16 (GPU'ya göre) |
| device | GPU/CPU | '0' (GPU) |

#### GPU Memory Sorunları

Eğer "CUDA out of memory" hatası alırsanız:

```python
# Batch size'ı azaltın
train_model(model_name='yolov8s.pt', epochs=100, batch=8)

# Veya daha küçük model kullanın
train_model(model_name='yolov8n.pt', epochs=100, batch=16)
```

### 4. Eğitim Sonuçlarını İnceleme

Eğitim tamamlandıktan sonra:

```
runs/train/visdrone_yolo/
├── weights/
│   ├── best.pt          # En iyi model (validation loss'a göre)
│   └── last.pt          # Son epoch
├── results.png          # Metrik grafikleri
├── confusion_matrix.png # Confusion matrix
├── F1_curve.png        # F1 score curve
├── PR_curve.png        # Precision-Recall curve
└── args.yaml           # Eğitim parametreleri
```

### 5. Model Değerlendirme

```bash
python src/evaluation/evaluate_model.py
```

Bu script:
- Validation seti üzerinde mAP, precision, recall hesaplar
- Test görüntüleri üzerinde tahmin yapar (ilk 10 görüntü)
- Model hızını (FPS) ölçer

**Beklenen Metrikler:**
- mAP50: 0.40-0.50
- mAP50-95: 0.25-0.35
- FPS: 30-60 (GPU'ya bağlı)

### 6. Tracking (Nesne Takibi)

#### Python Script ile

```python
from src.core.tracker import UAVTracker

# Tracker'ı başlat
tracker = UAVTracker(
    model_path='runs/train/visdrone_yolo/weights/best.pt',
    tracker_config='bytetrack.yaml'
)

# Video üzerinde tracking
tracker.process_video(
    video_path='data/test_video.mp4',
    output_path='runs/tracked_video.mp4',
    conf=0.3,           # Confidence threshold
    iou=0.45,           # IOU threshold
    show=True,          # Görüntüyü göster
    save_txt=True       # Sonuçları txt'ye kaydet
)

# Tek görüntü üzerinde tespit
tracker.process_image(
    image_path='data/test_image.jpg',
    output_path='runs/test_detection.jpg',
    conf=0.3
)

# İstatistikleri göster
tracker.get_statistics()
```

#### Hızlı Test

```bash
python scripts/quick_test.py
```

### 7. Tam Pipeline

Tüm adımları tek seferde çalıştır:

```bash
python scripts/run_full_pipeline.py
```

Opsiyonlar:
```bash
# Veri hazırlamayı atla (zaten hazırsa)
python scripts/run_full_pipeline.py --skip-prepare

# Eğitimi atla (model zaten eğitilmişse)
python scripts/run_full_pipeline.py --skip-train

# Farklı model ve parametreler
python scripts/run_full_pipeline.py --model yolov8m.pt --epochs 150 --batch 8
```

## 🎯 Tracking Çıktısı Formatı

### Video Çıktısı
- Her nesneye sabit ID atanır (örn: ID:10)
- Hareket yolu çizilir (son 30 frame)
- Bounding box ve label gösterilir

### TXT Çıktısı (save_txt=True)
```
frame_id,track_id,class_id,confidence,x1,y1,x2,y2
1,10,3,0.8745,450.23,320.45,580.67,420.89
1,15,0,0.9123,120.34,200.56,180.78,280.90
2,10,3,0.8823,455.12,325.34,585.45,425.67
...
```

Format:
- frame_id: Frame numarası
- track_id: Nesne takip ID'si
- class_id: Sınıf ID'si (0-9)
- confidence: Güven skoru
- x1,y1,x2,y2: Bounding box koordinatları

## 🔧 İleri Seviye Kullanım

### Eğitimi Devam Ettirme

Eğitim kesintiye uğradıysa:

```python
from src.training.train_yolo import resume_training

resume_training(
    checkpoint_path='runs/train/visdrone_yolo/weights/last.pt',
    epochs=150
)
```

### Hyperparameter Tuning

```python
from ultralytics import YOLO

model = YOLO('yolov8s.pt')

# Hyperparameter tuning
model.tune(
    data='data/visdrone_config.yaml',
    epochs=30,
    iterations=300,
    optimizer='AdamW',
    plots=True,
    save=True
)
```

### Model Export (ONNX, TensorRT)

```python
from ultralytics import YOLO

model = YOLO('runs/train/visdrone_yolo/weights/best.pt')

# ONNX export
model.export(format='onnx')

# TensorRT export (NVIDIA GPU için)
model.export(format='engine', device=0)
```

### Multi-GPU Training

```python
train_model(
    model_name='yolov8s.pt',
    epochs=100,
    batch=32,
    device='0,1'  # 2 GPU kullan
)
```

## 📊 Performans Optimizasyonu

### 1. Batch Size
- GPU memory'ye göre ayarlayın
- Daha büyük batch = daha stabil eğitim
- Önerilen: 16 (8GB GPU için)

### 2. Image Size
- Daha büyük = daha iyi doğruluk, daha yavaş
- Daha küçük = daha hızlı, daha düşük doğruluk
- Önerilen: 640 (İHA için yeterli)

### 3. Model Boyutu
- n (nano): En hızlı, en düşük doğruluk
- s (small): Hız/doğruluk dengesi (önerilen)
- m (medium): İyi doğruluk, orta hız
- l (large): Yüksek doğruluk, yavaş
- x (xlarge): En iyi doğruluk, en yavaş

### 4. Augmentation
İHA görüntüleri için özel ayarlar:
- Rotation: 0° (İHA sabit açıda)
- Perspective: 0 (kuş bakışı)
- Vertical flip: 0 (İHA için anlamsız)
- Horizontal flip: 0.5 (uygun)

## 🐛 Sık Karşılaşılan Sorunlar

### 1. CUDA out of memory
```python
# Çözüm: Batch size azalt
train_model(batch=8)  # veya 4
```

### 2. Labels klasörü bulunamadı
```bash
# Çözüm: Veri hazırlama scriptini çalıştır
python src/data/prepare_visdrone.py
```

### 3. Model bulunamadı
```python
# Çözüm: Model yolunu kontrol et
model_path = 'runs/train/visdrone_yolo/weights/best.pt'
print(Path(model_path).exists())
```

### 4. Düşük mAP
- Daha fazla epoch eğit (150-200)
- Daha büyük model kullan (yolov8m veya yolov8l)
- Hyperparameter tuning yap
- Veri augmentation ayarlarını optimize et

## 📚 Ek Kaynaklar

- [Ultralytics Docs](https://docs.ultralytics.com/)
- [VisDrone Dataset](https://github.com/VisDrone/VisDrone-Dataset)
- [ByteTrack Paper](https://arxiv.org/abs/2110.06864)
- [YOLO Training Tips](https://docs.ultralytics.com/guides/model-training-tips/)
