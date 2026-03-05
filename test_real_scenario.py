"""
Gerçek Senaryo Test Scripti
İHA görüntülerini gerçek koşullarda test et
"""
from src.api.uav_mission_system import UAVMissionSystem
from pathlib import Path
import sys
import time


def test_scenario_1_single_image():
    """Senaryo 1: Tek görüntü - Konum bilgisi ile"""
    
    print("\n" + "="*70)
    print("SENARYO 1: TEK FOTOĞRAF ANALİZİ")
    print("="*70)
    print("\n📸 Bu senaryo TEK FOTOĞRAF üzerinde çalışır")
    print("   GPS koordinatları ve mesafe bilgisi ile tespit yapar\n")
    
    system = UAVMissionSystem(conf_threshold=0.25)
    
    # Test görüntüsü
    image_path = input("Fotoğraf yolu (Enter=test fotoğrafı): ").strip()
    if not image_path:
        # Test veri setinden bir görüntü
        test_dir = Path('data/raw/VisDrone2019-DET-test-dev/VisDrone2019-DET-test-dev/images')
        if test_dir.exists():
            image_path = str(list(test_dir.glob('*.jpg'))[0])
            print(f"✅ Test fotoğrafı kullanılıyor: {Path(image_path).name}")
        else:
            print("❌ Test fotoğrafı bulunamadı!")
            return
    
    # İHA parametreleri
    print("\n📐 İHA Parametreleri:")
    altitude = float(input("  Yükseklik (metre) [100]: ") or "100")
    
    use_gps = input("  GPS koordinatları girilsin mi? (e/h) [h]: ").strip().lower()
    uav_gps = None
    if use_gps == 'e':
        lat = float(input("    Latitude: "))
        lon = float(input("    Longitude: "))
        uav_gps = (lat, lon)
    
    # Tespit yap
    result = system.detect_with_location(
        image_path=image_path,
        uav_altitude=altitude,
        uav_gps=uav_gps,
        camera_fov=60.0,
        camera_angle=90.0,
        save_result=True
    )
    
    # Sonuçları göster
    print("\n" + "="*70)
    print("📊 DETAYLI SONUÇLAR")
    print("="*70)
    
    if result['detections']:
        print(f"\n✅ {len(result['detections'])} hedef tespit edildi:\n")
        
        for i, det in enumerate(result['detections'][:10], 1):  # İlk 10 hedef
            print(f"{i}. {det['class'].upper()}")
            print(f"   • Güven: {det['confidence']:.2%}")
            print(f"   • Mesafe: {det['distance']:.1f}m")
            print(f"   • Konum (dünya): ({det['center_world'][0]:.1f}m, {det['center_world'][1]:.1f}m)")
            if det['gps']:
                print(f"   • GPS: {det['gps'][0]:.6f}, {det['gps'][1]:.6f}")
            print(f"   • Boyut: {det['size_world'][0]:.1f}m x {det['size_world'][1]:.1f}m")
            print()
        
        if len(result['detections']) > 10:
            print(f"   ... ve {len(result['detections']) - 10} hedef daha")
    else:
        print("⚠️  Hiç hedef tespit edilemedi")
    
    # Hedef kilitleme
    if result['detections']:
        lock = input("\n🎯 Hedef kilitlensin mi? (e/h) [h]: ").strip().lower()
        if lock == 'e':
            # Öncelikli hedefleri göster
            print("\nKilitlenebilir hedefler:")
            for i, det in enumerate(result['detections'][:5], 1):
                print(f"{i}. {det['class']} - {det['distance']:.1f}m - Güven: {det['confidence']:.2%}")
            
            choice = int(input("\nHedef seç (1-5): ") or "1") - 1
            if 0 <= choice < len(result['detections']):
                priority = input("Öncelik (low/normal/high/critical) [normal]: ") or "normal"
                system.lock_target(result['detections'][choice], priority=priority)
    
    print(f"\n💾 Sonuçlar kaydedildi: {result.get('saved_image', 'N/A')}")


