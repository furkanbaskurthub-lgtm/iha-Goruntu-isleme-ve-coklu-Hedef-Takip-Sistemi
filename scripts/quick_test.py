"""
Hızlı test scripti - Eğitilmiş modeli test et
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.tracker import UAVTracker


def quick_test():
    """
    Eğitilmiş modeli hızlıca test et
    """
    print("🚁 Baykar İHA Projesi - Hızlı Test")
    print("=" * 60)
    
    # Model yolu
    model_path = 'runs/train/visdrone_yolo/weights/best.pt'
    
    if not Path(model_path).exists():
        print(f"❌ Model bulunamadı: {model_path}")
        print("\nÖnce modeli eğitin:")
        print("  python src/training/train_yolo.py")
        return
    
    # Tracker'ı başlat
    tracker = UAVTracker(model_path=model_path)
    
    # Test görüntüsü
    test_image = 'data/raw/VisDrone2019-DET-test-dev/VisDrone2019-DET-test-dev/images/0000006_00159_d_0000001.jpg'
    
    if Path(test_image).exists():
        print(f"\n📸 Test görüntüsü işleniyor: {test_image}")
        tracker.process_image(
            test_image,
            output_path='runs/quick_test.jpg',
            conf=0.3
        )
    else:
        print(f"⚠️  Test görüntüsü bulunamadı: {test_image}")
    
    print("\n✅ Test tamamlandı!")
    print("📁 Sonuç: runs/quick_test.jpg")


if __name__ == "__main__":
    quick_test()
