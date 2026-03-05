"""
Kurulum testi - Her şeyin çalıştığını doğrula
"""
from pathlib import Path
from ultralytics import YOLO
import torch

print("=" * 60)
print("🚁 BAYKAR İHA PROJESİ - KURULUM TESTİ")
print("=" * 60)

# 1. GPU Kontrolü
print("\n1️⃣ GPU Kontrolü:")
if torch.cuda.is_available():
    print(f"   ✅ GPU kullanılabilir: {torch.cuda.get_device_name(0)}")
    print(f