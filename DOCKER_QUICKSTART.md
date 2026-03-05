# 🚀 Docker Hızlı Başlangıç

## Windows Kullanıcıları İçin

### 1. Gereksinimler
- Docker Desktop yüklü olmalı
- WSL2 aktif olmalı
- NVIDIA GPU sürücüleri güncel olmalı

### 2. Kurulum (3 Adım)

```powershell
# Adım 1: Image oluştur
.\docker-start.ps1 build

# Adım 2: Container başlat
.\docker-start.ps1 start

# Adım 3: Test et
docker exec iha-detection-system python3 docker-test.py
```

### 3. Kullanım

```powershell
# Video işle
docker exec -it iha-detection-system python3 test_real_scenario.py

# Menüyü aç
docker exec -it iha-detection-system python3 run_detection.py

# Shell'e gir
.\docker-start.ps1 shell

# Logları izle
.\docker-start.ps1 logs

# Durumu kontrol et
.\docker-start.ps1 status
```

---

## Linux/Mac Kullanıcıları İçin

### 1. Gereksinimler
- Docker yüklü olmalı
- NVIDIA Docker runtime yüklü olmalı (GPU için)

### 2. Kurulum (3 Adım)

```bash
# Adım 1: Script'i çalıştırılabilir yap
chmod +x docker-start.sh

# Adım 2: Image oluştur
./docker-start.sh build

# Adım 3: Container başlat
./docker-start.sh start

# Test et
docker exec iha-detection-system python3 docker-test.py
```

### 3. Kullanım

```bash
# Video işle
docker exec -it iha-detection-system python3 test_real_scenario.py

# Menüyü aç
docker exec -it iha-detection-system python3 run_detection.py

# Shell'e gir
./docker-start.sh shell

# Logları izle
./docker-start.sh logs

# Durumu kontrol et
./docker-start.sh status
```

---

## Docker Compose ile (Alternatif)

```bash
# Başlat
docker-compose up -d

# Durdur
docker-compose down

# Logları izle
docker-compose logs -f

# Yeniden başlat
docker-compose restart
```

---

## Sık Kullanılan Komutlar

### Model Eğitimi
```bash
docker exec iha-detection-system python3 src/training/train_yolo.py
```

### Video İşleme
```bash
# Video dosyasını data/ klasörüne koy
cp video.mp4 data/

# İşle
docker exec iha-detection-system python3 process_video_full.py data/video.mp4
```

### Tek Görüntü İşleme
```bash
docker exec iha-detection-system python3 -c "
from src.api.uav_mission_system import UAVMissionSystem
system = UAVMissionSystem('models/best.pt')
result = system.detect_image('data/test.jpg')
print(result)
"
```

### GPU Kontrolü
```bash
docker exec iha-detection-system nvidia-smi
```

### Dosya Kopyalama
```bash
# Container'dan host'a
docker cp iha-detection-system:/app/outputs/result.mp4 ./

# Host'tan container'a
docker cp ./video.mp4 iha-detection-system:/app/data/
```

---

## Sorun Giderme

### GPU Algılanmıyor
```bash
# Test et
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

# Docker Desktop'ta WSL2 GPU desteğini aktifleştir
# Settings > Resources > WSL Integration
```

### Container Başlamıyor
```bash
# Logları kontrol et
docker logs iha-detection-system

# Eski container'ı temizle
docker stop iha-detection-system
docker rm iha-detection-system
```

### Bellek Hatası
```bash
# Batch size'ı düşür
docker exec iha-detection-system python3 src/training/train_yolo.py --batch 4
```

### Port Zaten Kullanımda
```bash
# Farklı port kullan
docker run -d --name iha-detection-system --gpus all -p 9000:8000 baykar-iha-detection:latest
```

---

## Performans İpuçları

1. **Volume kullan** - Büyük dosyaları volume ile paylaş
2. **GPU memory** - Batch size'ı GPU'ya göre ayarla
3. **Cache** - Model dosyalarını cache'le
4. **Multi-stage build** - Production için Dockerfile.prod kullan

---

## Temizlik

```bash
# Container'ı durdur ve sil
docker stop iha-detection-system
docker rm iha-detection-system

# Image'ı sil
docker rmi baykar-iha-detection:latest

# Tüm kullanılmayan kaynakları temizle
docker system prune -a
```

---

## Jupyter Notebook (Geliştirme)

```bash
# Notebook servisini başlat
docker-compose --profile dev up -d iha-notebook

# Tarayıcıda aç
# http://localhost:8888
```

---

## Production Deployment

```bash
# Production image oluştur
docker build -f Dockerfile.prod -t baykar-iha-detection:prod .

# Başlat
docker run -d \
  --name iha-production \
  --gpus all \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  -p 8000:8000 \
  --restart always \
  baykar-iha-detection:prod
```

---

## Yardım

Detaylı bilgi için: [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
