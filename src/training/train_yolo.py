"""
YOLOv8/v10 Model Eğitim Scripti
Baykar İHA Projesi - VisDrone Dataset
"""
import os
from pathlib import Path
from ultralytics import YOLO
import torch


def train_model(
    model_name='yolov8n.pt',
    data_config='data/visdrone_config.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device='0',
    project='runs/train',
    name='visdrone_yolo'
):
    """
    YOLO modelini VisDrone veri seti ile eğit
    
    Args:
        model_name: Başlangıç modeli (yolov8n.pt, yolov8s.pt, yolov10n.pt, vb.)
        data_config: Veri seti konfigürasyon dosyası
        epochs: Eğitim epoch sayısı
        imgsz: Görüntü boyutu
        batch: Batch size
        device: GPU device ('0', 'cpu', veya '0,1' multi-GPU için)
        project: Sonuçların kaydedileceği klasör
        name: Eğitim run ismi
    """
    
    print("=" * 70)
    print("🚁 BAYKAR İHA PROJESİ - YOLO EĞİTİMİ")
    print("=" * 70)
    print(f"📦 Model: {model_name}")
    print(f"📊 Dataset: {data_config}")
    print(f"🔢 Epochs: {epochs}")
    print(f"📐 Image Size: {imgsz}")
    print(f"🎯 Batch Size: {batch}")
    print(f"💻 Device: {device}")
    print("=" * 70)
    
    # GPU kontrolü
    if device != 'cpu':
        if torch.cuda.is_available():
            print(f"✅ GPU kullanılabilir: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  GPU bulunamadı, CPU kullanılacak")
            device = 'cpu'
    
    # Model yükle
    model = YOLO(model_name)
    
    # Eğitimi başlat
    results = model.train(
        data=data_config,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device=device,
        project=project,
        name=name,
        # Optimizasyon parametreleri
        patience=50,          # Early stopping patience
        save=True,            # Checkpoint kaydet
        save_period=10,       # Her 10 epoch'ta kaydet
        cache=False,          # RAM'de cache (büyük veri setleri için False)
        workers=0,            # Multiprocessing kapalı (Windows page file hatası için)
        # Augmentation
        hsv_h=0.015,         # Hue augmentation
        hsv_s=0.7,           # Saturation augmentation
        hsv_v=0.4,           # Value augmentation
        degrees=0.0,         # Rotation (İHA görüntüleri için 0)
        translate=0.1,       # Translation
        scale=0.5,           # Scale
        shear=0.0,           # Shear
        perspective=0.0,     # Perspective (İHA için 0)
        flipud=0.0,          # Vertical flip (İHA için 0)
        fliplr=0.5,          # Horizontal flip
        mosaic=1.0,          # Mosaic augmentation
        mixup=0.0,           # Mixup augmentation
        # Diğer
        cos_lr=True,         # Cosine learning rate scheduler
        close_mosaic=10,     # Son 10 epoch'ta mosaic'i kapat
        amp=True,            # Automatic Mixed Precision
        fraction=1.0,        # Veri setinin kullanılacak oranı
        profile=False,       # Profiling
        freeze=None,         # Freeze layers
        # Multi-scale training
        multi_scale=False,   # 4GB GPU için kapatıldı
        rect=False,          # Rectangular training kapalı (ZeroDivisionError fix)
        # Optimizer
        optimizer='auto',    # SGD, Adam, AdamW, NAdam, RAdam, RMSProp, auto
        lr0=0.01,           # Initial learning rate
        lrf=0.01,           # Final learning rate (lr0 * lrf)
        momentum=0.937,     # SGD momentum
        weight_decay=0.0005, # Weight decay
        warmup_epochs=3.0,  # Warmup epochs
        warmup_momentum=0.8, # Warmup momentum
        warmup_bias_lr=0.1, # Warmup bias learning rate
        # Loss weights
        box=7.5,            # Box loss gain
        cls=0.5,            # Class loss gain
        dfl=1.5,            # DFL loss gain
        # Validation
        val=True,           # Validate during training
        plots=True,         # Grafikleri kaydet
        # Verbose
        verbose=True,       # Detaylı çıktı
    )
    
    print("\n" + "=" * 70)
    print("✅ EĞİTİM TAMAMLANDI!")
    print("=" * 70)
    print(f"📁 Sonuçlar: {results.save_dir}")
    print(f"🏆 En iyi model: {results.save_dir}/weights/best.pt")
    print(f"📊 Son model: {results.save_dir}/weights/last.pt")
    print("=" * 70)
    
    return results


def resume_training(checkpoint_path, epochs=100):
    """
    Kesintiye uğramış eğitimi devam ettir
    """
    print(f"🔄 Eğitim devam ettiriliyor: {checkpoint_path}")
    model = YOLO(checkpoint_path)
    results = model.train(resume=True, epochs=epochs)
    return results


if __name__ == "__main__":
    # Eğitim parametreleri
    # Küçük model (hızlı test için)
    # train_model(model_name='yolov8n.pt', epochs=50, batch=16)
    
    # Orta model (denge için önerilen) - TAM EĞİTİM
    # RTX 3050 Ti (4GB) için optimize edilmiş ayarlar
    train_model(
        model_name='yolov8s.pt', 
        epochs=150,              # Daha fazla epoch
        batch=8,                 # 4GB GPU için düşürüldü
        imgsz=640,
        device='0',              # GPU kullan (varsa)
        project='runs/train',
        name='visdrone_yolo_full'
    )
    
    # Büyük model (en iyi doğruluk için)
    # train_model(model_name='yolov8m.pt', epochs=200, batch=8)
    
    # YOLOv10 (en yeni)
    # train_model(model_name='yolov10n.pt', epochs=150, batch=16)
