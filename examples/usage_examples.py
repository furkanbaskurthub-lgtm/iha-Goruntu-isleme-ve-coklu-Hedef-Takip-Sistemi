"""
BAYKAR İHA Sistemi - Kullanım Örnekleri
Kendi kodunuzda nasıl kullanacağınızı gösterir
"""
from src.api.detection_api import UAVDetectionSystem


# ============================================================
# ÖRNEK 1: Basit Görüntü Tespiti
# ============================================================
def example_1_simple_detection():
    """En basit kullanım"""
    
    # Sistem oluştur
    system = UAVDetectionSystem()
    
    # Görüntüde tespit yap
    result = system.detect_image('test_image.jpg')
    
    # Sonuçları göster
    print(f"Tespit edilen nesne sayısı: {result['count']}")
    print(f"İşlem süresi: {result['processing_time']:.3f}s")


# ============================================================
# ÖRNEK 2: Detaylı Tespit Bilgileri
# ============================================================
def example_2_detailed_detection():
    """Tespit detaylarına erişim"""
    
    system = UAVDetectionSystem(conf_threshold=0.3)
    result = system.detect_image('test_image.jpg')
    
    # Her tespit için
    for i, det in enumerate(result['detections'], 1):
        print(f"\nNesne {i}:")
        print(f"  Sınıf: {det['class']}")
        print(f"  Güven: {det['confidence']:.2f}")
        print(f"  Konum: {det['center']}")
        print(f"  Boyut: {det['width']:.0f}x{det['height']:.0f}")


# ============================================================
# ÖRNEK 3: Belirli Hedefleri Bul
# ============================================================
def example_3_find_targets():
    """Belirli sınıftaki nesneleri bul"""
    
    system = UAVDetectionSystem()
    result = system.detect_image('test_image.jpg')
    
    # Sadece araçları bul
    cars = system.get_target_info(result['detections'], 'car')
    trucks = system.get_target_info(result['detections'], 'truck')
    
    print(f"Araç sayısı: {len(cars)}")
    print(f"Kamyon sayısı: {len(trucks)}")
    
    # İlk aracın bilgileri
    if cars:
        car = cars[0]
        print(f"\nİlk araç:")
        print(f"  Konum: {car['position']}")
        print(f"  Güven: {car['confidence']:.2f}")


# ============================================================
# ÖRNEK 4: Video Tracking
# ============================================================
def example_4_video_tracking():
    """Video üzerinde tracking"""
    
    system = UAVDetectionSystem()
    
    # Video işle
    result = system.track_video(
        'test_video.mp4',
        save_result=True,
        show_progress=True
    )
    
    print(f"Toplam frame: {result['total_frames']}")
    print(f"Takip edilen hedef: {result['unique_tracks']}")
    print(f"İşlem hızı: {result['fps']:.1f} FPS")


# ============================================================
# ÖRNEK 5: Özel Confidence Threshold
# ============================================================
def example_5_custom_threshold():
    """Farklı confidence threshold'ları dene"""
    
    image_path = 'test_image.jpg'
    
    # Düşük threshold (daha fazla tespit, daha fazla yanlış alarm)
    system_low = UAVDetectionSystem(conf_threshold=0.15)
    result_low = system_low.detect_image(image_path, save_result=False)
    
    # Yüksek threshold (daha az tespit, daha az yanlış alarm)
    system_high = UAVDetectionSystem(conf_threshold=0.5)
    result_high = system_high.detect_image(image_path, save_result=False)
    
    print(f"Düşük threshold (0.15): {result_low['count']} tespit")
    print(f"Yüksek threshold (0.5): {result_high['count']} tespit")


# ============================================================
# ÖRNEK 6: Gerçek Zamanlı Webcam
# ============================================================
def example_6_realtime_webcam():
    """Webcam'den gerçek zamanlı tespit"""
    
    system = UAVDetectionSystem(conf_threshold=0.3)
    
    # Webcam'i aç (çıkmak için 'q' tuşuna bas)
    system.detect_realtime(source=0)


# ============================================================
# ÖRNEK 7: RTSP Stream
# ============================================================
def example_7_rtsp_stream():
    """RTSP stream'den tespit"""
    
    system = UAVDetectionSystem()
    
    # RTSP URL
    rtsp_url = "rtsp://username:password@ip:port/stream"
    
    # Stream'i işle
    system.detect_realtime(source=rtsp_url)


# ============================================================
# ÖRNEK 8: Toplu Görüntü İşleme
# ============================================================
def example_8_batch_processing():
    """Birden fazla görüntüyü işle"""
    
    from pathlib import Path
    
    system = UAVDetectionSystem()
    
    # Klasördeki tüm görüntüler
    image_folder = Path('test_images')
    image_files = list(image_folder.glob('*.jpg'))
    
    results = []
    for img_path in image_files:
        result = system.detect_image(str(img_path))
        results.append(result)
        print(f"{img_path.name}: {result['count']} tespit")
    
    # Toplam istatistikler
    total_detections = sum(r['count'] for r in results)
    avg_time = sum(r['processing_time'] for r in results) / len(results)
    
    print(f"\nToplam tespit: {total_detections}")
    print(f"Ortalama süre: {avg_time:.3f}s")


