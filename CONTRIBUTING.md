# 🤝 Katkıda Bulunma Rehberi

İHA Görüntü İşleme ve Hedef Takip Sistemi projesine katkıda bulunmak istediğiniz için teşekkür ederiz!

## 🚀 Nasıl Katkıda Bulunabilirsiniz?

### 1. Issue Açma

Hata bildirimi veya özellik önerisi için:

1. [Issues](https://github.com/furkanbaskurthub-lgtm/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi/issues) sayfasına gidin
2. "New Issue" butonuna tıklayın
3. Uygun template'i seçin (Bug Report / Feature Request)
4. Detaylı açıklama yazın

### 2. Pull Request Gönderme

1. **Fork yapın**
   ```bash
   # GitHub'da "Fork" butonuna tıklayın
   ```

2. **Clone edin**
   ```bash
   git clone https://github.com/YOUR_USERNAME/iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi.git
   cd iha-Goruntu-isleme-ve-coklu-Hedef-Takip-Sistemi
   ```

3. **Branch oluşturun**
   ```bash
   git checkout -b feature/amazing-feature
   # veya
   git checkout -b fix/bug-fix
   ```

4. **Değişikliklerinizi yapın**
   - Kod yazın
   - Test edin
   - Dokümantasyon güncelleyin

5. **Commit edin**
   ```bash
   git add .
   git commit -m "feat: Add amazing feature"
   ```

6. **Push edin**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Pull Request açın**
   - GitHub'da repository'nize gidin
   - "Compare & pull request" butonuna tıklayın
   - Değişikliklerinizi açıklayın

## 📝 Commit Mesajları

Conventional Commits formatını kullanın:

```
feat: Yeni özellik ekleme
fix: Hata düzeltme
docs: Dokümantasyon değişikliği
style: Kod formatı (işlevselliği etkilemeyen)
refactor: Kod yeniden yapılandırma
test: Test ekleme/düzeltme
chore: Build/config değişiklikleri
```

Örnekler:
```bash
git commit -m "feat: Add real-time camera support"
git commit -m "fix: GPU memory leak in video processing"
git commit -m "docs: Update installation guide"
```

## 🧪 Test Etme

Değişikliklerinizi test edin:

```bash
# Temel testler
python -m pytest tests/

# Docker testi
docker build -t iha-test .
docker run --rm iha-test python3 docker-test.py

# Manuel test
python run_detection.py
```

## 📋 Kod Standartları

### Python Stil Rehberi

- **PEP 8** standartlarına uyun
- **Type hints** kullanın
- **Docstring** yazın

```python
def detect_objects(image: np.ndarray, confidence: float = 0.5) -> List[Detection]:
    """
    Görüntüde nesneleri tespit eder.
    
    Args:
        image: Input görüntü (numpy array)
        confidence: Minimum güven skoru (0-1)
    
    Returns:
        Tespit edilen nesnelerin listesi
    """
    pass
```

### Dosya Organizasyonu

```
src/
├── api/          # API ve interface'ler
├── core/         # Temel algoritmalar
├── data/         # Veri işleme
├── training/     # Model eğitimi
├── evaluation/   # Değerlendirme
└── utils/        # Yardımcı fonksiyonlar
```

## 🎯 Katkı Alanları

### Öncelikli İhtiyaçlar

1. **Performans İyileştirmeleri**
   - GPU optimizasyonu
   - Batch processing
   - Multi-threading

2. **Yeni Özellikler**
   - Farklı model desteği (YOLOv10, YOLO-NAS)
   - REST API
   - Web interface
   - Mobile deployment

3. **Dokümantasyon**
   - Tutorial'lar
   - Video kılavuzlar
   - API dokümantasyonu
   - Çeviri (İngilizce)

4. **Test Coverage**
   - Unit testler
   - Integration testler
   - Performance testler

### Kolay Başlangıç İçin

"good first issue" etiketli issue'lara bakın:
- Dokümantasyon düzeltmeleri
- Küçük bug fix'ler
- Örnek kod ekleme

## 🐛 Hata Bildirimi

Hata bildirirken şunları ekleyin:

1. **Açıklama**: Ne oldu?
2. **Beklenen davranış**: Ne olmalıydı?
3. **Adımlar**: Hatayı nasıl tekrar oluşturabiliriz?
4. **Ortam**:
   - OS: Windows/Linux/Mac
   - Python version
   - GPU: Model ve CUDA version
   - PyTorch version
5. **Loglar**: Hata mesajları
6. **Ekran görüntüsü**: Varsa

## 💡 Özellik Önerisi

Özellik önerirken şunları ekleyin:

1. **Problem**: Hangi sorunu çözüyor?
2. **Çözüm**: Önerilen yaklaşım
3. **Alternatifler**: Düşünülen diğer yöntemler
4. **Ek bilgi**: Referanslar, örnekler

## 📞 İletişim

- **GitHub Issues**: Teknik sorular ve bug report
- **Discussions**: Genel tartışmalar ve sorular
- **Email**: Özel konular için

## 🙏 Teşekkürler

Her türlü katkı değerlidir:
- Kod
- Dokümantasyon
- Test
- Bug report
- Özellik önerisi
- Yıldız ⭐

Katkılarınız için teşekkür ederiz! 🚁
