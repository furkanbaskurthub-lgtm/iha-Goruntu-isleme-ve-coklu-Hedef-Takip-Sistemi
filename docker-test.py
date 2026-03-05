#!/usr/bin/env python3
"""
Docker Container Test Scripti
Container içinde çalıştırılarak sistem sağlığını kontrol eder
"""

import sys
import torch
import cv2
import numpy as np
from pathlib import Path

def test_gpu():
    """GPU erişimini test et"""
    print("🔍 GPU Testi...")
    try:
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            memory_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✅ GPU bulundu: {device_name}")
            print(f"   Toplam bellek: {memory_total:.2f} GB")
            
            # Basit tensor işlemi
            x = torch.randn(1000, 1000).cuda()
            y = torch.matmul(x, x)
            print(f"   Tensor işlemi başarılı: {y.shape}")
            return True
        else:
            print("❌ GPU bulunamadı!")
            return False
    except Exception as e:
        print(f"❌ GPU testi başarısız: {e}")
        return False

def test_opencv():
    """OpenCV kurulumunu test et"""
    print("\n🔍 OpenCV Testi...")
    try:
        # Basit görüntü oluştur
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.rectangle(img, (10, 10), (90, 90), (0, 255, 0), 2)
        
        # Encode/decode test
        _, buffer = cv2.imencode('.jpg', img)
        decoded = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        
        print(f"✅ OpenCV çalışıyor: v{cv2.__version__}")
        print(f"   Test görüntü: {decoded.shape}")
        return True
    except Exception as e:
        print(f"❌ OpenCV testi başarısız: {e}")
        return False

def test_ultralytics():
    """Ultralytics YOLO kurulumunu test et"""
    print("\n🔍 Ultralytics YOLO Testi...")
    try:
        from ultralytics import YOLO
        
        # Nano model indir (küçük)
        model = YOLO('yolov8n.pt')
        print(f"✅ YOLO model yüklendi")
        
        # Dummy inference
        img = np.zeros((640, 640, 3), dtype=np.uint8)
        results = model(img, verbose=False)
        print(f"   Inference başarılı: {len(results)} sonuç")
        return True
    except Exception as e:
        print(f"❌ YOLO testi başarısız: {e}")
        return False

def test_directories():
    """Gerekli dizinleri kontrol et"""
    print("\n🔍 Dizin Yapısı Testi...")
    required_dirs = [
        'data',
        'models',
        'outputs',
        'runs',
        'logs',
        'src',
        'configs'
    ]
    
    all_ok = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}/ mevcut")
        else:
            print(f"❌ {dir_name}/ bulunamadı!")
            all_ok = False
    
    return all_ok

def test_model_file():
    """Model dosyasını kontrol et"""
    print("\n🔍 Model Dosyası Testi...")
    model_paths = [
        'models/best.pt',
        'runs/detect/runs/train/visdrone_yolo_full4/weights/best.pt',
        'runs/train/visdrone_yolo_full/weights/best.pt'
    ]
    
    for model_path in model_paths:
        if Path(model_path).exists():
            size_mb = Path(model_path).stat().st_size / 1024**2
            print(f"✅ Model bulundu: {model_path}")
            print(f"   Boyut: {size_mb:.2f} MB")
            return True
    
    print("⚠️  Model dosyası bulunamadı (eğitim gerekli)")
    return False

def test_imports():
    """Tüm gerekli paketleri import et"""
    print("\n🔍 Python Paketleri Testi...")
    packages = {
        'torch': 'PyTorch',
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'ultralytics': 'Ultralytics',
        'yaml': 'PyYAML',
        'tqdm': 'tqdm',
        'matplotlib': 'Matplotlib',
        'pandas': 'Pandas',
        'PIL': 'Pillow'
    }
    
    all_ok = True
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} yüklenemedi!")
            all_ok = False
    
    return all_ok

def main():
    """Ana test fonksiyonu"""
    print("=" * 70)
    print("🚁 BAYKAR İHA DOCKER CONTAINER TEST")
    print("=" * 70)
    
    results = {
        'GPU': test_gpu(),
        'OpenCV': test_opencv(),
        'Ultralytics': test_ultralytics(),
        'Directories': test_directories(),
        'Model': test_model_file(),
        'Imports': test_imports()
    }
    
    print("\n" + "=" * 70)
    print("📊 TEST SONUÇLARI")
    print("=" * 70)
    
    for test_name, result in results.items():
        status = "✅ BAŞARILI" if result else "❌ BAŞARISIZ"
        print(f"{test_name:15s}: {status}")
    
    print("=" * 70)
    
    # Genel sonuç
    all_passed = all(results.values())
    if all_passed:
        print("🎉 Tüm testler başarılı! Container hazır.")
        return 0
    else:
        failed = [name for name, result in results.items() if not result]
        print(f"⚠️  Bazı testler başarısız: {', '.join(failed)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
