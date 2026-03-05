# Recall İyileştirme Rehberi

## Mevcut Durum
- **Precision**: 0.52 (iyi)
- **Recall**: 0.40 (düşük ❌)
- **mAP50**: 0.41
- **Problem**: Model nesnelerin sadece %40'ını tespit ediyor

## Recall Neden Düşük?

1. **Küçük nesneler**: VisDrone'da çok küçük nesneler var
2. **Yoğun sahneler**: Çok fazla nesne bir arada
3. **Model kapasitesi**: YOLOv8s yeterli olmayabilir
4. **Augmentation**: Yetersiz veri çeşitliliği

## Çözüm Stratejileri

### Strateji 1: Mevcut Modeli İyileştir (ÖNERİLEN)
```bash
# Mevcut en iyi modelden devam et, daha agresif augmentation ile
python src/training/train_yolo_improved.py
```

**Değişiklikler:**
- ✅ Daha agresif augmentation (mixup, copy-paste)
- ✅ AdamW optimizer (daha iyi generalization)
- ✅ Düşük confidence threshold
- ✅ Class loss azaltıldı (recall için)
- ✅ Mevcut best.pt'den devam

### Strateji 2: Daha Büyük Model Kullan
```python
# YOLOv8m veya YOLOv8l dene (daha fazla parametre)
model_name='yolov8m.pt'  # 25M parametre
batch=4  # Batch size düşür
```

### Strateji 3: Görüntü Boyutunu Artır
```python
# Küçük nesneler için daha büyük görüntü
imgsz=1280  # 640 yerine
batch=4     # Batch size düşür
```

### Strateji 4: Veri Dengesizliği Kontrolü
```bash
# Hangi sınıflar düşük recall'a sahip?
python src/evaluation/evaluate_model.py
```

### Strateji 5: Ensemble Yöntemi
```python
# Birden fazla model kullan ve sonuçları birleştir
# - YOLOv8s (hızlı)
# - YOLOv8m (dengeli)
# - YOLOv10 (yeni)
```

## Hızlı Test

Mevcut eğitimi durdurup yeni stratejiyi dene:

```bash
# 1. Mevcut eğitimi durdur (Ctrl+C veya process'i durdur)

# 2. İyileştirilmiş versiyonu çalıştır
python src/training/train_yolo_improved.py

# 3. 20-30 epoch sonra results.csv'yi kontrol et
# Recall artıyor mu?
```

## Beklenen Sonuçlar

- **Hedef Recall**: 0.50+ (minimum)
- **İyi Recall**: 0.60+
- **Mükemmel Recall**: 0.70+

## Inference Sırasında Recall Artırma

Model eğitildikten sonra:

```python
# Confidence threshold düşür
model.predict(
    source='image.jpg',
    conf=0.1,      # 0.25 yerine 0.1
    iou=0.5,       # NMS threshold
    max_det=1000   # Maksimum detection sayısı artır
)
```

## Önemli Notlar

1. **Precision vs Recall Trade-off**: Recall artarken precision düşebilir
2. **Baykar için**: Hedefi kaçırmamak önemli, yanlış alarm tolere edilebilir
3. **Real-time**: Recall için model yavaşlayabilir
4. **Test**: Farklı confidence threshold'ları test et

## Sonraki Adımlar

1. ✅ Mevcut eğitimi durdur
2. ✅ `train_yolo_improved.py` çalıştır
3. ⏳ 20-30 epoch bekle
4. 📊 Results.csv'yi kontrol et
5. 🎯 Recall 0.50+ ise devam, değilse Strateji 2'ye geç
