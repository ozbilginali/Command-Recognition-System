# Komut Tanıma Sistemi

Bu proje, web kamerası üzerinden el hareketlerinizi (jestleri) tanıyarak bilgisayarınızda belirli komutları (fare kontrolü, kısayollar vb.) çalıştırmanızı sağlayan yapay zeka tabanlı bir uygulamadır.

---

## Kurulum ve Çalıştırma Bölümü

Projeyi bilgisayarınızda sorunsuz bir şekilde ayağa kaldırmak için aşağıdaki adımları sırasıyla ve eksiksiz bir şekilde takip etmeniz gerekmektedir.

### 1. Python Kurulumu ve Sürüm Uyumluluğu
Sistemde kullanılan derin öğrenme ve yapay zeka kütüphanelerinin (özellikle TensorFlow) kararlı çalışabilmesi için bilgisayarınızda Python 3.10 veya Python 3.11 sürümünün yüklü olması şarttır. Daha yeni sürümler (Python 3.12, 3.13 vb.) bu yapay zeka modellerini henüz resmi olarak desteklememektedir.

1. Bilgisayarınızda halihazırda Python 3.13 veya farklı bir uyumsuz sürüm yüklüyse, kurulum çakışmalarını önlemek adına öncelikle bu sürümü Denetim Masası üzerinden tamamen kaldırın.
2. Resmi Python 3.11 İndirme Sayfası (https://www.python.org/downloads/release/python-3119/) üzerinden Windows mimarinize uygun olan kararlı sürümü indirin ve kurulum dosyasını çalıştırın.
3. KURULUM ESNASINDA DİKKAT EDİLMESİ GEREKEN KRİTİK ADIM: Kurulum arayüzü ilk açıldığında, pencerenin en altında yer alan "Add Python to PATH" (Python'ı PATH'e ekle) kutucuğunu MUTLAKA işaretleyin. Bu kutucuk işaretlenmeden yapılan kurulumlarda sistem komutları algılamayacaktır. Kutucuğu işaretledikten sonra "Install Now" diyerek işlemi tamamlayın.

### 2. Gerekli Yapay Zeka ve Arayüz Kütüphanelerinin Yüklenmesi
Sistemin el takibi yapabilmesi, görüntü işlemesi ve komutları tetikleyebilmesi için gerekli kütüphanelerin terminal üzerinden manuel olarak indirilmesi gerekmektedir.

1. Bilgisayarınızın arama çubuğuna "cmd" yazarak Komut İstemi (Terminal) penceresini açın.
2. Aşağıdaki komut satırını tamamen kopyalayın, terminal penceresine sağ tıklayarak yapıştırın ve Enter tuşuna basın:

pip install opencv-python mediapipe numpy pyautogui pillow tensorflow

3. Bu işlem internet hızınıza ve bilgisayar performansınıza bağlı olarak birkaç dakika sürebilir. İndirme esnasında terminali kapatmayın. Yükleme sorunsuz tamamlandığında terminal hata vermeden yeni bir satır başına geçecektir.

### 3. Uygulamanın Başlatılması ve Çalıştırılması
1. Size iletilen ZIP arşivini sağ tıklayarak bir klasöre çıkartın.
2. Proje klasörünün içerisindeki "app.py" ana dosyasına sağ tıklayıp "Birlikte Aç -> Python" seçeneğini seçerek uygulamayı doğrudan başlatabilirsiniz.
3. Alternatif olarak; Komut İstemi (cmd) üzerinden proje klasörünün bulunduğu dizine geçiş yaparak "python app.py" komutuyla da sistemi çalıştırabilirsiniz.

---

## Olası Hatalar ve Çözüm Yolları

* AttributeError: module 'mediapipe' has no attribute 'solutions' Hatası:
  Kütüphanelerin indirilmesi esnasında internet dalgalanmasından ötürü eksik kurulum gerçekleştiğinde bu hata alınır. Çözüm için terminale "pip install --force-reinstall mediapipe" yazarak kütüphaneyi sıfırdan ve temiz bir şekilde kurun.

* UnicodeDecodeError (Karakter Kodlama Hatası):
  Proje klasörünün bulunduğu dizin yolunda (Örn: C:\Users\KullanıcıAdı\Masaüstü...) Türkçe karakterler (ç, ş, ı, g, ö, ü, ü) yer alıyorsa TensorFlow modeli yüklenirken hata verebilir. Çözüm için proje klasörünün adını tamamen İngilizce karakterlerden oluşacak şekilde (Örn: "proje_kod") değiştirin veya klasörü doğrudan Yerel Disk C içerisine taşıyın.

---

## Proje Klasör Yapısı ve Dosya Görevleri

* app.py: Uygulamanın grafiksel arayüzünü (Tkinter) yöneten, kamera görüntüsünü işleyen ve ana mantığı çalıştıran kök dosyadır.
* hareket_tanima_modeli.h5: Önceden eğitilmiş, el hareketlerini ve anlamlarını hafızasında tutan derin öğrenme model dosyasıdır (Yapay zeka beyni).
* icons/: Uygulama arayüzünde kullanılan görsel tasarımların, butonların ve el simgelerinin yer aldığı yardımcı kaynak klasörüdür.