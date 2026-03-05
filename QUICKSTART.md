# ⚡ Hızlı Başlangıç

## 🚀 3 Adımda Başla

### 1️⃣ Veri Setini Hazırla
```bash
python src/data/prepare_visdrone.py
```
Bu komut VisDrone annotation'larını YOLO formatına dönüştürür.

### 2️⃣ Modeli Eğit
```bash
python src/training/train_yolo.py
```
YOLOv8s modelini 100 epoch eğitir (~2-4 saat GPU'da).

### 3️⃣ Test Et
```bash
python scripts/quick_test.py
```
Eğitilmiş modeli test görüntüsü üzerinde dener.

## 📊 Tracking Kullanımı

```python
from src.core.tracker import UAVTracker

# Tracker başlat
tracker = UAVTracker(
    model_path='runs/train/visdrone_yolo/weights/best.pt'
)

# Video işle
tracker.process_video(
    'data/test_video.mp4',
    output_path='runs/tracked_video.mp4',
    conf=0.3,
    save_txt=True
)
```

## 📁 Proje Yapısı

```
iha_target_kitlenme/
├── data/
│   ├── raw/                    # VisDrone veri seti
│   └── visdrone_config.yaml    # YOLO config
├── src/
│   ├── core/tracker.py         # Tracking
│   ├── data/prepare_visdrone.py # Veri hazırlama
│   ├── training/train_yolo.py  # Eğitim
│   └── evaluation/evaluate_model.py # Değerlendirme
├── scripts/
│   ├── run_full_pipeline.py    # Tam pipeline
│   └── quick_test.py           # Hızlı test
├── configs/
│   └── bytetrack.yaml          # Tracker config
├── notebooks/
│   └── demo_tracking.ipynb     # Demo notebook
├── README.md                   # Detaylı dokümantasyon
├── USAGE_GUIDE.md             # Kullanım kılavuzu
├── BAYKAR_INTERVIEW_NOTES.md  # Mülakat notları
└── requirements.txt           # Bağımlılıklar
```

## 🎯 Önemli Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `README.md` | Detaylı proje dokümantasyonu |
| `USAGE_GUIDE.md` | Adım adım kullanım kılavuzu |
| `BAYKAR_INTERVIEW_NOTES.md` | Teknik kararlar ve mülakat notları |
| `src/core/tracker.py` | Ana tracking implementasyonu |
| `src/training/train_yolo.py` | Model eğitim scripti |
| `notebooks/demo_tracking.ipynb` | İnteraktif demo |

## 💡 İpuçları

### GPU Memory Yetersizse
```python
# train_yolo.py içinde batch size'ı azalt
train_model(model_name='yolov8s.pt', epochs=100, batch=8)
```

### Hızlı Test İçin
```python
# Küçük model kullan
train_model(model_name='yolov8n.pt', epochs=50, batch=16)
```

### En İyi Doğruluk İçin
```python
# Büyük model ve daha fazla epoch
train_model(model_name='yolov8m.pt', epochs=150, batch=8)
```

## 📚 Daha Fazla Bilgi

- Detaylı kullanım: `USAGE_GUIDE.md`
- Teknik detaylar: `BAYKAR_INTERVIEW_NOTES.md`
- API dokümantasyonu: `README.md`
- İnteraktif demo: `notebooks/demo_tracking.ipynb`

## 🆘 Sorun mu Yaşıyorsunuz?

1. GPU kontrolü: `python -c "import torch; print(torch.cuda.is_available())"`
2. Veri seti kontrolü: `data/raw/` klasöründe VisDrone klasörleri var mı?
3. Labels oluşturuldu mu: `data/raw/VisDrone2019-DET-train/VisDrone2019-DET-train/labels/` var mı?

## ✅ Başarı Kriterleri

- ✅ mAP50 > 0.40
- ✅ FPS > 30
- ✅ Tracking ID'leri stabil
- ✅ Baykar formatında çıktı: "Hedef X nolu araç, koordinatları: [...]"
