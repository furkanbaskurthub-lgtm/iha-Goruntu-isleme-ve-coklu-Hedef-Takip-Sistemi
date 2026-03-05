"""
YOLOv8 Model Eğitim Scripti - İyileştirilmiş Versiyon
Düşük Recall için optimize edilmiş
"""
import os
from pathlib import Path
from ultralytics import YOLO
import torch


def train_improved_model(
    model_name='yolov8s.pt',
    data_config='data/visdrone_config.yaml',
    epochs=100,
    imgsz=640,
    batch=8,
    device='0',
    project='runs/train',
    name='visdrone_improved'
):
    """
    Düşük recall problemini çözmek için optimize edilmiş eğitim
    """
    
    print("=" * 70)
    print("🚁 BAYKAR İHA PROJESİ - İYİLEŞTİRİLMİŞ EĞİTİM")
    print("=" * 70)
    print(f"📦 Model: {model_name}")
    print(f"🎯 Hedef: Recall artırma")
    print("=" * 70)
    
    # GPU kontrolü
    if device != 'cpu':
        if torch.cuda.is_available():
            print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  GPU bulunamadı, CPU kullanılacak")
            device = 'cpu'
    
    # Model yükle
    model = YOLO(model_name)
    
    # Recall artırmak için optimize edilmiş parametreler
    results = model.train(
        data=data_config,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device=device,
        project=project,
        name=name,
        workers=0,
        
        # Recall artırma stratejileri
        patience=30,          # Daha erken durma
        save=True,
        save_period=10,
        cache=False,
        
        # Augmentation - Daha agresif
        hsv_h=0.03,          # Daha fazla renk varyasyonu
        hsv_s=0.8,
        hsv_v=0.5,
        degrees=5.0,         # Hafif rotasyon (İHA için)
        translate=0.2,       # Daha fazla translation
        scale=0.7,           # Daha fazla scale
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.15,          # Mixup ekle
        copy_paste=0.1,      # Copy-paste augmentation
        
        # Loss weights - Recall için optimize
        box=7.5,
        cls=0.3,             # Class loss azaltıldı
        dfl=1.5,
        
        # Optimizer
        optimizer='AdamW',   # AdamW daha iyi sonuç verebilir
        lr0=0.001,           # Daha düşük learning rate
        lrf=0.001,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=5.0,   # Daha uzun warmup
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        
        # Diğer
        cos_lr=True,
        close_mosaic=15,
        amp=True,
        fraction=1.0,
        multi_scale=False,   # 4GB GPU için kapalı
        
        # Validation
        val=True,
        plots=True,
        verbose=True,
        
        # Confidence threshold düşür (recall için)
        conf=0.001,          # Çok düşük confidence threshold
        iou=0.6,             # NMS IoU threshold
    )
    
    print("\n" + "=" * 70)
    print("✅ EĞİTİM TAMAMLANDI!")
    print("=" * 70)
    print(f"📁 Sonuçlar: {results.save_dir}")
    print(f"🏆 En iyi model: {results.save_dir}/weights/best.pt")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    # Strateji 1: Mevcut modelden devam et (transfer learning)
    # Eğer runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt varsa
    import os
    best_model_path = "runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt"
    
    if os.path.exists(best_model_path):
        print(f"📦 Mevcut en iyi modelden devam ediliyor: {best_model_path}")
        train_improved_model(
            model_name=best_model_path,  # Önceki en iyi modelden başla
            epochs=50,                    # 50 epoch daha
            batch=8,
            imgsz=640,
            device='0',
            project='runs/train',
            name='visdrone_improved_v1'
        )
    else:
        print("⚠️  Önceki model bulunamadı, sıfırdan başlanıyor")
        train_improved_model(
            model_name='yolov8s.pt',
            epochs=100,
            batch=8,
            imgsz=640,
            device='0',
            project='runs/train',
            name='visdrone_improved_v1'
        )
