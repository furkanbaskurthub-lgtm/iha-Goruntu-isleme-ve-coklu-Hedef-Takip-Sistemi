import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
from collections import defaultdict


class UAVTracker:
    """
    İHA görüntülerinden nesne tespiti ve takibi
    YOLOv8/v10 + ByteTrack algoritması
    """
    
    def __init__(self, model_path='yolov8n.pt', tracker_config='bytetrack.yaml'):
        """
        Args:
            model_path: Eğitilmiş YOLO model yolu
            tracker_config: Tracker konfigürasyonu (bytetrack.yaml veya botsort.yaml)
        """
        print(f"🚁 UAV Tracker başlatılıyor...")
        print(f"  • Model: {model_path}")
        print(f"  • Tracker: {tracker_config}")
        
        self.model = YOLO(model_path)
        self.tracker_config = tracker_config
        self.track_history = defaultdict(lambda: [])

    def process_video(self, video_path, output_path='runs/output_video.mp4', 
                     conf=0.25, iou=0.45, show=False, save_txt=False):
        """
        Video üzerinde nesne tespiti ve takibi
        
        Args:
            video_path: Giriş video yolu
            output_path: Çıkış video yolu
            conf: Confidence threshold
            iou: IOU threshold
            show: Görüntüyü göster
            save_txt: Sonuçları txt dosyasına kaydet
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ Video açılamadı: {video_path}")
            return
        
        # Video özellikleri
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"\n📹 Video işleniyor:")
        print(f"  • Boyut: {width}x{height}")
        print(f"  • FPS: {fps}")
        print(f"  • Toplam frame: {total_frames}")
        
        # Output klasörünü oluştur
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        # Txt dosyası için
        if save_txt:
            txt_path = output_path.with_suffix('.txt')
            txt_file = open(txt_path, 'w')
        
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Tracking (persist=True ile her nesneye sabit ID verilir)
            results = self.model.track(
                frame, 
                persist=True, 
                tracker=self.tracker_config,
                conf=conf,
                iou=iou,
                verbose=False
            )
            
            # Sonuçları işle
            annotated_frame = frame.copy()
            
            if results[0].boxes is not None and results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                track_ids = results[0].boxes.id.cpu().numpy().astype(int)
                classes = results[0].boxes.cls.cpu().numpy().astype(int)
                confidences = results[0].boxes.conf.cpu().numpy()
                
                for box, track_id, cls, conf in zip(boxes, track_ids, classes, confidences):
                    x1, y1, x2, y2 = box
                    
                    # Track history güncelle
                    center = ((x1 + x2) / 2, (y1 + y2) / 2)
                    self.track_history[track_id].append(center)
                    
                    # Son 30 frame'i tut
                    if len(self.track_history[track_id]) > 30:
                        self.track_history[track_id].pop(0)
                    
                    # Bounding box çiz
                    color = self._get_color(track_id)
                    cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    
                    # Label
                    label = f"ID:{track_id} {self.model.names[cls]} {conf:.2f}"
                    cv2.putText(annotated_frame, label, (int(x1), int(y1) - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    
                    # Track çizgisi
                    points = np.array(self.track_history[track_id], dtype=np.int32).reshape((-1, 1, 2))
                    cv2.polylines(annotated_frame, [points], False, color, 2)
                    
                    # Txt dosyasına kaydet
                    if save_txt:
                        txt_file.write(f"{frame_count},{track_id},{cls},{conf:.4f},{x1:.2f},{y1:.2f},{x2:.2f},{y2:.2f}\n")
            
            # Frame bilgisi
            cv2.putText(annotated_frame, f"Frame: {frame_count}/{total_frames}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Kaydet
            out.write(annotated_frame)
            
            # Göster
            if show:
                cv2.imshow("Baykar AI - UAV Target Tracking", annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Progress
            if frame_count % 30 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"  ⏳ İşleniyor: {progress:.1f}% ({frame_count}/{total_frames})")
        
        cap.release()
        out.release()
        if save_txt:
            txt_file.close()
        if show:
            cv2.destroyAllWindows()
        
        print(f"\n✅ Video işleme tamamlandı!")
        print(f"  • Çıkış: {output_path}")
        if save_txt:
            print(f"  • Tracking sonuçları: {txt_path}")
    
    def process_image(self, image_path, output_path='runs/output_image.jpg', conf=0.25):
        """
        Tek bir görüntü üzerinde tespit
        """
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"❌ Görüntü okunamadı: {image_path}")
            return
        
        results = self.model(img, conf=conf)
        annotated = results[0].plot()
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_path), annotated)
        
        print(f"✅ Görüntü kaydedildi: {output_path}")
        
        # Tespit edilen nesneleri yazdır
        if len(results[0].boxes) > 0:
            print("\n🎯 Tespit edilen nesneler:")
            for box in results[0].boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy()
                print(f"  • {self.model.names[cls]}: {conf:.2f} @ [{xyxy[0]:.0f}, {xyxy[1]:.0f}, {xyxy[2]:.0f}, {xyxy[3]:.0f}]")
    
    def _get_color(self, track_id):
        """Track ID'ye göre renk üret"""
        np.random.seed(track_id)
        return tuple(map(int, np.random.randint(0, 255, 3)))
    
    def get_statistics(self):
        """Tracking istatistikleri"""
        print("\n📊 Tracking İstatistikleri:")
        print(f"  • Toplam takip edilen nesne: {len(self.track_history)}")
        for track_id, history in self.track_history.items():
            print(f"  • ID {track_id}: {len(history)} frame")

if __name__ == "__main__":
    # Eğitilmiş model ile test
    model_path = 'runs/train/visdrone_yolo/weights/best.pt'
    
    tracker = UAVTracker(model_path=model_path, tracker_config='bytetrack.yaml')
    
    # Video işleme
    # tracker.process_video(
    #     'data/test_video.mp4',
    #     output_path='runs/tracked_video.mp4',
    #     conf=0.3,
    #     show=True,
    #     save_txt=True
    # )
    
    # Görüntü işleme
    # tracker.process_image(
    #     'data/raw/VisDrone2019-DET-test-dev/VisDrone2019-DET-test-dev/images/0000006_00159_d_0000001.jpg',
    #     output_path='runs/test_detection.jpg',
    #     conf=0.3
    # )
    
    print("✅ Tracker hazır!")