import cv2
import os
import csv
import re  # Yıl bilgisi (regex) 

# KULLANICI AYARLARI
video_path = 'PATH_TO_VIDEO.mp4' # Video dosyası yolu
output_folder = 'sample_outputs/faces'  # Yüzlerin kaydedileceği klasör
csv_file = 'sample_outputs/faces/etiketler.csv'  # Etiketlerin kaydedileceği CSV dosyası
frame_skip = 60  # Kaç frame'de bir yüz aranacak (örneğin her 60 frame'de 1)
resize_factor = 0.5  # Görüntü boyutunu küçültme oranı

# Klasör oluştur (varsa geç)
os.makedirs(output_folder, exist_ok=True)

# CSV dosyası oluştur (varsa aç)
csv_exists = os.path.isfile(csv_file)
csvfile = open(csv_file, 'a', newline='', encoding='utf-8')
csvwriter = csv.writer(csvfile)

# Eğer yeni oluşturuluyorsa başlıkları yaz
if not csv_exists:
    csvwriter.writerow(['video_adı', 'frame_id', 'fotoğraf_ismi', 'etiket', 'yıl'])

# Video aç
cap = cv2.VideoCapture(video_path)
frame_id = 0

# FPS değerini kontrol et
fps = cap.get(cv2.CAP_PROP_FPS)  # Frame per second (fps) değeri
if fps == 0:
    print("FPS alınamadı, video dosyasını kontrol edin.")
    cap.release()  # Kaynağı serbest bırakıyoruz
    csvfile.close()  # Dosyayı kapatıyoruz
    cv2.destroyAllWindows()  # Pencereleri temizliyoruz
    exit()  # FPS alınamıyorsa işlem durduruluyor
print(f"FPS: {fps}")

# Video çözünürlüğü
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Genişlik
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Yükseklik

# Yüz tanıyıcı (OpenCV // Haarcascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Videonun yıl bilgisini dosya adından al (örneğin: 'VID_20210117_041124.mp4' -> '2021')
video_year = re.search(r'(\d{4})', os.path.basename(video_path))  # Yıl bilgisini regex ile al
if video_year:
    video_year = video_year.group(1)  # Yıl bilgisi alındı
else:
    video_year = 'NONE'  # Yıl bilgisi alınamadıysa NONE kullanıyoruz
print(f"Video Yılı: {video_year}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Video sona erdi veya okuma hatası!")
        break  # Video bitti veya okuma hatası var

    # Kareyi küçült 
    frame_resized = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor)

    # Yüz algılama işlemi her `frame_skip` karede yapılır
    if frame_id % frame_skip == 0:
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Dakika ve saniyeyi hesapla
        minutes = int(frame_id // (fps * 60))  # Dakika hesaplama
        seconds = int((frame_id // fps) % 60)  # Saniye hesaplama

        for idx, (x, y, w, h) in enumerate(faces):
            face_img = frame_resized[y:y+h, x:x+w]
            face_filename = f"{os.path.splitext(os.path.basename(video_path))[0]}_frame{frame_id}_face{idx}.jpg"
            face_path = os.path.join(output_folder, face_filename)

            # Yüzü kaydet
            cv2.imwrite(face_path, face_img)

            # Kullanıcıdan etiket iste 
            print(f"Frame {frame_id} | Dakika {minutes}, Saniye {seconds} | Yüz {idx} algılandı: {face_filename}")
            etiket = input("Bu yüzün etiketi nedir? (örnek: happy, sad, exciting, neutral): ")

            # CSV'ye yaz (yıl bilgisi ekleyerek)
            csvwriter.writerow([os.path.basename(video_path), frame_id, face_filename, etiket, video_year])

            # Yüzü çerçeve içine al
            cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Algılanan yüzleri ekranda göster
        cv2.putText(frame_resized, 'Face Detection', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    frame_id += 1

    # Yüz algılama penceresinin boyutunu ayarla ve köşeye yerleştir
    cv2.namedWindow('Face Detection', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Face Detection', 300, 300) # pencere boyutu
    cv2.moveWindow('Face Detection', 10, 10)  # Pencere sol üst köşede

    # Yüz algılama penceresini göster
    cv2.imshow('Face Detection', frame_resized)

    # 'q' tuşuna basarak çıkış (yapılabilir)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Kaynağı serbest bırak
csvfile.close()  # CSV dosyasını kapat
cv2.destroyAllWindows()  # OpenCV pencerelerini kapatıyoruz

print("İşlem tamamlandı!")