# ============================================================
# ÖRNEK 9: JSON Çıktısı Kullanma
# ============================================================
def example_9_json_output():
    """JSON çıktısını kullan"""
    
    import json
    
    system = UAVDetectionSystem()
    result = system.detect_image('test_image.jpg', save_result=True)
    
    # JSON dosyasını oku
    json_path = result['saved_json']
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # JSON'dan bilgi al
    print(f"Model: {data['model']}")
    print(f"Tespit sayısı: {data['count']}")
    
    # Tespitleri filtrele
    high_conf_detections = [
        d for d in data['detections'] 
        if d['confidence'] > 0.7
    ]
    print(f"Yüksek güvenli tespit: {len(high_conf_detections)}")


# ============================================================
# ÖRNEK 10: Hedef Takibi (Koordinat Bilgisi)
# ============================================================
def example_10_target_tracking():
    """Hedef koordinatlarını takip et"""
    
    system = UAVDetectionSystem()
    result = system.detect_image('test_image.jpg')
    
    # Araçları bul
    vehicles = [
        d for d in result['detections'] 
        if d['class'] in ['car', 'truck', 'van', 'bus']
    ]
    
    print(f"Toplam araç: {len(vehicles)}")
    
    # Her araç için koordinat bilgisi
    for i, vehicle in enumerate(vehicles, 1):
        cx, cy = vehicle['center']
        print(f"\nAraç {i} ({vehicle['class']}):")
        print(f"  Merkez koordinat: ({cx:.0f}, {cy:.0f})")
        print(f"  Güven: {vehicle['confidence']:.2%}")
        print(f"  Boyut: {vehicle['width']:.0f}x{vehicle['height']:.0f}px")


# ============================================================
# ÖRNEK 11: Performans Optimizasyonu
# ============================================================
def example_11_performance():
    """Performans için optimize edilmiş kullanım"""
    
    import time
    
    # GPU kullan, düşük confidence
    system = UAVDetectionSystem(
        conf_threshold=0.2,
        iou_threshold=0.5,
        device='0'  # GPU
    )
    
    # Birden fazla görüntü işle
    image_paths = ['img1.jpg', 'img2.jpg', 'img3.jpg']
    
    start = time.time()
    for img_path in image_paths:
        result = system.detect_image(img_path, save_result=False)
    elapsed = time.time() - start
    
    print(f"Toplam süre: {elapsed:.2f}s")
    print(f"Görüntü başına: {elapsed/len(image_paths):.3f}s")
    print(f"FPS: {len(image_paths)/elapsed:.1f}")


# ============================================================
# ÖRNEK 12: Hata Yönetimi
# ============================================================
def example_12_error_handling():
    """Hata yönetimi ile güvenli kullanım"""
    
    from pathlib import Path
    
    system = UAVDetectionSystem()
    
    image_path = 'test_image.jpg'
    
    try:
        # Dosya var mı kontrol et
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Dosya bulunamadı: {image_path}")
        
        # Tespit yap
        result = system.detect_image(image_path)
        
        # Sonuç kontrolü
        if result['count'] == 0:
            print("⚠️  Hiç nesne tespit edilemedi")
        else:
            print(f"✅ {result['count']} nesne tespit edildi")
    
    except FileNotFoundError as e:
        print(f"❌ Dosya hatası: {e}")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")


# ============================================================
# ANA PROGRAM
# ============================================================
if __name__ == "__main__":
    print("BAYKAR İHA Sistemi - Kullanım Örnekleri")
    print("=" * 60)
    print("\nHangi örneği çalıştırmak istersiniz?")
    print("1.  Basit görüntü tespiti")
    print("2.  Detaylı tespit bilgileri")
    print("3.  Belirli hedefleri bul")
    print("4.  Video tracking")
    print("5.  Özel confidence threshold")
    print("6.  Gerçek zamanlı webcam")
    print("7.  RTSP stream")
    print("8.  Toplu görüntü işleme")
    print("9.  JSON çıktısı kullanma")
    print("10. Hedef takibi (koordinat)")
    print("11. Performans optimizasyonu")
    print("12. Hata yönetimi")
    
    choice = input("\nSeçim (1-12): ").strip()
    
    examples = {
        '1': example_1_simple_detection,
        '2': example_2_detailed_detection,
        '3': example_3_find_targets,
        '4': example_4_video_tracking,
        '5': example_5_custom_threshold,
        '6': example_6_realtime_webcam,
        '7': example_7_rtsp_stream,
        '8': example_8_batch_processing,
        '9': example_9_json_output,
        '10': example_10_target_tracking,
        '11': example_11_performance,
        '12': example_12_error_handling,
    }
    
    if choice in examples:
        print(f"\n{'='*60}")
        examples[choice]()
    else:
        print("❌ Geçersiz seçim!")
