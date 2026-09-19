import cv2, os
import mediapipe as mp
import numpy as np

HAREKETLER = ['not_defteri_ac', 'bekle', 'tarayici_ac', 'klasor_ac', 'onayla',
              'ses_artir', 'iptal', 'ekran_goruntusu', 'gorev_yoneticisi', 'hesap_makinesi']
HEDEF = 300

print("Mevcut hareketler:", ', '.join(HAREKETLER))
hareket = input("Hareket adı: ").strip()

os.makedirs("data", exist_ok=True)
kayit_yolu = f"data/{hareket}.npy"
mevcut = list(np.load(kayit_yolu)) if os.path.exists(kayit_yolu) else []
kalan = HEDEF - len(mevcut)

if kalan <= 0:
    print("Zaten 300 örnek var")
    exit()

print(f"{kalan} örnek toplanacak. 'r' ile başla, 'q' ile çık.")

eller = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cizim = mp.solutions.drawing_utils
kamera, toplanan, kayit, sayac = cv2.VideoCapture(0), [], False, 0

while True:
    ok, kare = kamera.read()
    if not ok: break

    kare = cv2.flip(kare, 1)
    sonuc = eller.process(cv2.cvtColor(kare, cv2.COLOR_BGR2RGB))

    if sonuc.multi_hand_landmarks:
        el = sonuc.multi_hand_landmarks[0]
        cizim.draw_landmarks(kare, el, mp.solutions.hands.HAND_CONNECTIONS)

        if kayit and sayac < kalan:
            koordinatlar = [v for nokta in el.landmark for v in (nokta.x, nokta.y, nokta.z)]
            toplanan.append(koordinatlar)
            sayac += 1
            cv2.putText(kare, f"Kaydediliyor: {sayac}/{kalan}",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        elif sayac >= kalan:
            np.save(kayit_yolu, np.array(mevcut + toplanan))
            print(f" Kaydedildi → toplam {len(mevcut)+len(toplanan)} örnek")
            break
    else:
        if kayit:
            cv2.putText(kare, "El bulunamadi", (10,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Veri Toplama", kare)
    tus = cv2.waitKey(1) & 0xFF
    if tus == ord('q'): break
    elif tus == ord('r') and not kayit:
        kayit = True
        print("Kayıt başladı")

kamera.release()
cv2.destroyAllWindows()