"""
BAYKAR İHA Tespit ve Takip API
Production kullanımı için hazır
"""
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import time
from typing import List, Dict, Tuple, Optional
import json


class UAVDetectionSystem:
    """İHA görüntü işleme sistemi - Production ready"""
    
    def __init__(
        self, 
        model_path: str = 'runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt',
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.5,
        device: str = 'auto'
    ):
        """
        Args:
            model_path: Model dosya yolu
            conf_threshold: Confidence eşiği (0.1-0.9)
            iou_threshold: NMS IoU eşiği
            device: 'auto', '0' (GPU), veya 'cpu'
        """
        print("🚁 BAYKAR İHA Tespit Sistemi Başlatılıyor...")
        
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        
        # Model yükle
        self.model = YOLO(model_path)
        
        # Device ayarla
        if device == 'auto':
            import torch
            self.device = '0' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
        
        # Sınıf isimleri (VisDrone veri seti - doğru mapping)
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
        
        print(f"✅ Model yüklendi: {Path(model_path).name}")
        print(f"💻 Device: {self.device}")
        print(f"🎯 Confidence: {conf_threshold}")
        print("=" * 60)
    
    def detect_image(
        self, 
        image_path: str,
        save_result: bool = True,
        output_dir: str = 'outputs'
    ) -> Dict:
        """
        Tek görüntüde tespit yap
        
        Returns:
            {
                'detections': [
                    {
                        'class': 'car',
                        'confidence': 0.85,
                        'bbox': [x1, y1, x2, y2],
                        'center': [cx, cy]
                    },
                    ...
                ],
                'count': 10,
                'processing_time': 0.05,
                'image_size': [1920, 1080]
            }
        """
        start_time = time.time()
        
        # Tespit yap
        results = self.model.predict(
            source=image_path,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            max_det=1000,
            device=self.device,
            verbose=False
        )
        
        result = results[0]
        
        # Sonuçları parse et
        detections = []
        if len(result.boxes) > 0:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()
            
            for box, conf, cls in zip(boxes, confidences, classes):
                x1, y1, x2, y2 = box
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                
                detections.append({
                    'class': self.class_names.get(int(cls), f'class_{int(cls)}'),
                    'class_id': int(cls),
                    'confidence': float(conf),
                    'bbox': [float(x1), float(y1), float(x2), float(y2)],
                    'center': [float(cx), float(cy)],
                    'width': float(x2 - x1),
                    'height': float(y2 - y1)
                })
        
        processing_time = time.time() - start_time
        
        # Sonuç objesi
        output = {
            'detections': detections,
            'count': len(detections),
            'processing_time': processing_time,
            'image_size': [result.orig_shape[1], result.orig_shape[0]],
            'model': Path(self.model_path).name,
            'confidence_threshold': self.conf_threshold
        }
        
        # Kaydet
        if save_result:
            output_path = Path(output_dir) / Path(image_path).name
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Görüntüyü çiz
            annotated = result.plot()
            cv2.imwrite(str(output_path), annotated)
            
            # JSON kaydet
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            output['saved_image'] = str(output_path)
            output['saved_json'] = str(json_path)
        
        return output
    
    def track_video(
        self,
        video_path: str,
        save_result: bool = True,
        output_dir: str = 'outputs',
        show_progress: bool = True
    ) -> Dict:
        """
        Video üzerinde tespit + tracking
        
        Returns:
            {
                'total_frames': 1000,
                'total_detections': 15000,
                'unique_tracks': 150,
                'processing_time': 45.2,
                'fps': 22.1,
                'output_video': 'outputs/tracked_video.mp4'
            }
        """
        start_time = time.time()
        
        # Video bilgisi
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        
        # Tracking yap
        results = self.model.track(
            source=video_path,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            tracker='bytetrack.yaml',
            device=self.device,
            stream=True,
            verbose=False
        )
        
        # Video writer
        if save_result:
            output_path = Path(output_dir) / f"tracked_{Path(video_path).name}"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        # İstatistikler
        frame_count = 0
        total_detections = 0
        all_track_ids = set()
        
        # Frame işle
        for result in results:
            frame_count += 1
            
            # Detections
            if len(result.boxes) > 0:
                total_detections += len(result.boxes)
                
                # Track ID'ler
                if result.boxes.id is not None:
                    track_ids = result.boxes.id.cpu().numpy().astype(int)
                    all_track_ids.update(track_ids)
            
            # Progress
            if show_progress and frame_count % 30 == 0:
                elapsed = time.time() - start_time
                current_fps = frame_count / elapsed
                print(f"   Frame {frame_count}/{total_frames} | "
                      f"{len(all_track_ids)} takip | "
                      f"{current_fps:.1f} FPS")
            
            # Kaydet
            if save_result:
                annotated = result.plot()
                out.write(annotated)
        
        if save_result:
            out.release()
        
        processing_time = time.time() - start_time
        
        # Sonuç
        output = {
            'total_frames': frame_count,
            'total_detections': total_detections,
            'unique_tracks': len(all_track_ids),
            'processing_time': processing_time,
            'fps': frame_count / processing_time,
            'video_info': {
                'width': width,
                'height': height,
                'original_fps': fps
            },
            'model': Path(self.model_path).name,
            'confidence_threshold': self.conf_threshold
        }
        
        if save_result:
            output['output_video'] = str(output_path)
            
            # JSON kaydet
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            output['saved_json'] = str(json_path)
        
        return output
    
    def detect_realtime(
        self,
        source: int = 0,
        window_name: str = "BAYKAR İHA Tespit"
    ):
        """
        Gerçek zamanlı kamera/stream'den tespit
        
        Args:
            source: Kamera ID (0, 1, ...) veya RTSP URL
            window_name: Pencere ismi
        """
        print(f"📹 Gerçek zamanlı tespit başlatılıyor...")
        print(f"   Kaynak: {source}")
        print(f"   Çıkmak için 'q' tuşuna basın")
        
        cap = cv2.VideoCapture(source)
        
        if not cap.isOpened():
            print("❌ Kamera/stream açılamadı!")
            return
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Tespit yap
            results = self.model.predict(
                source=frame,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                device=self.device,
                verbose=False
            )
            
            # Çiz
            annotated = results[0].plot()
            
            # FPS göster
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            cv2.putText(
                annotated, 
                f"FPS: {fps:.1f}", 
                (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (0, 255, 0), 
                2
            )
            
            # Göster
            cv2.imshow(window_name, annotated)
            
            # Çıkış
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n✅ Gerçek zamanlı tespit sonlandırıldı")
        print(f"   Toplam frame: {frame_count}")
        print(f"   Ortalama FPS: {fps:.1f}")
    
    def get_target_info(self, detections: List[Dict], target_class: str = 'car') -> List[Dict]:
        """
        Belirli bir sınıftaki hedeflerin bilgilerini al
        
        Args:
            detections: detect_image() veya track_video() sonucu
            target_class: Hedef sınıf ('car', 'truck', vb.)
        
        Returns:
            Hedef bilgileri listesi
        """
        targets = []
        for det in detections:
            if det['class'] == target_class:
                targets.append({
                    'id': len(targets) + 1,
                    'class': det['class'],
                    'confidence': det['confidence'],
                    'position': det['center'],
                    'bbox': det['bbox'],
                    'size': [det['width'], det['height']]
                })
        
        return targets


# Kullanım örnekleri
if __name__ == "__main__":
    # Sistem oluştur
    system = UAVDetectionSystem(
        conf_threshold=0.25,
        device='auto'
    )
    
    print("\n" + "=" * 60)
    print("KULLANIM ÖRNEKLERİ")
    print("=" * 60)
    
    # Örnek 1: Görüntü tespiti
    print("\n1️⃣ Görüntü Tespiti:")
    print("   result = system.detect_image('image.jpg')")
    print("   print(f\"Tespit: {result['count']} nesne\")")
    
    # Örnek 2: Video tracking
    print("\n2️⃣ Video Tracking:")
    print("   result = system.track_video('video.mp4')")
    print("   print(f\"Takip: {result['unique_tracks']} hedef\")")
    
    # Örnek 3: Gerçek zamanlı
    print("\n3️⃣ Gerçek Zamanlı:")
    print("   system.detect_realtime(source=0)  # Webcam")
    print("   system.detect_realtime(source='rtsp://...')  # RTSP stream")
    
    # Örnek 4: Hedef bilgisi
    print("\n4️⃣ Hedef Bilgisi:")
    print("   result = system.detect_image('image.jpg')")
    print("   cars = system.get_target_info(result['detections'], 'car')")
    print("   print(f\"Araç sayısı: {len(cars)}\")")
    
    print("\n" + "=" * 60)
