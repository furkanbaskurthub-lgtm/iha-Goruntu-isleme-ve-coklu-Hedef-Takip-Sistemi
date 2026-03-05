# 📤 GitHub'a Yükleme Rehberi

## ✅ Hazırlık Tamamlandı

Aşağıdaki dosyalar GitHub için hazırlandı:

### 📄 Temel Dosyalar
- ✅ README.md - Profesyonel proje açıklaması
- ✅ LICENSE - MIT lisansı
- ✅ .gitignore - Gereksiz dosyaları hariç tut
- ✅ CONTRIBUTING.md - Katkı rehberi

### 🐳 Docker Dosyaları
- ✅ Dockerfile - Temel image
- ✅ Dockerfile.prod - Production image
- ✅ docker-compose.yml - Servis orkestrasyon
- ✅ .dockerignore - Docker için ignore
- ✅ docker-start.sh - Linux/Mac script
- ✅ docker-start.ps1 - Windows script

### 📹 Demo
- ✅ outputs/demo/demo_video.mp4 - Örnek video (213 MB)

### 🤖 GitHub Actions
- ✅ .github/workflows/docker-build.yml - CI/CD
- ✅ .github/ISSUE_TEMPLATE/bug_report.md
- ✅ .github/ISSUE_TEMPLATE/feature_request.md

---

## 🚀 GitHub'a Yükleme Adımları

### 1. Git Repository Başlat

```bash
# Git başlat
git init

# Dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: İHA Görüntü İşleme ve Hedef Takip Sistemi"
```

### 2. GitHub Repository Oluştur

1. GitHub'da oturum aç
2. Sağ üstteki "+" → "New repository"
3. Repository adı: `iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi`
4. Description: "İHA için gerçek zamanlı nesne tespiti ve takip sistemi"
5. Public seç
6. "Create repository"

### 3. Remote Ekle ve Push Et

```bash
# Remote ekle
git remote add origin https://github.com/furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi.git

# Branch adını main yap
git branch -M main

# Push et
git push -u origin main
```

---

## ⚠️ Önemli Notlar

### Yüklenmeyen Dosyalar (.gitignore)

Aşağıdaki dosyalar/klasörler yüklenmeyecek:
- ❌ `data/raw/VisDrone2019-*` - Veri setleri (çok büyük)
- ❌ `runs/` - Eğitim sonuçları
- ❌ `*.pt` - Model dosyaları (büyük)
- ❌ `outputs/missions/` - Mission çıktıları
- ❌ `__pycache__/` - Python cache
- ❌ `venv/` - Sanal ortam

### Yüklenen Dosyalar

- ✅ Kaynak kodlar (`src/`)
- ✅ Konfigürasyon dosyaları (`configs/`)
- ✅ Docker dosyaları
- ✅ Dokümantasyon
- ✅ Demo video (`outputs/demo/demo_video.mp4`)
- ✅ Scripts
- ✅ Requirements

---

## 📊 Repository Boyutu

Tahmini boyut: ~220-250 MB
- Demo video: ~213 MB
- Kaynak kod: ~5 MB
- Dokümantasyon: ~2 MB

---

## 🎨 Repository Ayarları

### About Bölümü

GitHub repository sayfasında "About" → ⚙️:

**Description:**
```
İHA için gerçek zamanlı nesne tespiti ve takip sistemi. YOLOv8, ByteTrack ve profesyonel HUD ile donatılmış yapay zeka tabanlı görüntü işleme.
```

**Website:**
```
https://github.com/furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi
```

**Topics (etiketler):**
```
yolov8
object-detection
object-tracking
bytetrack
uav
drone
computer-vision
deep-learning
pytorch
opencv
real-time
gpu
cuda
docker
python
```

### Repository Settings

1. **Features**
   - ✅ Issues
   - ✅ Projects
   - ✅ Discussions (opsiyonel)
   - ✅ Wiki (opsiyonel)

2. **Social Preview**
   - Demo video'dan bir frame ekle

---

## 📝 İlk Release

### Release Oluşturma

1. GitHub'da "Releases" → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - İlk Sürüm`
4. Description:

```markdown
## 🎉 İlk Sürüm

### ✨ Özellikler
- YOLOv8 ile nesne tespiti
- ByteTrack ile çoklu hedef takibi
- Profesyonel İHA HUD overlay
- GPS ve telemetri özellikleri
- Docker desteği
- Video ve görüntü işleme

### 📦 Kurulum
```bash
pip install -r requirements.txt
```

### 🚀 Kullanım
```bash
python run_detection.py
```

### 📹 Demo
Demo video repository'de mevcuttur: `outputs/demo/demo_video.mp4`
```

---

## 🔄 Sonraki Adımlar

### 1. Model Dosyası Ekleme

Model dosyası çok büyük olduğu için Git LFS kullanın:

```bash
# Git LFS kur
git lfs install

# Model dosyasını track et
git lfs track "models/*.pt"

# .gitattributes'u commit et
git add .gitattributes
git commit -m "Add Git LFS tracking for model files"

# Model dosyasını ekle
git add models/best.pt
git commit -m "Add trained model"
git push
```

### 2. README'yi Güncelle

Demo video linkini güncelle:
```markdown
https://github.com/furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi/raw/main/outputs/demo/demo_video.mp4
```

### 3. Badges Ekle

README'ye eklenebilecek badge'ler:
- Build status
- License
- Python version
- Stars
- Forks
- Issues

---

## 🎯 Tanıtım

### README'de Vurgulanacaklar

1. ✅ Demo video (ilk göze çarpan)
2. ✅ Özellikler (bullet points)
3. ✅ Hızlı başlangıç (3-5 adım)
4. ✅ Ekran görüntüleri
5. ✅ Performans metrikleri
6. ✅ Docker desteği

### Sosyal Medya

Paylaşım için:
- Demo video
- Özellikler listesi
- GitHub linki
- #YOLOv8 #ObjectDetection #UAV #AI

---

## ✅ Kontrol Listesi

Push etmeden önce kontrol et:

- [ ] README.md doğru mu?
- [ ] LICENSE var mı?
- [ ] .gitignore doğru mu?
- [ ] Demo video ekli mi?
- [ ] requirements.txt güncel mi?
- [ ] Docker dosyaları çalışıyor mu?
- [ ] Dokümantasyon tam mı?
- [ ] Hassas bilgi yok mu? (API key, şifre vb.)

---

## 🚀 Push Komutu

Her şey hazırsa:

```bash
git push -u origin main
```

Başarılı! 🎉

Repository linki:
https://github.com/furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi
