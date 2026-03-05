"""
Video İşleme - Tam Versiyon
Her frame'i işler ve tracking ile birlikte video oluşturur
"""
from src.api.uav_mission_system import UAVMissionSystem
from pathlib import Path
import cv2
import time


def process_video_with_tracking(
    video_path: str,
    uav_altitude: float = 100.0,
    uav_gps: tuple = None,
    conf_threshold: float = 0.25,
    save_every_frame: bool = False
):
    """
    Video'yu tracking ile işle ve yeni video oluştur
    
    Args:
        video_path: Video dosya yolu
        uav_altitude: İHA yüksekliği (metre)
        uav_gps: İHA GPS koordinatları (lat, lon)
        conf_threshold: Confidence eşiği
        save_every_frame: Her frame'i kaydet (yavaş ama detaylı)
    """
    
    print("=" * 70)
    print("🎥 VİDEO İŞLEME - TAM VERSİYON")
    print("=" * 70)
    
    # Sistem oluştur
    system = UAVMissionSystem(conf_threshold=conf_threshold)
    
    # Video bilgisi
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"\n📹 Video Bilgisi:")
    print(f"   Toplam frame: {total_frames}")
    print(f"   FPS: {fps}")
    print(f"   Çözünürlük: {width}x{height}")
    print(f"   Süre: {total_frames/fps:.1f} saniye")
    
    # Çıktı video
    output_dir = Path(f'outputs/missions/{system.mission_id}')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_video_path = output_dir / f'tracked_{Path(video_path).name}'
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_video_path), fourcc, fps, (width, height))
    
    print(f"\n💾 Çıktı: {output_video_path}")
    print(f"\n🚀 İşleme başlıyor...")
    
    # Tracking için YOLO kullan
    from ultralytics import YOLO
    model = YOLO(system.model.model_path)
    
    # Tracking yap
    results = model.track(
        source=video_path,
        conf=conf_threshold,
        iou=0.5,
        tracker='bytetrack.yaml',
        device=system.device,
        stream=True,
        verbose=False
    )
    
    # İstatistikler
    frame_count = 0
    total_detections = 0
    all_track_ids = set()
    class_counts = {}
    start_time = time.time()
    
    # Her frame'i işle
    for result in results:
        frame_count += 1
        
        # Annotated frame al
        annotated = result.plot()
        
        # Detections
        if len(result.boxes) > 0:
            total_detections += len(result.boxes)
            
            # Track ID'ler
            if result.boxes.id is not None:
                track_ids = result.boxes.id.cpu().numpy().astype(int)
                all_track_ids.update(track_ids)
            
            # Sınıf sayımı
            classes = result.boxes.cls.cpu().numpy()
            for cls in classes:
                cls_name = system.class_names.get(int(cls), f'class_{int(cls)}')
                class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
        
        # Ek bilgiler ekle
        # Üst panel
        info_lines = [
            f"Frame: {frame_count}/{total_frames}",
            f"Hedef: {len(result.boxes) if len(result.boxes) > 0 else 0}",
            f"Takip: {len(all_track_ids)}",
            f"Yukseklik: {uav_altitude}m"
        ]
        
        y_offset = 30
        for line in info_lines:
            cv2.putText(
                annotated, line, (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
            )
            y_offset += 30
        
        # Progress bar
        progress = frame_count / total_frames
        bar_width = width - 40
        bar_height = 20
        bar_x = 20
        bar_y = height - 40
        
        # Arka plan
        cv2.rectangle(annotated, (bar_x, bar_y), 
                     (bar_x + bar_width, bar_y + bar_height), 
                     (50, 50, 50), -1)
        
        # Progress
        progress_width = int(bar_width * progress)
        cv2.rectangle(annotated, (bar_x, bar_y), 
                     (bar_x + progress_width, bar_y + bar_height), 
                     (0, 255, 0), -1)
        
        # Progress text
        progress_text = f"{progress*100:.1f}%"
        cv2.putText(annotated, progress_text, 
                   (bar_x + bar_width//2 - 30, bar_y + 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Video'ya yaz
        out.write(annotated)
        
        # Progress göster
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps_current = frame_count / elapsed
            eta = (total_frames - frame_count) / fps_current if fps_current > 0 else 0
            
            print(f"   Frame {frame_count}/{total_frames} | "
                  f"{len(all_track_ids)} takip | "
                  f"{fps_current:.1f} FPS | "
                  f"ETA: {eta:.0f}s")
    
    # Temizlik
    cap.release()
    out.release()
    
    # Sonuçlar
    processing_time = time.time() - start_time
    
    print("\n" + "=" * 70)
    print("✅ VİDEO İŞLEME TAMAMLANDI!")
    print("=" * 70)
    print(f"\n📊 İstatistikler:")
    print(f"   Toplam frame: {frame_count}")
    print(f"   Toplam tespit: {total_detections}")
    print(f"   Takip edilen hedef: {len(all_track_ids)}")
    print(f"   İşlem süresi: {processing_time:.1f}s")
    print(f"   İşlem hızı: {frame_count/processing_time:.1f} FPS")
    
    print(f"\n📋 Sınıf Dağılımı:")
    for cls, count in sorted(class_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {cls}: {count}")
    
    print(f"\n💾 Video kaydedildi: {output_video_path}")
    print(f"📁 Dosya boyutu: {output_video_path.stat().st_size / 1024 / 1024:.1f} MB")
    print("=" * 70)
    
    return {
        'output_video': str(output_video_path),
        'total_frames': frame_count,
        'total_detections': total_detections,
        'unique_tracks': len(all_track_ids),
        'processing_time': processing_time,
        'fps': frame_count / processing_time,
        'class_counts': class_counts
    }


def main():
    """Ana program"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║              VİDEO İŞLEME - TAM VERSİYON                    ║
    ║                                                              ║
    ║  • Her frame işlenir                                        ║
    ║  • ByteTrack ile tracking                                   ║
    ║  • Gerçek zamanlı bilgiler                                  ║
    ║  • Progress bar                                             ║
    ║  • İşlenmiş video çıktısı                                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Video yolu
    video_path = input("Video yolu: ").strip()
    if not Path(video_path).exists():
        print("❌ Video bulunamadı!")
        return
    
    # Parametreler
    print("\n📐 Parametreler:")
    altitude = float(input("  İHA yüksekliği (metre) [100]: ") or "100")
    conf = float(input("  Confidence threshold (0.1-0.9) [0.25]: ") or "0.25")
    
    use_gps = input("  GPS koordinatları girilsin mi? (e/h) [h]: ").strip().lower()
    uav_gps = None
    if use_gps == 'e':
        lat = float(input("    Latitude: "))
        lon = float(input("    Longitude: "))
        uav_gps = (lat, lon)
    
    # İşle
    result = process_video_with_tracking(
        video_path=video_path,
        uav_altitude=altitude,
        uav_gps=uav_gps,
        conf_threshold=conf
    )
    
    print("\n✅ İşlem tamamlandı!")
    print(f"📹 Video'yu oynatmak için: {result['output_video']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 İşlem iptal edildi (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()
