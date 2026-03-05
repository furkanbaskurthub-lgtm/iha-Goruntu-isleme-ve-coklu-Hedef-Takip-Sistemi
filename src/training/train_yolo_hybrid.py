"""
YOLOv8 Model Eğitim Scripti - Hibrit Versiyon
En iyi parametrelerin kombinasyonu
"""
import os
from pathlib import Path
from ultralytics import YOLO
import torch


def train_hybrid_model(
    model_name='yolov8s.pt',
    data_config='data/visdrone_config.yaml',
    resume_from_best=True
):
    """
    Hibrit yaklaşım: İmgsz=960 + Agresif augmentation + Recall optimize
    """
    
    print("=" * 70)
    print("🚁 BAYKAR İHA PROJESİ - HİBRİT EĞİTİM")
    print("=" * 70)
    print("📦 imgsz=960 (küçük nesneler için)")
    print("🎨 Agresif augmentation (recall için)")
    print("🎯 AdamW optimizer + düşük LR")
    print("=" * 70)
    
    # GPU kontrolü
    if torch.cuda.is_available():
        print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
        device = '0'
    else:
        print("⚠️  GPU bulunamadı, CPU kullanılacak")
        device = 'cpu'
    
    # Mevcut en iyi modelden devam et
    if resume_from_best:
        best_model_path = "runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt"
        if os.path.exists(best_model_path):
            print(f"📦 Mevcut en iyi modelden devam: {best_model_path}")
            model_name = best_model_path
        else:
            print("⚠️  Önceki model bulunamadı, yeni model başlatılıyor")
    
    # Model yükle
    model = YOLO(model_name)
    
    # HİBRİT PARAMETRELER - En iyilerin kombinasyonu
    results = model.train(
        data=data_config,
        
        # Temel parametreler
        epochs=60,            # Senin önerinle
        imgsz=960,            # Senin önerinle - küçük nesneler için kritik
        batch=4,              # 960 için uygun
        device=device,
        project='runs/train',
        name='visdrone_hybrid',
        workers=0,            # Windows için güvenli
        
        # Kaydetme
        patience=30,
        save=True,
        save_period=10,
        cache=False,
        
        # Augmentation - Agresif (recall için)
        hsv_h=0.03,
        hsv_s=0.8,
        hsv_v=0.5,
        degrees=5.0,          # Hafif rotasyon
        translate=0.2,
        scale=0.7,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,           # Benim önerimle - maksimum
        mixup=0.15,           # Benim önerimle - daha fazla
        copy_paste=0.1,       # Ekstra augmentation
        
        # Loss weights - Recall optimize
        box=8.0,              # Senin önerinle
        cls=0.3,              # Benim önerimle - recall için düşük
        dfl=1.5,
        
        # Optimizer - Senin önerinle
        optimizer='AdamW',
        lr0=0.0008,           # Senin önerinle - konservatif
        lrf=0.001,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=5.0,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        
        # Diğer
        cos_lr=True,
        close_mosaic=20,      # Senin önerinle
        amp=True,
        fraction=1.0,
        multi_scale=False,    # 4GB GPU için kapalı
        
        # Inference parametreleri - Recall için
        conf=0.001,           # Çok düşük confidence
        iou=0.6,              # NMS threshold
        
        # Validation
        val=True,
        plots=True,
        verbose=True,
    )
    
    print("\n" + "=" * 70)
    print("✅ EĞİTİM TAMAMLANDI!")
    print("=" * 70)
    print(f"📁 Sonuçlar: {results.save_dir}")
    print(f"🏆 En iyi model: {results.save_dir}/weights/best.pt")
    print("\n📊 Sonraki adım:")
    print("   python src/evaluation/evaluate_model.py")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                  HİBRİT EĞİTİM STRATEJİSİ                   ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  • imgsz=960 (küçük nesneler için)                          ║
    ║  • Agresif augmentation (recall artırma)                    ║
    ║  • AdamW + düşük LR (stabil eğitim)                         ║
    ║  • cls=0.3 (recall optimize)                                ║
    ║  • Mevcut best.pt'den devam                                 ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  Tahmini süre: ~5-6 saat (60 epoch)                        ║
    ║  Beklenen recall: 0.50+ (şu an 0.40)                       ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    input("Devam etmek için Enter'a basın (veya Ctrl+C ile iptal)...")
    
    train_hybrid_model(
        model_name='yolov8s.pt',
        resume_from_best=True  # Mevcut best.pt'den devam et
    )
