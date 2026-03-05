# 🚀 Hızlı Başlangıç Rehberi

## 📸 Hangi Dosya Türünü Kullanmalıyım?

### Senaryo 1: Tek Fotoğraf Analizi
**Dosya türü:** `.jpg`, `.png`, `.jpeg` (tek fotoğraf)

**Ne yapar:**
- Fotoğraftaki nesneleri tespit eder
- GPS koordinatları hesaplar
- Mesafe bilgisi verir
- Gerçek boyut tahmini yapar

**Örnek kullanım:**
```bash
python test_real_scenario.py
# Seçim: 1
# Fotoğraf yolu: C:\Users\Admin\Desktop\drone_photo.jpg
```

---

### Senaryo 2: Video Görev Analizi
**Dosya türü:** `.mp4`, `.avi`, `.mov` (video dosyası)

**Ne yapar:**
- Video'nun frame'lerini işler
- Her frame'de tespit yapar
- Görev raporu oluşturur
- İstatistikler verir

**Örnek kullanım:**
```bash
python test_real_scenario.py
# Seçim: 2
# Video yolu: C:\Users\Admin\Desktop\drone_flight.mp4
```

---

### Senaryo 3: Toplu Fotoğraf Analizi
**Dosya türü:** Klasör (içinde `.jpg`, `.png` dosyaları)

**Ne yapar:**
- Klasördeki tüm fotoğrafları işler
- Her fotoğraf için ayrı sonuç
- Toplu görev raporu
- Genel istatistikler

**Örnek kullanım:**
```bash
python test_real_scenario.py
# Seçim: 3
# Klasör yolu: C:\Users\Admin\Desktop\drone_photos\
```

---

### Senaryo 4: Hedef Takip Simülasyonu
**Dosya türü:** `.jpg`, `.png`, `.jpeg` (tek fotoğraf)

**Ne yapar:**
- Fotoğraftaki hedefleri tespit eder
- Hedefleri kilitler
- Öncelik belirler (critical/high/normal/low)
- Takip raporu oluşturur

**Örnek kullanım:**
```bash
python test_real_scenario.py
# Seçim: 4
# Fotoğraf yolu: C:\Users\Admin\Desktop\target_area.jpg
```

---

## 🎯 Hangi Senaryoyu Seçmeliyim?

### Tek bir fotoğrafım var
→ **Senaryo 1** veya **Senaryo 4**

### Video dosyam var
→ **Senaryo 2**

### Birden fazla fotoğrafım var
→ **Senaryo 3**

### Hedefleri kilitlemek istiyorum
→ **Senaryo 4**

---

## 📁 Dosya Yolu Nasıl Girilir?

### Windows:
```
C:\Users\Admin\Desktop\image.jpg
C:\Users\Admin\Desktop\videos\flight.mp4
C:\Users\Admin\Desktop\photos\
```

### Kopyala-Yapıştır:
1. Dosyaya sağ tıkla
2. "Yolu kopyala" veya "Copy as path"
3. Programa yapıştır

### Sürükle-Bırak:
1. Dosyayı komut satırına sürükle
2. Yol otomatik yazılır

---

## ✅ Test İçin Hazır Fotoğraflar

Eğer kendi fotoğrafın yoksa, Enter'a bas:

```bash
# Senaryo 1, 3, 4 için
# Enter'a basınca otomatik test fotoğrafı kullanılır
Fotoğraf yolu (Enter=test fotoğrafı): [ENTER]
```

Test fotoğrafları:
```
data/raw/VisDrone2019-DET-test-dev/VisDrone2019-DET-test-dev/images/
```

---

## 🎬 Örnek Kullanım

### Örnek 1: Kendi Fotoğrafınla
```bash
python test_real_scenario.py

# Menü:
Seçim (1-5): 1

# Fotoğraf:
Fotoğraf yolu: C:\Users\Admin\Desktop\my_photo.jpg

# İHA parametreleri:
Yükseklik (metre) [100]: 150
GPS koordinatları girilsin mi? (e/h) [h]: e
  Latitude: 39.9334
  Longitude: 32.8597

# Sonuç:
✅ 25 hedef tespit edildi
📏 Zemin kapsama: 173.2m x 129.9m
💾 Sonuçlar kaydedildi: outputs/missions/...
```

### Örnek 2: Test Fotoğrafıyla
```bash
python test_real_scenario.py

# Menü:
Seçim (1-5): 4

# Fotoğraf (Enter=test):
Fotoğraf yolu: [ENTER]
✅ Test fotoğrafı kullanılıyor: 0000006_00159_d_0000001.jpg

# Hedef türü:
Seçim (1-3) [1]: 1

# Sonuç:
🎯 HEDEF KİLİTLENDİ
   ID: TGT_001
   Sınıf: car
   Mesafe: 85.3m
   GPS: 39.933456, 32.859712
   Öncelik: HIGH
```

---

## 🔧 Sorun Giderme

### "Dosya bulunamadı" hatası
- Dosya yolunu kontrol et
- Tırnak işaretleri olmadan yaz
- Dosya uzantısını kontrol et (.jpg, .mp4)

### "Test fotoğrafı bulunamadı"
- Veri setini indirmiş olman gerekiyor
- Veya kendi fotoğrafını kullan

### Video çok yavaş işleniyor
- "Kaç frame'de bir işlensin?" sorusuna büyük sayı gir (örn: 60)
- GPU kullanıldığından emin ol

---

## 💡 İpuçları

1. **İlk test için:** Senaryo 1 + Enter (test fotoğrafı)
2. **Hızlı sonuç için:** GPS koordinatlarını atlayabilirsin (h)
3. **Detaylı analiz için:** GPS koordinatlarını gir (e)
4. **Video için:** Her 30 frame'de bir işle (hızlı)
5. **Toplu işlem için:** Küçük klasörle başla (5-10 fotoğraf)

---

## 📊 Sonuçlar Nerede?

### Fotoğraf sonuçları:
```
outputs/missions/[GÖREV_ID]/
├── [fotoğraf_adı].jpg      # İşlenmiş fotoğraf
└── [fotoğraf_adı].json     # Detaylı bilgiler
```

### Görev raporu:
```
outputs/missions/[GÖREV_ID]/mission_report.json
```

### JSON içeriği:
- GPS koordinatları
- Mesafe bilgileri
- Tespit detayları
- İstatistikler

---

## 🚀 Hemen Başla!

```bash
# En kolay yol:
python test_real_scenario.py

# Seçim: 1 (Tek fotoğraf)
# Enter'a bas (test fotoğrafı)
# Enter'a bas (varsayılan yükseklik)
# h + Enter (GPS yok)

# 5 saniyede sonuç! ✅
```

---

**Başarılar! 🎯**
