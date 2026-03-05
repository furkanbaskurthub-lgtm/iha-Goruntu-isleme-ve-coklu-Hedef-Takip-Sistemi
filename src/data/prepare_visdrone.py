"""
VisDrone veri setini YOLO formatına dönüştürme scripti
"""
import os
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import shutil


def convert_box(size, box):
    """
    VisDrone formatını YOLO formatına çevir
    VisDrone: [x_topleft, y_topleft, width, height]
    YOLO: [x_center, y_center, width, height] (normalize edilmiş)
    """
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x_center = (box[0] + box[2] / 2) * dw
    y_center = (box[1] + box[3] / 2) * dh
    w = box[2] * dw
    h = box[3] * dh
    return x_center, y_center, w, h


def visdrone2yolo(data_dir):
    """
    VisDrone annotation'larını YOLO formatına dönüştür
    """
    data_dir = Path(data_dir)
    annotations_dir = data_dir / 'annotations'
    images_dir = data_dir / 'images'
    labels_dir = data_dir / 'labels'
    
    # Labels klasörünü oluştur
    labels_dir.mkdir(parents=True, exist_ok=True)
    
    if not annotations_dir.exists():
        print(f"⚠️  {annotations_dir} bulunamadı, atlanıyor...")
        return
    
    print(f"🔄 {data_dir.name} dönüştürülüyor...")
    
    annotation_files = list(annotations_dir.glob('*.txt'))
    
    for ann_file in tqdm(annotation_files, desc=f'Converting {data_dir.name}'):
        # Karşılık gelen görüntüyü bul
        img_file = images_dir / ann_file.with_suffix('.jpg').name
        
        if not img_file.exists():
            continue
            
        # Görüntü boyutunu al
        try:
            img = Image.open(img_file)
            img_size = img.size
            img.close()
        except Exception as e:
            print(f"❌ {img_file} okunamadı: {e}")
            continue
        
        # Annotation'ları oku ve dönüştür
        lines = []
        with open(ann_file, 'r') as f:
            for line in f.read().strip().splitlines():
                row = line.split(',')
                
                # VisDrone formatı: <bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>
                if len(row) < 6:
                    continue
                
                # Ignored regions (class 0) ve score 0 olanları atla
                if row[4] == '0' or row[5] == '0':
                    continue
                
                # Class ID (VisDrone 1-10, YOLO 0-9)
                cls = int(row[5]) - 1
                
                # Bounding box
                bbox = tuple(map(int, row[:4]))
                
                # YOLO formatına çevir
                yolo_box = convert_box(img_size, bbox)
                
                # YOLO formatında kaydet
                lines.append(f"{cls} {' '.join(f'{x:.6f}' for x in yolo_box)}\n")
        
        # Label dosyasını yaz
        label_file = labels_dir / ann_file.name
        with open(label_file, 'w') as f:
            f.writelines(lines)


def prepare_dataset(raw_dir='data/raw'):
    """
    Tüm VisDrone veri setini hazırla
    """
    raw_dir = Path(raw_dir)
    
    print("=" * 60)
    print("🚁 VisDrone Veri Seti Hazırlama")
    print("=" * 60)
    
    # Dönüştürülecek klasörler
    datasets = [
        'VisDrone2019-DET-train/VisDrone2019-DET-train',
        'VisDrone2019-DET-val/VisDrone2019-DET-val',
        'VisDrone2019-DET-test-dev/VisDrone2019-DET-test-dev'
    ]
    
    for dataset in datasets:
        dataset_path = raw_dir / dataset
        if dataset_path.exists():
            visdrone2yolo(dataset_path)
        else:
            print(f"⚠️  {dataset_path} bulunamadı")
    
    print("\n✅ Veri seti hazırlama tamamlandı!")
    print("\n📊 İstatistikler:")
    
    # İstatistikleri göster
    for dataset in datasets:
        dataset_path = raw_dir / dataset
        labels_dir = dataset_path / 'labels'
        if labels_dir.exists():
            label_count = len(list(labels_dir.glob('*.txt')))
            print(f"  • {dataset_path.name}: {label_count} label dosyası")


if __name__ == "__main__":
    prepare_dataset()
