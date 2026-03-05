"""
Hızlı Model Performans Değerlendirmesi
"""
from ultralytics import YOLO
import pandas as pd
from pathlib import Path


def evaluate_model(model_path='runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt'):
    """Model performansını değerlendir"""
    
    print("=" * 70)
    print("🎯 MODEL PERFORMANS DEĞERLENDİRMESİ")
    print("=" * 70)
    
    # Model yükle
    print(f"\n📦 Model: {model_path}")
    model = YOLO(model_path)
    
    # Validation set üzerinde değerlendir
    print("\n🔍 Validation seti üzerinde değerlendirme yapılıyor...")
    results = model.val(
        data='data/visdrone_config.yaml',
        split='val',
        batch=8,
        device='0',
        verbose=False
    )
    
    # Sonuçları göster
    print("\n" + "=" * 70)
    print("📊 PERFORMANS METRİKLERİ")
    print("=" * 70)
    
    metrics = {
        'Precision': results.box.mp,
        'Recall': results.box.mr,
        'mAP50': results.box.map50,
        'mAP50-95': results.box.map,
    }
    
    for metric, value in metrics.items():
        status = "✅" if value > 0.5 else "⚠️" if value > 0.3 else "❌"
        print(f"{status} {metric:15s}: {value:.4f} ({value*100:.2f}%)")
    
    # Sınıf bazında performans
    print("\n" + "=" * 70)
    print("📋 SINIF BAZINDA PERFORMANS")
    print("=" * 70)
    
    class_names = {
        0: 'pedestrian',
        1: 'people',
        2: 'bicycle',
        3: 'car',
        4: 'van',
        5: 'truck',
        6: 'tricycle',
        7: 'awning-tricycle',
        8: 'bus',
        9: 'motor'
    }
    
    # Sınıf bazında AP50
    if hasattr(results.box, 'ap50'):
        ap50_per_class = results.box.ap50
        for i, ap in enumerate(ap50_per_class):
            if i < len(class_names):
                cls_name = class_names[i]
                status = "✅" if ap > 0.5 else "⚠️" if ap > 0.3 else "❌"
                print(f"{status} {cls_name:20s}: {ap:.4f}")
    
    # Eğitim geçmişi
    print("\n" + "=" * 70)
    print("📈 EĞİTİM GEÇMİŞİ")
    print("=" * 70)
    
    results_csv = Path(model_path).parent.parent / 'results.csv'
    if results_csv.exists():
        df = pd.read_csv(results_csv)
        
        # Son 10 epoch
        last_10 = df.tail(10)
        
        print(f"\nToplam epoch: {len(df)}")
        print(f"En iyi epoch: {df['metrics/mAP50(B)'].idxmax() + 1}")
        print(f"En iyi mAP50: {df['metrics/mAP50(B)'].max():.4f}")
        print(f"En iyi Recall: {df['metrics/recall(B)'].max():.4f}")
        
        print("\nSon 10 epoch ortalamaları:")
        print(f"  Precision: {last_10['metrics/precision(B)'].mean():.4f}")
        print(f"  Recall:    {last_10['metrics/recall(B)'].mean():.4f}")
        print(f"  mAP50:     {last_10['metrics/mAP50(B)'].mean():.4f}")
        print(f"  mAP50-95:  {last_10['metrics/mAP50-95(B)'].mean():.4f}")
    
    # Karar
    print("\n" + "=" * 70)
    print("🎯 KARAR")
    print("=" * 70)
    
    recall = results.box.mr
    map50 = results.box.map50
    
    if recall >= 0.50 and map50 >= 0.40:
        print("✅ Model performansı İYİ!")
        print("   → Uygulamaya geçilebilir")
        print("   → Demo için: python demo_detection_tracking.py")
    elif recall >= 0.40 and map50 >= 0.35:
        print("⚠️  Model performansı ORTA")
        print("   → Uygulamada test edilebilir")
        print("   → Eğer sonuç kötüyse yeniden eğit:")
        print("     python src/training/train_yolo_hybrid.py")
    else:
        print("❌ Model performansı DÜŞÜK")
        print("   → Yeniden eğitim önerilir:")
        print("     python src/training/train_yolo_hybrid.py")
    
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    evaluate_model()
