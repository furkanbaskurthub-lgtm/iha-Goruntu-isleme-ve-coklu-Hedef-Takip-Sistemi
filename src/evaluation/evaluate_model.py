"""
Model değerlendirme ve test scripti
"""
from ultralytics import YOLO
from pathlib import Path
import cv2
import numpy as np


def evaluate_model(model_path, data_config='data/visdrone_config.yaml'):
    """
    Eğitilmiş modeli değerlendir
    """
    print("=" * 60)
    print("📊 MODEL DEĞERLENDİRME")
    print("=" * 60)
    
    model = YOLO(model_path)
    
    # Validation seti üzerinde değerlendirme
    metrics = model.val(data=data_config, split='val')
    
    print("\n🎯 Metrikler:")
    print(f"  • mAP50: {metrics.box.map50:.4f}")
    print(f"  • mAP50-95: {metrics.box.map:.4f}")
    print(f"  • Precision: {metrics.box.mp:.4f}")
    print(f"  • Recall: {metrics.box.mr:.4f}")
    
    return metrics


def test_on_images(model_path, test_images_dir, output_dir='runs/test', conf=0.25):
    """
    Test görüntüleri üzerinde tahmin yap
    """
    model = YOLO(model_path)
    test_images_dir = Path(test_images_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🖼️  Test görüntüleri işleniyor: {test_images_dir}")
    
    image_files = list(test_images_dir.glob('*.jpg')) + list(test_images_dir.glob('*.png'))
    
    for img_file in image_files[:10]:  # İlk 10 görüntü
        results = model(img_file, conf=conf)
        
        # Sonuçları kaydet
        for i, result in enumerate(results):
            annotated = result.plot()
            output_path = output_dir / f"{img_file.stem}_pred.jpg"
            cv2.imwrite(str(output_path), annotated)
            
            # Tespit edilen nesneleri yazdır
            if len(result.boxes) > 0:
                print(f"\n📸 {img_file.name}:")
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    xyxy = box.xyxy[0].cpu().numpy()
                    print(f"  • {model.names[cls]}: {conf:.2f} @ [{xyxy[0]:.0f}, {xyxy[1]:.0f}, {xyxy[2]:.0f}, {xyxy[3]:.0f}]")
    
    print(f"\n✅ Sonuçlar kaydedildi: {output_dir}")


def benchmark_speed(model_path, imgsz=640):
    """
    Model hız testi (FPS)
    """
    model = YOLO(model_path)
    
    print("\n⚡ HIZ TESTİ")
    print(f"Görüntü boyutu: {imgsz}x{imgsz}")
    
    # Dummy görüntü oluştur
    dummy_img = np.random.randint(0, 255, (imgsz, imgsz, 3), dtype=np.uint8)
    
    # Warmup
    for _ in range(10):
        model(dummy_img, verbose=False)
    
    # Benchmark
    import time
    n_runs = 100
    start = time.time()
    for _ in range(n_runs):
        model(dummy_img, verbose=False)
    end = time.time()
    
    avg_time = (end - start) / n_runs
    fps = 1 / avg_time
    
    print(f"  • Ortalama süre: {avg_time*1000:.2f} ms")
    print(f"  • FPS: {fps:.1f}")
    print(f"  • İHA için uygun: {'✅ Evet' if fps >= 30 else '⚠️  Hayır (30 FPS altı)'}")


if __name__ == "__main__":
    # En iyi modeli değerlendir
    model_path = 'runs/train/visdrone_yolo/weights/best.pt'
    
    # Değerlendirme
    evaluate_model(model_path)
    
    # Test görüntüleri üzerinde tahmin
    test_on_images(
        model_path,
        'data/raw/VisDrone2019-DET-test-dev/VisDrone2019-DET-test-dev/images',
        output_dir='runs/test/predictions'
    )
    
    # Hız testi
    benchmark_speed(model_path)
