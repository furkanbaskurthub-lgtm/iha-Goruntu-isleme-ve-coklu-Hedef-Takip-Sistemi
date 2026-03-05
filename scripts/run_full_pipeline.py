"""
Tam pipeline: Veri hazırlama -> Eğitim -> Değerlendirme -> Tracking
"""
import sys
from pathlib import Path

# Proje root'unu path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.prepare_visdrone import prepare_dataset
from src.training.train_yolo import train_model
from src.evaluation.evaluate_model import evaluate_model, test_on_images, benchmark_speed


def run_pipeline(
    skip_prepare=False,
    skip_train=False,
    model_name='yolov8s.pt',
    epochs=100,
    batch=16
):
    """
    Tam pipeline'ı çalıştır
    """
    print("\n" + "=" * 70)
    print("🚁 BAYKAR İHA PROJESİ - TAM PIPELINE")
    print("=" * 70)
    
    # 1. Veri Hazırlama
    if not skip_prepare:
        print("\n📦 ADIM 1: Veri Hazırlama")
        print("-" * 70)
        prepare_dataset()
    else:
        print("\n⏭️  Veri hazırlama atlandı")
    
    # 2. Model Eğitimi
    if not skip_train:
        print("\n🎓 ADIM 2: Model Eğitimi")
        print("-" * 70)
        results = train_model(
            model_name=model_name,
            epochs=epochs,
            batch=batch
        )
        model_path = f"{results.save_dir}/weights/best.pt"
    else:
        print("\n⏭️  Eğitim atlandı, mevcut model kullanılacak")
        model_path = 'runs/train/visdrone_yolo/weights/best.pt'
    
    # 3. Model Değerlendirme
    print("\n📊 ADIM 3: Model Değerlendirme")
    print("-" * 70)
    
    # Metrikler
    evaluate_model(model_path)
    
    # Test görüntüleri
    test_on_images(
        model_path,
        'data/raw/VisDrone2019-DET-test-dev/VisDrone2019-DET-test-dev/images',
        output_dir='runs/test/predictions'
    )
    
    # Hız testi
    benchmark_speed(model_path)
    
    print("\n" + "=" * 70)
    print("✅ PIPELINE TAMAMLANDI!")
    print("=" * 70)
    print(f"\n📁 Model: {model_path}")
    print("📁 Test sonuçları: runs/test/predictions/")
    print("\n💡 Tracking için:")
    print(f"   from src.core.tracker import UAVTracker")
    print(f"   tracker = UAVTracker(model_path='{model_path}')")
    print(f"   tracker.process_video('video.mp4')")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Baykar İHA Projesi - Tam Pipeline')
    parser.add_argument('--skip-prepare', action='store_true', help='Veri hazırlamayı atla')
    parser.add_argument('--skip-train', action='store_true', help='Eğitimi atla')
    parser.add_argument('--model', default='yolov8s.pt', help='Model adı (yolov8n.pt, yolov8s.pt, vb.)')
    parser.add_argument('--epochs', type=int, default=100, help='Epoch sayısı')
    parser.add_argument('--batch', type=int, default=16, help='Batch size')
    
    args = parser.parse_args()
    
    run_pipeline(
        skip_prepare=args.skip_prepare,
        skip_train=args.skip_train,
        model_name=args.model,
        epochs=args.epochs,
        batch=args.batch
    )
