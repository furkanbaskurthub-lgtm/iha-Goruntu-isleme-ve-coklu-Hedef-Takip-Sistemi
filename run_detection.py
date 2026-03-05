"""
BAYKAR İHA Tespit Sistemi - Ana Program
Kullanımı kolay, production ready
"""
import sys
from pathlib import Path
from src.api.detection_api import UAVDetectionSystem


def main():
    """Ana program"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           BAYKAR İHA TESPİT VE TAKİP SİSTEMİ               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Sistem oluştur
    system = UAVDetectionSystem(
        model_path='runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt',
        conf_threshold=0.25,  # Confidence eşiği (0.1-0.9)
        device='auto'         # Otomatik GPU/CPU seçimi
    )
    
    print("\n" + "=" * 60)
    print("KULLANIM MODLARı")
    print("=" * 60)
    print("1. Görüntü Tespiti (tek görüntü)")
    print("2. Video Tracking (video dosyası)")
    print("3. Gerçek Zamanlı (webcam/stream)")
    print("4. Toplu İşlem (klasördeki tüm görüntüler)")
    print("5. Çıkış")
    print("=" * 60)
    
    while True:
        choice = input("\nSeçiminiz (1-5): ").strip()
        
        if choice == '1':
            # Görüntü tespiti
            image_path = input("Görüntü yolu: ").strip()
            
            if not Path(image_path).exists():
                print("❌ Dosya bulunamadı!")
                continue
            
            print("\n🔍 Tespit yapılıyor...")
            result = system.detect_image(image_path, save_result=True)
            
            print("\n" + "=" * 60)
            print("📊 SONUÇLAR")
            print("=" * 60)
            print(f"✅ Tespit edilen nesne: {result['count']}")
            print(f"⏱️  İşlem süresi: {result['processing_time']:.3f}s")
            print(f"📁 Sonuç: {result.get('saved_image', 'N/A')}")
            
            # Sınıf bazında sayım
            if result['count'] > 0:
                class_counts = {}
                for det in result['detections']:
                    cls = det['class']
                    class_counts[cls] = class_counts.get(cls, 0) + 1
                
                print("\n📋 Sınıf Bazında:")
                for cls, count in sorted(class_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f"   • {cls}: {count}")
            
            print("=" * 60)
        
        elif choice == '2':
            # Video tracking
            video_path = input("Video yolu: ").strip()
            
            if not Path(video_path).exists():
                print("❌ Dosya bulunamadı!")
                continue
            
            print("\n🎥 Video işleniyor...")
            result = system.track_video(video_path, save_result=True, show_progress=True)
            
            print("\n" + "=" * 60)
            print("📊 SONUÇLAR")
            print("=" * 60)
            print(f"🎬 Toplam frame: {result['total_frames']}")
            print(f"🎯 Toplam tespit: {result['total_detections']}")
            print(f"🔢 Takip edilen hedef: {result['unique_tracks']}")
            print(f"⏱️  İşlem süresi: {result['processing_time']:.1f}s")
            print(f"🚀 İşlem hızı: {result['fps']:.1f} FPS")
            print(f"📁 Sonuç: {result.get('output_video', 'N/A')}")
            print("=" * 60)
        
        elif choice == '3':
            # Gerçek zamanlı
            print("\n📹 Gerçek zamanlı tespit")
            print("   1. Webcam (varsayılan)")
            print("   2. RTSP stream")
            
            rt_choice = input("Seçim (1-2): ").strip()
            
            if rt_choice == '1':
                source = 0
            elif rt_choice == '2':
                source = input("RTSP URL: ").strip()
            else:
                print("❌ Geçersiz seçim!")
                continue
            
            system.detect_realtime(source=source)
        
        elif choice == '4':
            # Toplu işlem
            folder_path = input("Klasör yolu: ").strip()
            folder = Path(folder_path)
            
            if not folder.exists():
                print("❌ Klasör bulunamadı!")
                continue
            
            # Görüntü dosyalarını bul
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
                image_files.extend(folder.glob(ext))
            
            if not image_files:
                print("❌ Görüntü dosyası bulunamadı!")
                continue
            
            print(f"\n📸 {len(image_files)} görüntü işlenecek...")
            
            total_detections = 0
            for i, img_path in enumerate(image_files, 1):
                print(f"\n[{i}/{len(image_files)}] {img_path.name}")
                result = system.detect_image(str(img_path), save_result=True)
                total_detections += result['count']
                print(f"   ✅ {result['count']} nesne tespit edildi")
            
            print("\n" + "=" * 60)
            print("📊 TOPLU İŞLEM SONUÇLARI")
            print("=" * 60)
            print(f"📸 İşlenen görüntü: {len(image_files)}")
            print(f"🎯 Toplam tespit: {total_detections}")
            print(f"📊 Ortalama: {total_detections/len(image_files):.1f} nesne/görüntü")
            print("=" * 60)
        
        elif choice == '5':
            print("\n👋 Çıkılıyor...")
            break
        
        else:
            print("❌ Geçersiz seçim! (1-5)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program sonlandırıldı (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()
