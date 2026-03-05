# 🎥 Video İşleme Rehberi

## 📹 Video İşleme Seçenekleri

### Seçenek 1: Hızlı İşleme (Frame Atlama)
**Script:** `test_real_scenario.py` → Senaryo 2

**Özellikler:**
- ✅ Belirli frame'leri işler (örn: her 30 frame'de bir)
- ✅ Çok hızlı
- ✅ Görev raporu oluşturur
- ⚠️ Video çıktısı var ama tüm frame'ler işlenmez

**Kullanım:**
```bash
python test_real_scenario.py
# Seçim: 2
# Video yolu: video.mp4
# Kaç frame'de bir: 30
```

**Sonuç:**
- İşlenmiş video: `outputs/missions/[ID]/tracked_video.mp4`
- Görev raporu: `outputs/missions/[ID]/mission_report.json`

---

### Seçenek 2: Tam İşleme (Her Frame) ⭐ ÖNERİLEN
**Script:** `process_video_full.py`

**Özellikler:**
- ✅ Her frame işlenir
- ✅ ByteTrack ile tracking
- ✅ Gerçek zamanlı bilgiler (frame sayısı, hedef sayısı)
- ✅ Progress bar
- ✅ Pürüzsüz video çıktısı

**Kullanım:**
```bash
python process_video_full.py
# Video yolu: video.mp4
# Yükseklik: 100
# Confidence: 0.25
# GPS: h (hayır)
```

**Sonuç:**
- İşlenmiş video: `outputs/missions/[ID]/tracked_video.mp4`
- Her frame'de:
  - Bounding box'lar
  - Tracking ID'ler
  - Confidence skorları
  - Frame bilgisi
  - Progress bar

---

## 🎬 Video Çıktısında Neler Var?

### Görsel Öğeler:
1. **Bounding Box'lar**: Her tespit edilen nesne etrafında
2. **Label'lar**: Sınıf ismi + confidence skoru
3. **Tracking ID'ler**: Her hedef için unique ID
4. **Mesafe Bilgisi**: İHA'dan hedefe mesafe (metre)

### Bilgi Paneli (Sol Üst):
```
Frame: 150/1000
Hedef: 12
Takip: 8
Yukseklik: 100m
```

### Progress Bar (Alt):
```
[████████████░░░░░░░░] 65.3%
```

---

## ⚡ Performans Karşılaştırması

### Hızlı İşleme (Frame Atlama)
```
Video: 1000 frame, 30 FPS
İşleme: Her 30 frame'de bir
Süre: ~2 dakika
Çıktı: 1000 frame (33 işlenmiş)
```

### Tam İşleme (Her Frame)
```
Video: 1000 frame, 30 FPS
İşleme: Her frame
Süre: ~5-10 dakika (GPU'ya bağlı)
Çıktı: 1000 frame (hepsi işlenmiş)
```

---

## 🎯 Hangi Yöntemi Seçmeliyim?

### Hızlı İşleme Kullan:
- ✅ Hızlı sonuç istiyorsan
- ✅ Sadece istatistik gerekiyorsa
- ✅ Uzun video'lar için (>10 dakika)
- ✅ Görev raporu önemliyse

### Tam İşleme Kullan:
- ✅ Pürüzsüz video istiyorsan
- ✅ Her frame'i görmek istiyorsan
- ✅ Sunum/demo için
- ✅ Detaylı analiz için
- ✅ Tracking performansını görmek için

---

## 📊 Örnek Çıktılar

### Hızlı İşleme Sonucu:
```
✅ Görev tamamlandı!
📊 92 frame işlendi

Sınıf Dağılımı:
  • bus: 576
  • bicycle: 422
  • van: 147
  • car: 46

Mesafe İstatistikleri:
  • Min: 50.0m
  • Max: 59.5m
  • Ortalama: 53.4m

💾 Rapor: outputs/missions/20260305_045125/mission_report.json
📹 Video: outputs/missions/20260305_045125/tracked_video.mp4
```