def test_scenario_2_video_mission():
    """Senaryo 2: Video görev analizi"""
    
    print("\n" + "="*70)
    print("SENARYO 2: VİDEO GÖREV ANALİZİ")
    print("="*70)
    print("\n🎥 Bu senaryo VİDEO dosyası üzerinde çalışır")
    print("   Her frame işlenir ve tracking ile video oluşturur\n")
    
    system = UAVMissionSystem(conf_threshold=0.25)
    
    # Video yolu
    video_path = input("Video yolu (.mp4, .avi, vb.): ").strip()
    if not Path(video_path).exists():
        print("❌ Video bulunamadı!")
        return
    
    # İHA parametreleri
    altitude = float(input("İHA yüksekliği (metre) [100]: ") or "100")
    
    use_gps = input("GPS koordinatları girilsin mi? (e/h) [h]: ").strip().lower()
    uav_gps = None
    if use_gps == 'e':
        lat = float(input("  Latitude: "))
        lon = float(input("  Longitude: "))
        uav_gps = (lat, lon)
    
    # Video bilgisi
    import cv2
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    
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
    
    # Tracking için YOLO kullan (aynı model)
    from ultralytics import YOLO
    from src.utils.uav_hud import UAV_HUD
    
    model_path = 'runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt'
    model = YOLO(model_path)
    
    # HUD oluştur
    hud = UAV_HUD(width, height)
    
    print(f"📦 Model: {model_path}")
    print(f"🎨 İHA HUD aktif")
    
    # Tracking yap (daha yüksek confidence)
    results = model.track(
        source=video_path,
        conf=0.25,  # Confidence threshold
        iou=0.5,    # NMS IoU threshold
        tracker='bytetrack.yaml',
        device=system.device,
        stream=True,
        verbose=False,
        classes=None,  # Tüm sınıflar
        agnostic_nms=False,  # Sınıf bazlı NMS
        max_det=300  # Maksimum tespit sayısı
    )
    
    # İstatistikler
    frame_count = 0
    total_detections = 0
    all_track_ids = set()
    class_counts = {}
    detections_list = []
    start_time = time.time()
    
    # Her frame'i işle
    for result in results:
        frame_count += 1
        
        # Detections
        detection_count = 0
        if len(result.boxes) > 0:
            total_detections += len(result.boxes)
            detection_count = len(result.boxes)
            
            # Track ID'ler
            if result.boxes.id is not None:
                track_ids = result.boxes.id.cpu().numpy().astype(int)
                all_track_ids.update(track_ids)
            
            # Sınıf sayımı
            classes = result.boxes.cls.cpu().numpy()
            for cls in classes:
                cls_name = system.class_names.get(int(cls), f'class_{int(cls)}')
                class_counts[cls_name] = class_counts.get(cls_name, 0) + 1
        
        # Annotated frame al
        annotated = result.plot()
        
        # İHA HUD ekle
        annotated = hud.draw_full_hud(
            annotated,
            altitude=altitude,
            speed=5.0 + (frame_count % 100) / 20,  # Simüle edilmiş hız
            heading=(frame_count * 0.5) % 360,  # Simüle edilmiş yön
            gps=uav_gps,
            battery=max(20, 100 - frame_count // 50),  # Simüle edilmiş batarya
            signal=95,
            target_count=detection_count,
            tracked_count=len(all_track_ids),
            frame_num=frame_count,
            total_frames=total_frames,
            mission_id=system.mission_id[-8:],  # Son 8 karakter
            pitch=0.0
        )
        
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


def test_scenario_3_batch_analysis():
    """Senaryo 3: Toplu görüntü analizi"""
    
    print("\n" + "="*70)
    print("SENARYO 3: TOPLU FOTOĞRAF ANALİZİ")
    print("="*70)
    print("\n📁 Bu senaryo KLASÖR içindeki tüm fotoğrafları işler")
    print("   Birden fazla fotoğrafı toplu olarak analiz eder\n")
    
    system = UAVMissionSystem(conf_threshold=0.25)
    
    # Klasör yolu
    folder_path = input("Klasör yolu (Enter=test klasörü): ").strip()
    if not folder_path:
        folder_path = 'data/raw/VisDrone2019-DET-test-dev/VisDrone2019-DET-test-dev/images'
        print(f"✅ Test klasörü kullanılıyor: {folder_path}")
    
    folder = Path(folder_path)
    if not folder.exists():
        print("❌ Klasör bulunamadı!")
        return
    
    # Görüntüleri bul
    image_files = list(folder.glob('*.jpg')) + list(folder.glob('*.png'))
    
    if not image_files:
        print("❌ Görüntü bulunamadı!")
        return
    
    # Kaç görüntü işlensin
    max_images = int(input(f"\nKaç görüntü işlensin? (1-{len(image_files)}) [10]: ") or "10")
    image_files = image_files[:max_images]
    
    # İHA parametreleri
    altitude = float(input("İHA yüksekliği (metre) [100]: ") or "100")
    
    print(f"\n📸 {len(image_files)} görüntü işleniyor...")
    
    detections_list = []
    
    for i, img_path in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] {img_path.name}")
        
        result = system.detect_with_location(
            image_path=str(img_path),
            uav_altitude=altitude,
            uav_gps=None,
            camera_fov=60.0,
            camera_angle=90.0,
            save_result=True
        )
        
        detections_list.append(result)
    
    # Görev raporu
    if detections_list:
        report = system.generate_mission_report(detections_list)
        print(f"\n✅ Toplu analiz tamamlandı!")


