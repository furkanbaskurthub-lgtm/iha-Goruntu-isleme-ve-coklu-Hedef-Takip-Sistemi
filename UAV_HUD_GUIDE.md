# 🎯 İHA HUD (Heads-Up Display) Rehberi

## ✨ Yeni Özellik: Gerçek İHA Görünümü!

Artık video çıktılarında profesyonel İHA HUD'ı var!

## 🎨 HUD Özellikleri

### 1. Merkez Nişangah
- Yeşil çapraz nişan
- Merkez daire
- Hedef kilitleme için

### 2. Telemetri Paneli (Sol Üst)
```
ALT: 150.5m      # Yükseklik
SPD: 12.3m/s     # Hız
HDG: 45°         # Yön
BAT: 85%         # Batarya
SIG: 95%         # Sinyal
GPS: 39.93340,32.85970
```

### 3. Hedef Bilgi Paneli (Sağ Üst)
```
TARGETS: 12      # Tespit edilen hedef
TRACKED: 8       # Takip edilen hedef
FRAME: 150/1000  # Frame numarası
TIME: 14:35:22   # Zaman
```

### 4. Yükseklik Merdiveni (Sağ)
```
120m
110m
100m  ← Mevcut
90m
80m
```

### 5. Hız Merdiveni (Sol)
```
20m/s
15m/s
10m/s  ← Mevcut
5m/s
0m/s
```

### 6. Pusula (Üst Orta)
```
W  NW  N  NE  E
      ▼
     45°
```

### 7. Yapay Ufuk Çizgisi
- Yatay referans çizgisi
- Pitch açısına göre hareket eder

### 8. Görev Durumu (Alt Sol)
```
MISSION: BAYKAR_001
STATUS: ACTIVE
```

### 9. Kayıt Göstergesi (Sağ Alt)
```
● REC  (yanıp söner)
```

### 10. Köşe Parantezleri
- Dört köşede L şeklinde işaretler
- Görüntü çerçevesi

---

## 🚀 Kullanım

### Video İşleme ile Otomatik:
```bash
python test_real_scenario.py
# Seçim: 2
# Video: video.mp4
```

HUD otomatik olarak eklenir!

### Manuel Kullanım (Kendi Kodunda):
```python
from src.utils.uav_hud import UAV_HUD
import cv2

# Video aç
cap = cv2.VideoCapture('video.mp4')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# HUD oluştur
hud = UAV_HUD(width, height)

# Her frame için
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # HUD ekle
    frame = hud.draw_full_hud(
        frame,
        altitude=100.0,
        speed=12.5,
        heading=45.0,
        gps=(39.9334, 32.8597),
        battery=85,
        signal=95,
        target_count=10,
        tracked_count=8,
        frame_num=150,
        total_frames=1000,
        mission_id="BAYKAR_001"
    )
    
    # Göster veya kaydet
    cv2.imshow('UAV View', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

---

## 🎯 HUD Elementleri Detay

### Renkler:
- **Yeşil (0, 255, 0)**: Ana HUD elementleri
- **Turuncu (0, 200, 255)**: Hedef bilgileri
- **Kırmızı (0, 0, 255)**: Uyarılar, kayıt
- **Beyaz (255, 255, 255)**: Metin
- **Siyah (0, 0, 0)**: Arka plan (yarı saydam)

### Uyarı Sistemi:
- **Batarya < 30%**: Turuncu
- **Batarya < 15%**: Kırmızı
- **Sinyal < 50%**: Uyarı rengi

### Simüle Edilen Veriler:
Video işlemede bazı veriler simüle edilir:
- **Hız**: 5-10 m/s arası değişir
- **Yön**: Yavaşça döner (0-360°)
- **Batarya**: Zamanla azalır
- **Sinyal**: Sabit 95%

---

## 📊 Örnek Görünüm

```
┌─────────────────────────────────────────────────────┐
│ ALT: 150.5m              N                          │
│ SPD: 12.3m/s            ▼45°                        │
│ HDG: 45°                                  TARGETS: 12│
│ BAT: 85%                                  TRACKED: 8 │
│ SIG: 95%                                  FRAME: 150 │
│ GPS: 39.93,32.86                          TIME: 14:35│
│                                                       │
│                                                       │
│                    ─────                              │
│                    │   │                              │
│              ─────  ⊕  ─────                         │
│                    │   │                              │
│                    ─────                              │
│                                                       │
│                                                       │
│ MISSION: BAYKAR_001                          ● REC   │
│ STATUS: ACTIVE                                        │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Özelleştirme

### Renkleri Değiştir:
```python
hud = UAV_HUD(width, height)
hud.color_primary = (255, 0, 0)  # Mavi
hud.color_secondary = (0, 255, 255)  # Sarı
```

### Sadece Belirli Elementleri Çiz:
```python
# Sadece nişangah
frame = hud.draw_crosshair(frame)

# Sadece telemetri
frame = hud.draw_telemetry_panel(frame, altitude=100, speed=10)

# Sadece pusula
frame = hud.draw_compass(frame, heading=45)
```

### Kendi HUD'ını Oluştur:
```python
# Özel kombinasyon
frame = hud.draw_corner_brackets(frame)
frame = hud.draw_crosshair(frame)
frame = hud.draw_telemetry_panel(frame, ...)
frame = hud.draw_compass(frame, ...)
```

---

## 💡 İpuçları

1. **Performans**: HUD çizimi minimal CPU kullanır
2. **Çözünürlük**: Her çözünürlükte çalışır (otomatik ölçeklenir)
3. **Gerçek Veri**: GPS ve yükseklik gerçek, diğerleri simüle
4. **Kayıt**: REC göstergesi her zaman aktif
5. **Batarya**: Video uzunluğuna göre azalır

---

## 🎬 Sonuç

Artık video çıktıların profesyonel İHA görünümünde!

**Öncesi:**
- Sadece bounding box'lar
- Basit label'lar

**Sonrası:**
- ✅ Tam İHA HUD
- ✅ Telemetri bilgileri
- ✅ Pusula ve yükseklik
- ✅ Profesyonel görünüm
- ✅ Gerçek İHA hissi

---

**🚁 Baykar için hazır!**
