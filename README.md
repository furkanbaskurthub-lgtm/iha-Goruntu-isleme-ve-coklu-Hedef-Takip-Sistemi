# 🚁 İHA Görüntü İşleme ve Hedef Takip Sistemi

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red.svg)](https://pytorch.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF.svg)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

İnsansız Hava Araçları (İHA) için gerçek zamanlı nesne tespiti ve takip sistemi. YOLOv8 ve ByteTrack algoritmaları kullanılarak geliştirilmiş, profesyonel HUD (Heads-Up Display) arayüzü ile donatılmış yapay zeka tabanlı görüntü işleme sistemi.

## 📹 Demo Video

https://github.com/furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi/raw/main/outputs/demo/demo_video.mp4

*İHA görüntüsü üzerinde gerçek zamanlı nesne tespiti, takip ve telemetri bilgileri*

---

## ✨ Özellikler

### 🎯 Nesne Tespiti
- **YOLOv8** modeli ile yüksek doğrulukta tespit
- **10 farklı sınıf**: Yaya, araç, kamyon, otobüs, bisiklet, motor, van, tricycle vb.
- **GPU hızlandırma** desteği (CUDA)
- Gerçek zamanlı işleme kapasitesi

### 🔄 Çoklu Hedef Takibi
- **ByteTrack** algoritması ile güçlü takip
- Benzersiz ID ataması
- Oklüzyon (engelleme) durumlarında dayanıklılık
- Frame-to-frame tutarlılık

### 🎮 Profesyonel İHA HUD
- **Crosshair** (nişangah) sistemi
- **Telemetri paneli**: Yükseklik, hız, yön, GPS, batarya, sinyal
- **Altitude/Speed ladder**: Dikey/yatay göstergeler
- **Compass**: Pusula göstergesi
- **Artificial horizon**: Yapay ufuk çizgisi
- **Mission status**: Görev durumu
- **Recording indicator**: Kayıt göstergesi

### 📍 GPS ve Konum Özellikleri
- Piksel koordinatlarından GPS koordinatlarına dönüşüm
- İHA ile hedef arası mesafe hesaplama (metre)
- Yer kapsama alanı hesaplama
- Gerçek dünya boyut tahmini
- Hedef kilitleme ve önceliklendirme

### 🐳 Docker Desteği
- GPU destekli containerization
- Kolay deployment
- İzole çalışma ortamı
- Production-ready yapılandırma

---

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.8+
- CUDA 11.8+ (GPU kullanımı için)
- 4GB+ GPU belleği (önerilen)
- 8GB+ RAM

### Kurulum

```bash
# Repository'yi klonla
git clone https://github.com/furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi.git
cd iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi

# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# PyTorch CUDA versiyonu (GPU için)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Model İndirme

Eğitilmiş model dosyasını indirin ve `models/` klasörüne yerleştirin:

```bash
# Model dosyası (best.pt) gereklidir
# Eğitim yapmadıysanız, önceden eğitilmiş modeli kullanabilirsiniz
```

---

## 💻 Kullanım

### 1. İnteraktif Menü

```bash
python run_detection.py
```

Menü seçenekleri:
1. Tek görüntü işleme
2. Video işleme (HUD ile)
3. Gerçek zamanlı kamera
4. Batch işleme
5. Hedef takip simülasyonu

### 2. Video İşleme (HUD ile)

```bash
python test_real_scenario.py
```

Senaryo 2'yi seçerek video işleme:
- Her frame işlenir
- ByteTrack takip aktif
- Profesyonel İHA HUD overlay
- GPS ve telemetri bilgileri
- Çıktı: `outputs/missions/[ID]/tracked_video.mp4`

### 3. Tek Görüntü İşleme

```python
from src.api.uav_mission_system import UAVMissionSystem

# Sistem başlat
system = UAVMissionSystem('models/best.pt')

# Görüntü işle
result = system.detect_image(
    'data/test_image.jpg',
    uav_altitude=100,
    uav_gps=(41.0082, 28.9784)
)

print(f"Tespit edilen: {result['detection_count']} nesne")
```

### 4. Video İşleme (Programatik)

```python
from src.api.uav_mission_system import UAVMissionSystem

system = UAVMissionSystem('models/best.pt')

result = system.process_video(
    'data/video.mp4',
    uav_altitude=150,
    uav_gps=(41.0082, 28.9784),
    save_video=True
)
```

---

## 🐳 Docker Kullanımı

### Hızlı Başlangıç

```bash
# Windows
.\docker-start.ps1 build
.\docker-start.ps1 start

# Linux/Mac
chmod +x docker-start.sh
./docker-start.sh build
./docker-start.sh start
```

### Docker Compose

```bash
# Servisi başlat
docker-compose up -d

# Logları izle
docker-compose logs -f

# Durdur
docker-compose down
```

### Container İçinde Çalıştırma

```bash
# Video işle
docker exec -it iha-detection-system python3 test_real_scenario.py

# Menüyü aç
docker exec -it iha-detection-system python3 run_detection.py

# Shell'e gir
docker exec -it iha-detection-system bash
```

Detaylı bilgi: [DOCKER_GUIDE.md](DOCKER_GUIDE.md)

---

## 📊 Model Eğitimi

### Veri Seti Hazırlama

```bash
# VisDrone veri setini indir ve data/raw/ klasörüne çıkar
# Ardından YOLO formatına dönüştür:
python src/data/prepare_visdrone.py
```

### Eğitim

```bash
python src/training/train_yolo.py
```

Eğitim parametreleri:
- Model: YOLOv8s
- Epochs: 150
- Batch size: 8 (4GB GPU için)
- Image size: 640x640
- Optimizer: SGD + Cosine LR
- Augmentation: Mosaic, flip, scale

### Performans

Eğitilmiş model metrikleri (VisDrone test seti):
- **Precision**: 51%
- **Recall**: 41%
- **mAP50**: 41.6%
- **mAP50-95**: 25.8%

---

## 📁 Proje Yapısı

```
iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi/
├── src/
│   ├── api/
│   │   ├── detection_api.py          # Temel detection API
│   │   └── uav_mission_system.py     # İHA mission sistemi
│   ├── core/
│   │   └── tracker.py                # ByteTrack implementasyonu
│   ├── data/
│   │   └── prepare_visdrone.py       # Veri seti hazırlama
│   ├── training/
│   │   └── train_yolo.py             # Model eğitimi
│   ├── evaluation/
│   │   └── evaluate_model.py         # Model değerlendirme
│   └── utils/
│       └── uav_hud.py                # İHA HUD sistemi
├── configs/
│   └── bytetrack.yaml                # ByteTrack konfigürasyonu
├── data/
│   ├── raw/                          # Ham veri seti
│   └── visdrone_config.yaml          # YOLO veri config
├── models/                           # Eğitilmiş modeller
├── outputs/                          # İşlenmiş çıktılar
│   └── demo/
│       └── demo_video.mp4            # Demo video
├── runs/                             # Eğitim sonuçları
├── scripts/
│   └── run_full_pipeline.py          # Tam pipeline
├── notebooks/                        # Jupyter notebook'lar
├── Dockerfile                        # Docker image
├── docker-compose.yml                # Docker compose
├── requirements.txt                  # Python bağımlılıkları
├── run_detection.py                  # Ana program
├── test_real_scenario.py             # Senaryo testleri
└── README.md                         # Bu dosya
```

---

## 🎨 HUD Özellikleri

### Görsel Elemanlar

1. **Crosshair (Nişangah)**
   - Merkez hedefleme sistemi
   - Dinamik çizgiler

2. **Telemetri Paneli**
   - Yükseklik (m)
   - Hız (m/s)
   - Yön (derece)
   - GPS koordinatları
   - Batarya seviyesi (%)
   - Sinyal gücü (%)

3. **Hedef Bilgileri**
   - Tespit edilen hedef sayısı
   - Takip edilen hedef sayısı
   - Frame numarası
   - Zaman damgası

4. **Altitude/Speed Ladder**
   - Dikey yükseklik göstergesi
   - Yatay hız göstergesi

5. **Compass (Pusula)**
   - 360° yön göstergesi
   - Kardinal noktalar (N, S, E, W)

6. **Mission Status**
   - Görev ID
   - Durum bilgisi

7. **Recording Indicator**
   - Kayıt göstergesi
   - Zaman sayacı

---

## 🔧 Yapılandırma

### ByteTrack Parametreleri

`configs/bytetrack.yaml`:
```yaml
track_thresh: 0.5      # Yüksek güven eşiği
track_buffer: 30       # Kayıp track buffer
match_thresh: 0.8      # Eşleştirme eşiği
frame_rate: 30         # Video frame rate
```

### Model Parametreleri

`src/training/train_yolo.py`:
```python
epochs = 150           # Eğitim epoch sayısı
batch = 8              # Batch size (GPU'ya göre ayarla)
imgsz = 640            # Görüntü boyutu
lr0 = 0.01             # Başlangıç learning rate
```

---

## 📈 Performans Optimizasyonu

### GPU Kullanımı

```python
# GPU bellek optimizasyonu
import torch
torch.cuda.empty_cache()

# Batch size ayarı
batch_size = 8  # 4GB GPU için
batch_size = 16  # 8GB GPU için
batch_size = 32  # 16GB+ GPU için
```

### Video İşleme Hızı

- **GPU (RTX 3050 Ti)**: ~25-30 FPS
- **CPU**: ~3-5 FPS

### Bellek Kullanımı

- Model: ~50MB
- Video işleme: ~2-4GB GPU
- Eğitim: ~3-4GB GPU

---

## 🛠️ Sorun Giderme

### GPU Algılanmıyor

```python
import torch
print(torch.cuda.is_available())  # True olmalı
print(torch.cuda.get_device_name(0))
```

Çözüm:
```bash
# CUDA versiyonunu kontrol et
nvidia-smi

# PyTorch CUDA versiyonunu yeniden yükle
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Bellek Hatası

```python
# Batch size'ı düşür
batch = 4  # veya 2

# Workers'ı kapat (Windows)
workers = 0
```

### Video İşleme Yavaş

```python
# Frame skip kullan
skip_frames = 2  # Her 2 frame'de bir işle

# Görüntü boyutunu küçült
imgsz = 416  # 640 yerine
```

---

## 📚 Dokümantasyon

- [Docker Kullanım Kılavuzu](DOCKER_GUIDE.md)
- [Docker Hızlı Başlangıç](DOCKER_QUICKSTART.md)
- [İHA HUD Kılavuzu](UAV_HUD_GUIDE.md)
- [Sınıf Mapping Düzeltmesi](CLASS_MAPPING_FIX.md)
- [Video İşleme Kılavuzu](VIDEO_PROCESSING_GUIDE.md)

---

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - Nesne tespiti
- [ByteTrack](https://github.com/ifzhang/ByteTrack) - Çoklu nesne takibi
- [VisDrone Dataset](http://aiskyeye.com/) - Veri seti
- [OpenCV](https://opencv.org/) - Görüntü işleme

---

## 📧 İletişim

Furkan Başkırbuh - [@furkanbaskurthub-lgtm](https://github.com/furkanbaskurthub-lgtm)

Proje Linki: [https://github.com/furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi](https://github.com/furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi)

---

## ⭐ Yıldız Geçmişi

[![Star History Chart](https://api.star-history.com/svg?repos=furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi&type=Date)](https://star-history.com/#furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi&Date)

---

<div align="center">
  <strong>🚁 İHA Görüntü İşleme ve Hedef Takip Sistemi</strong>
  <br>
  <sub>Yapay zeka destekli İHA görüntü analizi</sub>
</div>