### Tam İşleme Sonucu:
```
✅ VİDEO İŞLEME TAMAMLANDI!

📊 İstatistikler:
   Toplam frame: 2750
   Toplam tespit: 15234
   Takip edilen hedef: 156
   İşlem süresi: 245.3s
   İşlem hızı: 11.2 FPS

📋 Sınıf Dağılımı:
   • bicycle: 8542
   • car: 3421
   • bus: 1876
   • van: 1395

💾 Video kaydedildi: outputs/missions/[ID]/tracked_video.mp4
📁 Dosya boyutu: 125.3 MB
```

---

## 🔧 Ayarlar ve Optimizasyon

### Confidence Threshold
```python
# Daha fazla tespit (daha fazla yanlış alarm)
conf_threshold = 0.15

# Dengeli (önerilen)
conf_threshold = 0.25

# Daha az tespit (daha az yanlış alarm)
conf_threshold = 0.4
```

### İşlem Hızı
**GPU kullan:**
```bash
# GPU otomatik kullanılır
# RTX 3050 Ti: ~10-15 FPS
# CPU: ~2-3 FPS
```

**Frame atlama:**
```bash
# Hızlı işleme için
Kaç frame'de bir: 60  # Çok hızlı
Kaç frame'de bir: 30  # Hızlı (önerilen)
Kaç frame'de bir: 10  # Orta
Kaç frame'de bir: 1   # Yavaş ama detaylı
```

---

## 🎬 Video Formatları

### Desteklenen Formatlar:
- ✅ `.mp4` (önerilen)
- ✅ `.avi`
- ✅ `.mov`
- ✅ `.mkv`
- ✅ `.wmv`

### Çıktı Formatı:
- Format: MP4 (H.264)
- Codec: mp4v
- FPS: Orijinal video ile aynı
- Çözünürlük: Orijinal video ile aynı

---

## 💡 İpuçları

1. **İlk test için:** Kısa video kullan (10-30 saniye)
2. **Uzun video için:** Hızlı işleme kullan (frame atlama)
3. **Demo için:** Tam işleme kullan (her frame)
4. **GPU kullan:** Çok daha hızlı (10x)
5. **Confidence ayarla:** 0.25 dengeli bir değer

---

## 🐛 Sorun Giderme

### Video çok yavaş işleniyor
**Çözüm:**
1. GPU kullanıldığından emin ol
2. Frame atlama kullan (her 30 frame)
3. Confidence threshold'u yükselt (0.3-0.4)

### Video çıktısı oynatılmıyor
**Çözüm:**
1. VLC Media Player kullan
2. Codec yükle (K-Lite Codec Pack)
3. Farklı video player dene

### Çok fazla yanlış tespit
**Çözüm:**
1. Confidence threshold'u yükselt (0.3-0.4)
2. IOU threshold'u ayarla

---

## 🚀 Hızlı Başlangıç

### En Kolay Yol (Tam İşleme):
```bash
python process_video_full.py

# Video yolu: C:\Users\Admin\Desktop\video.mp4
# Yükseklik: [ENTER] (100m)
# Confidence: [ENTER] (0.25)
# GPS: h [ENTER]

# Bekle... (5-10 dakika)
# ✅ Video hazır!
```

### Hızlı Sonuç (Frame Atlama):
```bash
python test_real_scenario.py

# Seçim: 2
# Video: C:\Users\Admin\Desktop\video.mp4
# Yükseklik: [ENTER]
# GPS: h [ENTER]
# Frame atlama: 30 [ENTER]

# Bekle... (2-3 dakika)
# ✅ Rapor + Video hazır!
```

---

## 📁 Çıktı Dosyaları

```
outputs/missions/[GÖREV_ID]/
├── tracked_video.mp4          # İşlenmiş video
├── mission_report.json        # Görev raporu
└── [frame_images]/            # Frame görüntüleri (opsiyonel)
```

---

**🎬 Başarılar! Video işleme hazır!**