def test_scenario_4_target_tracking():
    """Senaryo 4: Hedef takip simülasyonu"""
    
    print("\n" + "="*70)
    print("SENARYO 4: HEDEF TAKİP SİMÜLASYONU")
    print("="*70)
    print("\n📸 Bu senaryo TEK FOTOĞRAF üzerinde çalışır")
    print("   Fotoğraftaki hedefleri tespit edip kilitler\n")
    
    system = UAVMissionSystem(conf_threshold=0.2)  # Daha hassas
    
    # Görüntü
    image_path = input("Fotoğraf yolu (Enter=test fotoğrafı): ").strip()
    if not image_path:
        # Test veri setinden bir görüntü
        test_dir = Path('data/raw/VisDrone2019-DET-test-dev/VisDrone2019-DET-test-dev/images')
        if test_dir.exists():
            image_path = str(list(test_dir.glob('*.jpg'))[0])
            print(f"✅ Test fotoğrafı kullanılıyor: {Path(image_path).name}")
        else:
            print("❌ Test fotoğrafı bulunamadı!")
            return
    
    if not Path(image_path).exists():
        print("❌ Fotoğraf bulunamadı!")
        return
    
    # Tespit yap
    result = system.detect_with_location(
        image_path=image_path,
        uav_altitude=100.0,
        uav_gps=(39.9334, 32.8597),  # Örnek GPS
        camera_fov=60.0,
        camera_angle=90.0,
        save_result=True
    )
    
    if not result['detections']:
        print("⚠️  Hedef bulunamadı!")
        return
    
    # Hedef türü seç
    print("\n🎯 Hedef türü seçin:")
    print("1. Araçlar (car, truck, van, bus)")
    print("2. İnsanlar (pedestrian, people)")
    print("3. Tümü")
    
    choice = input("\nSeçim (1-3) [1]: ") or "1"
    
    target_classes = {
        '1': ['car', 'truck', 'van', 'bus'],
        '2': ['pedestrian', 'people'],
        '3': None  # Tümü
    }
    
    selected_classes = target_classes.get(choice)
    
    # Hedefleri filtrele ve kilitle
    locked_count = 0
    for det in result['detections']:
        if selected_classes is None or det['class'] in selected_classes:
            # Mesafeye göre öncelik belirle
            if det['distance'] < 50:
                priority = 'critical'
            elif det['distance'] < 100:
                priority = 'high'
            elif det['distance'] < 200:
                priority = 'normal'
            else:
                priority = 'low'
            
            system.lock_target(det, priority=priority)
            locked_count += 1
    
    print(f"\n✅ {locked_count} hedef kilitlendi!")
    
    # Rapor oluştur
    report = system.generate_mission_report([result])


def main():
    """Ana menü"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║        BAYKAR İHA GÖREV SİSTEMİ - GERÇEK SENARYO TEST      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("\nTEST SENARYOLARI:")
    print("=" * 70)
    print("1. Tek Fotoğraf Analizi")
    print("   → GPS + Mesafe + Konum bilgisi")
    print("   → Tek bir fotoğraf üzerinde çalışır")
    print()
    print("2. Video Görev Analizi")
    print("   → Frame bazlı analiz + Görev raporu")
    print("   → Video dosyası (.mp4, .avi) gerekir")
    print()
    print("3. Toplu Fotoğraf Analizi")
    print("   → Klasördeki tüm fotoğrafları işler")
    print("   → Birden fazla fotoğraf için")
    print()
    print("4. Hedef Takip Simülasyonu")
    print("   → Hedef kilitleme ve önceliklendirme")
    print("   → Tek bir fotoğraf üzerinde çalışır")
    print()
    print("5. Çıkış")
    print("=" * 70)
    
    while True:
        choice = input("\nSeçim (1-5): ").strip()
        
        if choice == '1':
            test_scenario_1_single_image()
        elif choice == '2':
            test_scenario_2_video_mission()
        elif choice == '3':
            test_scenario_3_batch_analysis()
        elif choice == '4':
            test_scenario_4_target_tracking()
        elif choice == '5':
            print("\n👋 Çıkılıyor...")
            break
        else:
            print("❌ Geçersiz seçim!")
        
        input("\nDevam etmek için Enter'a basın...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program sonlandırıldı (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()
