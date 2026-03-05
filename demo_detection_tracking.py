"""
BAYKAR İHA Projesi - Hızlı Demo
Nesne Tespiti + Tracking (ByteTrack)
"""
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import time


class DroneDetectionTracker:
    """İHA görüntülerinde nesne tespiti ve takibi"""
    
    def __init__(self, model_path='runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt'):
        """
        Args:
            model_path: Eğitilmiş YOLO model yolu
        """
        print("🚁 BAYKAR İHA Tespit ve Takip Sistemi")
        print("=" * 60)
        print(f"📦 Model yükleniyor: {model_path}")
        
        self.model = YOLO(model_path)
        
        # VisDrone sınıf isimleri (doğru mapping)
        self.class_names = {
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
        
        print("✅ Model hazır!")
        print("=" * 60)
    
    def detect_image(self, image_path, conf=0.25, save=True):
        """
        Tek görüntüde tespit yap
        
        Args:
            image_path: Görüntü dosya yolu
            conf: Confidence threshold
            save: Sonucu kaydet
        """
        print(f"\n📸 Görüntü işleniyor: {image_path}")
        
        # Tespit yap
        results = self.model.predict(
            source=image_path,
            conf=conf,
            iou=0.5,
            max_det=1000,  # Maksimum tespit sayısı
            device='0' if self.model.device.type == 'cuda' else 'cpu',
            verbose=False
        )
        
        # Sonuçları göster
        result = results[0]
        detections = len(result.boxes)
        
        print(f"✅ {detections} nesne tespit edildi")
        
        # Sınıf bazında sayım
        if detections > 0:
            classes = result.boxes.cls.cpu().numpy()
            unique, counts = np.unique(classes, return_counts=True)
            
            print("\n📊 Tespit edilen nesneler:")
            for cls, count in zip(unique, counts):
                cls_name = self.class_names.get(int(cls), f'class_{int(cls)}')
                print(f"   • {cls_name}: {count}")
        
        # Kaydet
        if save:
            output_path = Path('runs/demo') / Path(image_path).name
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Görüntüyü çiz
            annotated = result.plot()
            cv2.imwrite(str(output_path), annotated)
            print(f"\n💾 Sonuç kaydedildi: {output_path}")
        
        return results
    
    def track_video(self, video_path, conf=0.25, save=True):
        """
        Video üzerinde tespit + tracking yap
        
        Args:
            video_path: Video dosya yolu
            conf: Confidence threshold
            save: Sonucu kaydet
        """
        print(f"\n🎥 Video işleniyor: {video_path}")
        
        # Video tracking (ByteTrack otomatik)
        results = self.model.track(
            source=video_path,
            conf=conf,
            iou=0.5,
            tracker='bytetrack.yaml',  # ByteTrack kullan
            device='0' if self.model.device.type == 'cuda' else 'cpu',
            stream=True,
            verbose=False
        )
        
        # Video bilgisi
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        print(f"📹 Video: {width}x{height} @ {fps}fps, {total_frames} frame")
        
        # Video writer
        if save:
            output_path = Path('runs/demo') / f"tracked_{Path(video_path).name}"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        # Frame işle
        frame_count = 0
        start_time = time.time()
        
        for result in results:
            frame_count += 1
            
            # Tracking ID'leri al
            if result.boxes.id is not None:
                track_ids = result.boxes.id.cpu().numpy().astype(int)
                num_tracked = len(np.unique(track_ids))
            else:
                num_tracked = 0
            
            # Progress
            if frame_count % 30 == 0:
                elapsed = time.time() - start_time
                fps_current = frame_count / elapsed
                print(f"   Frame {frame_count}/{total_frames} | "
                      f"{num_tracked} takip edilen | "
                      f"{fps_current:.1f} FPS")
            
            # Kaydet
            if save:
                annotated = result.plot()
                out.write(annotated)
        
        if save:
            out.release()
            print(f"\n💾 Video kaydedildi: {output_path}")
        
        elapsed = time.time() - start_time
        print(f"\n✅ Tamamlandı! Süre: {elapsed:.1f}s, Ortalama FPS: {frame_count/elapsed:.1f}")
    
    def test_on_sample(self):
        """Test veri setinden örnek görüntülerde test et"""
        print("\n🧪 Test veri setinden örnekler test ediliyor...")
        
        # Test görüntüleri bul
        test_dir = Path('data/raw/VisDrone2019-DET-test-dev/VisDrone2019-DET-test-dev/images')
        
        if not test_dir.exists():
            print("⚠️  Test veri seti bulunamadı")
            return
        
        # İlk 5 görüntüyü test et
        test_images = list(test_dir.glob('*.jpg'))[:5]
        
        print(f"📸 {len(test_images)} görüntü test edilecek\n")
        
        for img_path in test_images:
            self.detect_image(str(img_path), conf=0.25, save=True)
        
        print("\n✅ Test tamamlandı! Sonuçlar: runs/demo/")


def main():
    """Ana fonksiyon"""
    
    # Tracker oluştur
    tracker = DroneDetectionTracker()
    
    print("\n" + "=" * 60)
    print("KULLANIM SEÇENEKLERİ:")
    print("=" * 60)
    print("1. Test veri setinden örnekler (otomatik)")
    print("2. Kendi görüntünüzü test edin")
    print("3. Video üzerinde tracking")
    print("=" * 60)
    
    choice = input("\nSeçiminiz (1-3): ").strip()
    
    if choice == '1':
        tracker.test_on_sample()
    
    elif choice == '2':
        img_path = input("Görüntü yolu: ").strip()
        conf = float(input("Confidence threshold (0.1-0.9, önerilen 0.25): ") or "0.25")
        tracker.detect_image(img_path, conf=conf)
    
    elif choice == '3':
        video_path = input("Video yolu: ").strip()
        conf = float(input("Confidence threshold (0.1-0.9, önerilen 0.25): ") or "0.25")
        tracker.track_video(video_path, conf=conf)
    
    else:
        print("❌ Geçersiz seçim")
    
    print("\n" + "=" * 60)
    print("🎯 BAYKAR İHA Projesi - Demo Tamamlandı")
    print("=" * 60)


if __name__ == "__main__":
    main()
