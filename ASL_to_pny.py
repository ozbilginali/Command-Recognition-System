import cv2
import mediapipe as mp
import numpy as np
import os

# MediaPipe ayarları
mp_eller = mp.solutions.hands
eller = mp_eller.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.3
)

# Yollar
PROJE_KLASORU = r"C:\Real-Time-Command-Recognition"
DATA_KLASORU = os.path.join(PROJE_KLASORU, "data")

# Hangi klasör hangi hareket ismine karşılık gelir
klasorler = {
    "A" : "not_defteri_ac",
    "B" : "bekle",
    "C" : "tarayici_ac",
    "D" : "klasor_ac",
    "L" : "ses_artir",
    "V" : "ekran_goruntusu",
    "W" : "gorev_yoneticisi",
}

for klasor, hareket_adi in klasorler.items():
    klasor_yolu = os.path.join(DATA_KLASORU, klasor)
    koordinatlar_listesi = []

    print(f"İşleniyor: {klasor} → {hareket_adi}")

    for dosya in os.listdir(klasor_yolu):
        if not dosya.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        resim_yolu = os.path.join(klasor_yolu, dosya)
        resim = cv2.imread(resim_yolu)
        if resim is None:
            continue

        resim_rgb = cv2.cvtColor(resim, cv2.COLOR_BGR2RGB)
        sonuc = eller.process(resim_rgb)

        if sonuc.multi_hand_landmarks:
            koordinatlar = []
            for nokta in sonuc.multi_hand_landmarks[0].landmark:
                koordinatlar.extend([nokta.x, nokta.y, nokta.z])
            koordinatlar_listesi.append(koordinatlar)

    if koordinatlar_listesi:
        kayit_yolu = os.path.join(DATA_KLASORU, f"{hareket_adi}.npy")
        np.save(kayit_yolu, np.array(koordinatlar_listesi))
        print(f"   {len(koordinatlar_listesi)} örnek → {hareket_adi}.npy")
    else:
        print(f"   Hiç el tespit edilemedi: {klasor}")

print("\nTamamlandı data klasörü içeriği:")
for f in os.listdir(DATA_KLASORU):
    if f.endswith('.npy'):
        data = np.load(os.path.join(DATA_KLASORU, f))
        print(f"  {f} → {len(data)} örnek")