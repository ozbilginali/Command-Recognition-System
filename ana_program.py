import os, cv2, webbrowser
import mediapipe as mp
import numpy as np
import pyautogui
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model

HAREKETLER = ['not_defteri_ac', 'bekle', 'tarayici_ac', 'klasor_ac',
              'ses_artir', 'ekran_goruntusu', 'gorev_yoneticisi']

KOMUTLAR = {
    "not_defteri_ac":  lambda: os.system("notepad"),
    "bekle":           lambda: None,
    "tarayici_ac":     lambda: webbrowser.open("https://www.google.com"),
    "klasor_ac":       lambda: os.startfile("C:\\"),
    "ses_artir":       lambda: pyautogui.press('volumeup'),
    "ekran_goruntusu": lambda: pyautogui.press('printscreen'),
    "gorev_yoneticisi":lambda: pyautogui.hotkey('ctrl','shift','esc'),
}

model = load_model("hareket_tanima_modeli.h5")
eller = mp.solutions.hands.Hands(
    static_image_mode=False, max_num_hands=1,
    min_detection_confidence=0.7, min_tracking_confidence=0.5
)
cizim = mp.solutions.drawing_utils
kamera = cv2.VideoCapture(0)
sayac, son_hareket, son_calistirilan = 0, "", ""

while kamera.isOpened():
    ok, kare = kamera.read()
    if not ok: break

    kare = cv2.flip(kare, 1)
    sonuc = eller.process(cv2.cvtColor(kare, cv2.COLOR_BGR2RGB))

    if sonuc.multi_hand_landmarks:
        el = sonuc.multi_hand_landmarks[0]
        cizim.draw_landmarks(kare, el, mp.solutions.hands.HAND_CONNECTIONS)

        koordinatlar = [v for nokta in el.landmark for v in (nokta.x, nokta.y, nokta.z)]
        tahmin = model.predict(np.array([koordinatlar]), verbose=0)
        hareket = HAREKETLER[np.argmax(tahmin)]
        guven = tahmin[0][np.argmax(tahmin)]

        if guven > 0.95:
            cv2.putText(kare, f"{hareket} ({int(guven*100)}%)",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            if hareket == son_hareket:
                sayac += 1
            else:
                sayac, son_hareket = 0, hareket
                if son_calistirilan != hareket:
                    son_calistirilan = ""

            if sayac == 10 and son_calistirilan != hareket:
                print(f">>> KOMUT: {hareket}")
                KOMUTLAR[hareket]()
                son_calistirilan, sayac = hareket, 0

    cv2.imshow("Komut Tanima", kare)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

kamera.release()
cv2.destroyAllWindows()