"""
BAYKAR İHA Görev Sistemi
Gerçek İHA senaryoları için gelişmiş özellikler:
- GPS koordinat dönüşümü
- Mesafe ve yükseklik hesaplama
- Hedef kilitleme ve takip
- Görev raporu
"""
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import time
from typing import List, Dict, Tuple, Optional
import json
from datetime import datetime
import math


class UAVMissionSystem:
    """İHA Görev Sistemi - Gerçek senaryo özellikleri"""
    
    def __init__(
        self, 
        model_path: str = 'runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt',
        conf_threshold: float = 0.25,
        device: str = 'auto'
    ):
        """
        Args:
            model_path: Model dosya yolu
            conf_threshold: Confidence eşiği
            device: 'auto', '0' (GPU), veya 'cpu'
        """
        print("🚁 BAYKAR İHA GÖREV SİSTEMİ")
        print("=" * 70)
        
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        
        # Device ayarla
        if device == 'auto':
            import torch
            self.device = '0' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
        
        # Sınıf isimleri (VisDrone veri seti - doğru mapping)
        self.class_names = {
            0: 'pedestrian', 1: 'people', 2: 'bicycle',
            3: 'car', 4: 'van', 5: 'truck', 6: 'tricycle',
            7: 'awning-tricycle', 8: 'bus', 9: 'motor'
        }
        
        # Görev bilgileri
        self.mission_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.locked_targets = {}  # Kilitlenmiş hedefler
        
        print(f"✅ Sistem hazır")
        print(f"📦 Model: {Path(model_path).name}")
        print(f"💻 Device: {self.device}")
        print(f"🎯 Görev ID: {self.mission_id}")
        print("=" * 70)
    
    def detect_with_location(
        self,
        image_path: str,
        uav_altitude: float = 100.0,  # İHA yüksekliği (metre)
        uav_gps: Tuple[float, float] = None,  # İHA GPS (lat, lon)
        camera_fov: float = 60.0,  # Kamera görüş açısı (derece)
        camera_angle: float = 90.0,  # Kamera açısı (90=dik aşağı)
        save_result: bool = True
    ) -> Dict:
        """
        Konum bilgisi ile tespit yap
        
        Args:
            image_path: Görüntü yolu
            uav_altitude: İHA yüksekliği (metre)
            uav_gps: İHA GPS koordinatları (latitude, longitude)
            camera_fov: Kamera görüş açısı (derece)
            camera_angle: Kamera açısı (90=dik aşağı, 0=yatay)
            save_result: Sonucu kaydet
        
        Returns:
            Tespit sonuçları + konum bilgileri
        """
        print(f"\n🎯 Görev: {image_path}")
        print(f"   Yükseklik: {uav_altitude}m")
        if uav_gps:
            print(f"   GPS: {uav_gps[0]:.6f}, {uav_gps[1]:.6f}")
        
        start_time = time.time()
        
        # Tespit yap
        results = self.model.predict(
            source=image_path,
            conf=self.conf_threshold,
            iou=0.5,
            max_det=1000,
            device=self.device,
            verbose=False
        )
        
        result = results[0]
        img_height, img_width = result.orig_shape
        
        # Zemin kapsama alanı hesapla
        ground_coverage = self._calculate_ground_coverage(
            uav_altitude, camera_fov, camera_angle, img_width, img_height
        )
        
        # Tespitleri işle
        detections = []
        if len(result.boxes) > 0:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()
            
            for idx, (box, conf, cls) in enumerate(zip(boxes, confidences, classes)):
                x1, y1, x2, y2 = box
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                
                # Piksel koordinatlarını gerçek dünya koordinatlarına dönüştür
                real_world_pos = self._pixel_to_world(
                    cx, cy, img_width, img_height, ground_coverage
                )
                
                # GPS koordinatı hesapla (eğer İHA GPS'i varsa)
                target_gps = None
                if uav_gps:
                    target_gps = self._calculate_target_gps(
                        uav_gps, real_world_pos, uav_altitude
                    )
                
                # Mesafe hesapla (İHA'dan hedefe)
                distance = math.sqrt(
                    real_world_pos[0]**2 + 
                    real_world_pos[1]**2 + 
                    uav_altitude**2
                )
                
                detection = {
                    'id': idx + 1,
                    'class': self.class_names.get(int(cls), f'class_{int(cls)}'),
                    'class_id': int(cls),
                    'confidence': float(conf),
                    'bbox': [float(x1), float(y1), float(x2), float(y2)],
                    'center_pixel': [float(cx), float(cy)],
                    'center_world': real_world_pos,  # (x, y) metre cinsinden
                    'distance': float(distance),  # İHA'dan mesafe (metre)
                    'gps': target_gps,  # GPS koordinatları (lat, lon)
                    'size_pixel': [float(x2-x1), float(y2-y1)],
                    'size_world': self._estimate_real_size(
                        x2-x1, y2-y1, img_width, img_height, 
                        ground_coverage, uav_altitude
                    )
                }
                
                detections.append(detection)
        
        processing_time = time.time() - start_time
        
        # Sonuç objesi
        output = {
            'mission_id': self.mission_id,
            'timestamp': datetime.now().isoformat(),
            'uav_info': {
                'altitude': uav_altitude,
                'gps': uav_gps,
                'camera_fov': camera_fov,
                'camera_angle': camera_angle
            },
            'ground_coverage': ground_coverage,
            'detections': detections,
            'count': len(detections),
            'processing_time': processing_time,
            'image_size': [img_width, img_height]
        }
        
        # Kaydet
        if save_result:
            output_dir = Path('outputs/missions') / self.mission_id
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Görüntüyü çiz (gelişmiş)
            annotated = self._draw_advanced_annotations(
                result, detections, uav_altitude, ground_coverage
            )
            
            output_path = output_dir / Path(image_path).name
            cv2.imwrite(str(output_path), annotated)
            
            # JSON kaydet
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            output['saved_image'] = str(output_path)
            output['saved_json'] = str(json_path)
        
        # Özet göster
        print(f"\n📊 Sonuç:")
        print(f"   ✅ {len(detections)} hedef tespit edildi")
        print(f"   ⏱️  İşlem süresi: {processing_time:.3f}s")
        print(f"   📏 Zemin kapsama: {ground_coverage['width']:.1f}m x {ground_coverage['height']:.1f}m")
        
        return output
    
    def lock_target(
        self,
        detection: Dict,
        priority: str = 'normal'
    ) -> Dict:
        """
        Hedefi kilitle ve takip et
        
        Args:
            detection: Tespit objesi
            priority: Öncelik ('low', 'normal', 'high', 'critical')
        
        Returns:
            Kilitlenmiş hedef bilgisi
        """
        target_id = f"TGT_{len(self.locked_targets) + 1:03d}"
        
        locked_target = {
            'target_id': target_id,
            'lock_time': datetime.now().isoformat(),
            'priority': priority,
            'detection': detection,
            'status': 'locked',
            'track_history': []
        }
        
        self.locked_targets[target_id] = locked_target
        
        print(f"\n🎯 HEDEF KİLİTLENDİ")
        print(f"   ID: {target_id}")
        print(f"   Sınıf: {detection['class']}")
        print(f"   Mesafe: {detection['distance']:.1f}m")
        if detection['gps']:
            print(f"   GPS: {detection['gps'][0]:.6f}, {detection['gps'][1]:.6f}")
        print(f"   Öncelik: {priority.upper()}")
        
        return locked_target
    
    def generate_mission_report(
        self,
        detections_list: List[Dict],
        save_path: str = None
    ) -> Dict:
        """
        Görev raporu oluştur
        
        Args:
            detections_list: Tespit sonuçları listesi
            save_path: Rapor kayıt yolu
        
        Returns:
            Görev raporu
        """
        print("\n📋 GÖREV RAPORU OLUŞTURULUYOR...")
        
        # İstatistikler
        total_detections = sum(d['count'] for d in detections_list)
        total_frames = len(detections_list)
        
        # Sınıf bazında sayım
        class_counts = {}
        all_distances = []
        
        for detection_result in detections_list:
            for det in detection_result['detections']:
                cls = det['class']
                class_counts[cls] = class_counts.get(cls, 0) + 1
                all_distances.append(det['distance'])
        
        # Rapor
        report = {
            'mission_id': self.mission_id,
            'report_time': datetime.now().isoformat(),
            'summary': {
                'total_frames': total_frames,
                'total_detections': total_detections,
                'avg_detections_per_frame': total_detections / total_frames if total_frames > 0 else 0,
                'unique_classes': len(class_counts),
                'locked_targets': len(self.locked_targets)
            },
            'class_distribution': class_counts,
            'distance_stats': {
                'min': float(min(all_distances)) if all_distances else 0,
                'max': float(max(all_distances)) if all_distances else 0,
                'avg': float(np.mean(all_distances)) if all_distances else 0,
                'median': float(np.median(all_distances)) if all_distances else 0
            },
            'locked_targets': list(self.locked_targets.values()),
            'frames': detections_list
        }
        
        # Kaydet
        if save_path is None:
            save_path = f'outputs/missions/{self.mission_id}/mission_report.json'
        
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Özet göster
        print("\n" + "=" * 70)
        print("📊 GÖREV RAPORU")
        print("=" * 70)
        print(f"Görev ID: {self.mission_id}")
        print(f"Toplam Frame: {total_frames}")
        print(f"Toplam Tespit: {total_detections}")
        print(f"Kilitli Hedef: {len(self.locked_targets)}")
        print(f"\nSınıf Dağılımı:")
        for cls, count in sorted(class_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {cls}: {count}")
        print(f"\nMesafe İstatistikleri:")
        print(f"  • Min: {report['distance_stats']['min']:.1f}m")
        print(f"  • Max: {report['distance_stats']['max']:.1f}m")
        print(f"  • Ortalama: {report['distance_stats']['avg']:.1f}m")
        print(f"\n💾 Rapor kaydedildi: {save_path}")
        print("=" * 70)
        
        return report
    
    def _calculate_ground_coverage(
        self,
        altitude: float,
        fov: float,
        angle: float,
        img_width: int,
        img_height: int
    ) -> Dict:
        """Zemin kapsama alanını hesapla"""
        
        # FOV'u radyana çevir
        fov_rad = math.radians(fov)
        angle_rad = math.radians(angle)
        
        # Zemin mesafesi
        ground_distance = altitude / math.tan(angle_rad) if angle != 90 else 0
        
        # Kapsama genişliği ve yüksekliği
        if angle == 90:  # Dik aşağı
            width = 2 * altitude * math.tan(fov_rad / 2)
            height = width * (img_height / img_width)
        else:
            # Eğik açı için yaklaşık hesaplama
            width = 2 * altitude * math.tan(fov_rad / 2)
            height = width * (img_height / img_width) / math.sin(angle_rad)
        
        return {
            'width': width,
            'height': height,
            'area': width * height,
            'center_offset': ground_distance
        }
    
    def _pixel_to_world(
        self,
        px: float,
        py: float,
        img_width: int,
        img_height: int,
        ground_coverage: Dict
    ) -> Tuple[float, float]:
        """Piksel koordinatlarını gerçek dünya koordinatlarına dönüştür"""
        
        # Normalize et (0-1)
        nx = px / img_width
        ny = py / img_height
        
        # Merkeze göre pozisyon (-0.5 ile 0.5 arası)
        rel_x = nx - 0.5
        rel_y = ny - 0.5
        
        # Gerçek dünya koordinatları (metre)
        world_x = rel_x * ground_coverage['width']
        world_y = rel_y * ground_coverage['height']
        
        return (world_x, world_y)
    
    def _calculate_target_gps(
        self,
        uav_gps: Tuple[float, float],
        target_offset: Tuple[float, float],
        altitude: float
    ) -> Tuple[float, float]:
        """Hedefin GPS koordinatlarını hesapla"""
        
        # Basitleştirilmiş GPS hesaplama
        # 1 derece latitude ≈ 111km
        # 1 derece longitude ≈ 111km * cos(latitude)
        
        lat, lon = uav_gps
        offset_x, offset_y = target_offset
        
        # Metre cinsinden offset'i dereceye çevir
        lat_offset = offset_y / 111000  # Kuzey-Güney
        lon_offset = offset_x / (111000 * math.cos(math.radians(lat)))  # Doğu-Batı
        
        target_lat = lat + lat_offset
        target_lon = lon + lon_offset
        
        return (target_lat, target_lon)
    
    def _estimate_real_size(
        self,
        width_px: float,
        height_px: float,
        img_width: int,
        img_height: int,
        ground_coverage: Dict,
        altitude: float
    ) -> Tuple[float, float]:
        """Nesnenin gerçek boyutunu tahmin et"""
        
        # Piksel başına metre
        meters_per_pixel_x = ground_coverage['width'] / img_width
        meters_per_pixel_y = ground_coverage['height'] / img_height
        
        # Gerçek boyut
        real_width = width_px * meters_per_pixel_x
        real_height = height_px * meters_per_pixel_y
        
        return (real_width, real_height)
    
    def _draw_advanced_annotations(
        self,
        result,
        detections: List[Dict],
        altitude: float,
        ground_coverage: Dict
    ) -> np.ndarray:
        """Gelişmiş annotasyon çiz"""
        
        # Temel çizim
        annotated = result.plot()
        
        # Her tespit için ek bilgiler
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            cx, cy = det['center_pixel']
            
            # Mesafe bilgisi
            distance_text = f"{det['distance']:.1f}m"
            cv2.putText(
                annotated,
                distance_text,
                (int(x1), int(y1) - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                2
            )
            
            # Merkez noktası
            cv2.circle(annotated, (int(cx), int(cy)), 5, (0, 255, 0), -1)
            
            # GPS varsa göster
            if det['gps']:
                gps_text = f"{det['gps'][0]:.5f},{det['gps'][1]:.5f}"
                cv2.putText(
                    annotated,
                    gps_text,
                    (int(x1), int(y2) + 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (255, 255, 0),
                    1
                )
        
        # Üst bilgi paneli
        info_text = [
            f"Altitude: {altitude:.1f}m",
            f"Coverage: {ground_coverage['width']:.1f}x{ground_coverage['height']:.1f}m",
            f"Targets: {len(detections)}"
        ]
        
        y_offset = 30
        for text in info_text:
            cv2.putText(
                annotated,
                text,
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )
            y_offset += 25
        
        return annotated


# Kullanım örneği
if __name__ == "__main__":
    # Sistem oluştur
    system = UAVMissionSystem()
    
    print("\n" + "=" * 70)
    print("KULLANIM ÖRNEĞİ")
    print("=" * 70)
    
    # Örnek: Konum bilgisi ile tespit
    result = system.detect_with_location(
        image_path='test_image.jpg',
        uav_altitude=100.0,  # 100 metre yükseklik
        uav_gps=(39.9334, 32.8597),  # Ankara koordinatları (örnek)
        camera_fov=60.0,
        camera_angle=90.0,
        save_result=True
    )
    
    # Hedef kilitle
    if result['detections']:
        # İlk aracı kilitle
        for det in result['detections']:
            if det['class'] == 'car':
                system.lock_target(det, priority='high')
                break
    
    print("\n✅ Örnek tamamlandı!")
