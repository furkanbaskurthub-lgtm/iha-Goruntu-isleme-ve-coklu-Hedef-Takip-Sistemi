"""
Pretrained VisDrone modeli indir veya YOLOv8 ile hızlı test
"""
from ultralytics import YOLO
import os

def download_and_test():
    """
    Pretrained YOLOv8 modelini indir ve VisDrone için hazırla
    """
    print("=" * 60)
    print("🚁 Pretrained Model İndiriliyor")
    print("=" * 60)
    
    # YOLOv8s pretrained model (COCO dataset ile eğitilmiş)
    # VisDrone sınıfları COCO'nun alt kümesi olduğu için kullanılabilir
    model = YOLO('yolov8s.pt')
    
    print("\n✅ Model indirildi: yolov8s.pt")
    print("\n💡 Bu model COCO dataset ile eğitilmiş (80 sınıf)")
    print("   VisDrone sınıfları (araç, insan, bisiklet vb.) içerir")
    print("\n📁 Model kaydedildi: yolov8s.pt")
    
    # Test için model bilgisi
    print("\n📊 Model Bilgisi:")
    print(f"   • Parametreler: 11.2M")
    print(f"   • GFLOPs: 28.7")
    print(f"   • Sınıflar: {len(model.names)}")
    
    # VisDrone ile uyumlu sınıflar
    visdrone_compatible = {
        'person': 0,      # pedestrian
        'bicycle': 1,     # bicycle
        'car': 2,         # car
        'motorcycle': 3,  # motor
        'bus': 5,         # bus
        'truck': 7        # truck
    }
    
    print("\n🎯 VisDrone Uyumlu COCO Sınıfları:")
    for name, idx in visdrone_compatible.items():
        print(f"   • {name}")
    
    return model

if __name__ == "__main__":
    model = download_and_test()
    
    print("\n" + "=" * 60)
    print("✅ Hazır! Şimdi tracking'i test edebilirsiniz:")
    print("=" * 60)
    print("\nKullanım:")
    print("  from src.core.tracker import UAVTracker")
    print("  tracker = UAVTracker(model_path='yolov8s.pt')")
    print("  tracker.process_image('test_image.jpg')")
