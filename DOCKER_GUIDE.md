# 🐳 Docker Kullanım Kılavuzu - BAYKAR İHA Projesi

## 📋 Gereksinimler

### 1. Docker Kurulumu
```bash
# Windows için Docker Desktop indir ve kur
# https://www.docker.com/products/docker-desktop/

# Linux için
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2. NVIDIA Docker Runtime (GPU için)
```bash
# Windows: Docker Desktop ayarlarından WSL2 ve GPU desteğini aktifleştir

# Linux için
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

### 3. GPU Testi
```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

---

## 🚀 Hızlı Başlangıç

### 1. Docker Image Oluştur
```bash
# Temel image
docker build -t baykar-iha-detection:latest .

# Veya docker-compose ile
docker-compose build
```

### 2. Container Çalıştır

#### A. Docker Compose ile (Önerilen)
```bash
# Servisi başlat
docker-compose up -d iha-detection

# Logları izle
docker-compose logs -f iha-detection

# Durdur
docker-compose down
```

#### B. Docker Run ile
```bash
docker run -d \
  --name iha-detection \
  --gpus all \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  -p 8000:8000 \
  baykar-iha-detection:latest
```

---

## 💻 Kullanım Senaryoları

### 1. İnteraktif Mod (Menü ile)
```bash
# Container'a gir
docker exec -it iha-detection bash

# Menüyü çalıştır
python3 run_detection.py
```

### 2. Video İşleme
```bash
# Video dosyasını data klasörüne koy
cp /path/to/video.mp4 ./data/

# Container içinde işle
docker exec -it iha-detection python3 test_real_scenario.py
```

### 3. Tek Görüntü İşleme
```bash
docker exec iha-detection python3 -c "
from src.api.uav_mission_system import UAVMissionSystem
system = UAVMissionSystem('models/best.pt')
result = system.detect_image('data/test_image.jpg')
print(result)
"
```

### 4. Model Eğitimi
```bash
# Eğitim verilerini hazırla
docker exec iha-detection python3 src/data/prepare_visdrone.py

# Eğitimi başlat
docker exec iha-detection python3 src/training/train_yolo.py
```

### 5. Jupyter Notebook (Geliştirme)
```bash
# Notebook servisini başlat
docker-compose --profile dev up -d iha-notebook

# Tarayıcıda aç: http://localhost:8888
```

---

## 📁 Volume Yapısı

```
Proje Dizini/
├── models/          → /app/models (Model dosyaları)
├── data/            → /app/data (Veri seti)
├── outputs/         → /app/outputs (Çıktılar)
├── runs/            → /app/runs (Eğitim sonuçları)
└── logs/            → /app/logs (Log dosyaları)
```

---

## 🔧 Yapılandırma

### GPU Bellek Ayarı
```yaml
# docker-compose.yml içinde
environment:
  - CUDA_VISIBLE_DEVICES=0  # İlk GPU
  - PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

### Port Değiştirme
```yaml
ports:
  - "9000:8000"  # Host:Container
```

---

## 🐛 Sorun Giderme

### GPU Algılanmıyor
```bash
# Container içinde test et
docker exec iha-detection python3 -c "import torch; print(torch.cuda.is_available())"

# NVIDIA runtime kontrolü
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Bellek Hatası
```bash
# Batch size'ı düşür
docker exec iha-detection python3 src/training/train_yolo.py --batch 4
```

### Permission Hatası
```bash
# Linux'ta volume izinleri
sudo chown -R $USER:$USER ./outputs ./runs ./logs
```

---

## 📊 Monitoring

### Container Durumu
```bash
# Tüm container'ları listele
docker ps -a

# Kaynak kullanımı
docker stats iha-detection

# Loglar
docker logs -f iha-detection
```

### GPU Kullanımı
```bash
# Container içinde
docker exec iha-detection nvidia-smi

# Sürekli izle
docker exec iha-detection watch -n 1 nvidia-smi
```

---

## 🔄 Güncelleme ve Bakım

### Image Güncelleme
```bash
# Yeni image oluştur
docker-compose build --no-cache

# Container'ı yeniden başlat
docker-compose up -d --force-recreate
```

### Temizlik
```bash
# Container'ı durdur ve sil
docker-compose down

# Image'ı sil
docker rmi baykar-iha-detection:latest

# Tüm kullanılmayan kaynakları temizle
docker system prune -a
```

---

## 🌐 Production Deployment

### Docker Hub'a Push
```bash
# Tag ekle
docker tag baykar-iha-detection:latest username/baykar-iha:v1.0

# Push et
docker push username/baykar-iha:v1.0
```

### Swarm/Kubernetes
```bash
# Docker Swarm
docker stack deploy -c docker-compose.yml iha-stack

# Kubernetes (helm chart gerekli)
kubectl apply -f k8s/deployment.yaml
```

---

## 📝 Örnek Komutlar

### Batch Video İşleme
```bash
# Tüm videoları işle
docker exec iha-detection bash -c "
for video in data/videos/*.mp4; do
  python3 process_video_full.py \$video
done
"
```

### Otomatik Yedekleme
```bash
# Outputs'u yedekle
docker exec iha-detection tar -czf /app/backup_$(date +%Y%m%d).tar.gz /app/outputs
docker cp iha-detection:/app/backup_*.tar.gz ./backups/
```

### Performans Testi
```bash
docker exec iha-detection python3 -c "
from src.api.uav_mission_system import UAVMissionSystem
import time

system = UAVMissionSystem('models/best.pt')
start = time.time()
result = system.detect_image('data/test.jpg')
print(f'İşlem süresi: {time.time()-start:.2f}s')
"
```

---

## ⚙️ Ortam Değişkenleri

```bash
# .env dosyası oluştur
cat > .env << EOF
CUDA_VISIBLE_DEVICES=0
MODEL_PATH=/app/models/best.pt
CONFIDENCE_THRESHOLD=0.25
IOU_THRESHOLD=0.45
MAX_DETECTIONS=300
OUTPUT_DIR=/app/outputs
LOG_LEVEL=INFO
EOF

# Docker compose ile kullan
docker-compose --env-file .env up -d
```

---

## 🎯 Best Practices

1. **Volume kullan** - Model ve veri dosyalarını container dışında tut
2. **GPU memory** - Batch size'ı GPU'ya göre ayarla
3. **Logging** - Logları volume'a yönlendir
4. **Health checks** - Container sağlığını izle
5. **Resource limits** - CPU/RAM limitlerini belirle
6. **Multi-stage build** - Production için optimize et
7. **Security** - Root kullanıcı yerine user oluştur

---

## 📞 Destek

Sorun yaşarsanız:
1. Logları kontrol edin: `docker logs iha-detection`
2. GPU durumunu kontrol edin: `nvidia-smi`
3. Container içine girin: `docker exec -it iha-detection bash`
