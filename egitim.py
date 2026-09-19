import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

HAREKETLER = ['not_defteri_ac', 'bekle', 'tarayici_ac', 'klasor_ac',
              'ses_artir', 'ekran_goruntusu', 'gorev_yoneticisi']

X_liste, y_liste = [], []


for i, h in enumerate(HAREKETLER):
    dosya = f"data/{h}.npy"
    if os.path.exists(dosya):
        veri = np.load(dosya)
        X_liste.append(veri)
        y_liste.extend([i] * veri.shape[0])
    else:
        print(f"UYARI: {dosya} bulunamadı")

X = np.concatenate(X_liste)
y = to_categorical(np.array(y_liste), num_classes=len(HAREKETLER))



X_egitim, X_test, y_egitim, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True, stratify=y
)


model = Sequential([
    Dense(128, activation='relu', input_shape=(63,)),
    Dropout(0.4), 
    Dense(64, activation='relu'),
    Dropout(0.4), 
    Dense(32, activation='relu'),
    Dense(len(HAREKETLER), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(X_egitim, y_egitim, epochs=50, batch_size=16, validation_data=(X_test, y_test))

model.save("hareket_tanima_modeli.h5")
print("Fotoğraf uyumlu standart eğitim başarıyla tamamlandı!")