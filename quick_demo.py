"""
Hızlı Demo - Otomatik Test
"""
from demo_detection_tracking import DroneDetectionTracker

# Tracker oluştur
tracker = DroneDetectionTracker()

# Test veri setinden örnekleri otomatik test et
tracker.test_on_sample()

print("\n" + "=" * 70)
print("✅ Demo tamamlandı!")
print("📁 Sonuçlar: runs/demo/")
print("\nSonraki adımlar:")
print("  1. runs/demo/ klasöründeki sonuçları incele")
print("  2. Eğer performans kötüyse:")
print("     python src/training/train_yolo_hybrid.py")
print("  3. Eğer performans iyiyse:")
print("     - Tracking sistemini entegre et")
print("     - API oluştur")
print("     - Deployment için hazırla")
print("=" * 70)
