import os, cv2, webbrowser, threading
import mediapipe as mp
import numpy as np
import pyautogui
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model
import sys

# 🚀 Sihirli Yol Bulucu Fonksiyon (Projeyi taşınabilir yapar, hata almayı önler)
def kaynak_yolu(goreceli_yol):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__)) # Dosyanın o anki klasörünü bulur
    return os.path.join(base_path, goreceli_yol)

HAREKETLER = ['not_defteri_ac', 'bekle', 'tarayici_ac', 'klasor_ac',
              'ses_artir', 'ekran_goruntusu', 'gorev_yoneticisi']

KOMUT_ETIKET = {
    'not_defteri_ac':  'Not Defteri Aç',
    'bekle':           'Bekle',
    'tarayici_ac':     'Tarayıcı Aç',
    'klasor_ac':       'Klasör Aç',
    'ses_artir':       'Ses Artır',
    'ekran_goruntusu': 'Ekran Görüntüsü',
    'gorev_yoneticisi':'Görev Yöneticisi',
}

KOMUTLAR = {
    'not_defteri_ac':  lambda: os.system("notepad"),
    'bekle':           lambda: None,
    'tarayici_ac':     lambda: webbrowser.open("https://www.google.com"),
    'klasor_ac':       lambda: os.startfile("C:\\"),
    'ses_artir':       lambda: pyautogui.press('volumeup', presses=3),
    'ekran_goruntusu': lambda: pyautogui.press('printscreen'),
    'gorev_yoneticisi':lambda: pyautogui.hotkey('ctrl','shift','esc'),
}

EL_SEMBOL = {
    'not_defteri_ac':  '1',
    'bekle':           '2',
    'tarayici_ac':     '3',
    'klasor_ac':       '4',
    'ses_artir':       '5',
    'ekran_goruntusu': '6',
    'gorev_yoneticisi':'7',
}

GORUNTU_DOSYALARI = [
    'not_defteri_ac.png',  
    'bekle.png',           
    'tarayici_ac.png',     
    'klasor_ac.png',       
    'ses_artir.png',       
    'ekran_goruntusu.png', 
    'gorev_yoneticisi.png' 
]

CAM_W, CAM_H = 620, 460

# 🛠️ Model yükleme satırı dinamik yol bulucuya bağlandı:
model = load_model(kaynak_yolu("hareket_tanima_modeli.h5"))

eller = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1,
                                 min_detection_confidence=0.8,
                                 min_tracking_confidence=0.8)
cizim = mp.solutions.drawing_utils


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Komut Tanıma Sistemi")
        self.configure(bg="#0f0f0f")
        
        self.resizable(True, True) 
        self.geometry("960x560+100+100")
        self.minsize(960, 560)
        
        self.calisiyor = False
        self.sayac = 0
        self.son_hareket = ""
        self.son_calistiran = ""
        self.kamera = None
        self.koordinat_hafizasi = []
        self.icon_images = [] 
        
        self.bind("<Escape>", self.tam_ekrandan_cik) 
        
        self._arayuz_kur()

    def _arayuz_kur(self):
        BG = "#0f0f0f"
        CARD = "#1a1a1a"
        ACC = "#00e5ff"
        DIM = "#555555"
        FG = "#f0f0f0"
        
        bold14 = tkfont.Font(family="Consolas", size=14, weight="bold")
        bold11 = tkfont.Font(family="Consolas", size=11, weight="bold")
        bold16 = tkfont.Font(family="Consolas", size=16, weight="bold")
        reg10 = tkfont.Font(family="Consolas", size=10)

        self.container = tk.Frame(self, bg=BG, width=960, height=560)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.container, text="KOMUT TANIMA SİSTEMİ",
                 bg=BG, fg=FG, font=bold16).place(x=0, y=10, width=960)

        self.kamera_label = tk.Label(self.container, bg=CARD)
        self.kamera_label.place(x=16, y=50, width=CAM_W, height=CAM_H)

        panel = tk.Frame(self.container, bg=CARD)
        panel.place(x=652, y=50, width=292, height=CAM_H)

        tk.Label(panel, text="TANILAN HAREKET", bg=CARD, fg=DIM, font=reg10).place(x=16, y=14)
        self.hareket_var = tk.StringVar(value="---")
        tk.Label(panel, textvariable=self.hareket_var, bg=CARD, fg=ACC, font=bold14).place(x=16, y=34)

        tk.Label(panel, text="GÜVEN ORANI", bg=CARD, fg=DIM, font=reg10).place(x=16, y=74)
        self.guven_var = tk.StringVar(value="---")
        tk.Label(panel, textvariable=self.guven_var, bg=CARD, fg=FG, font=bold11).place(x=16, y=94)

        self.bar_canvas = tk.Canvas(panel, bg=CARD, height=8, width=260, highlightthickness=0)
        self.bar_canvas.place(x=16, y=120)
        self.bar_canvas.create_rectangle(0, 0, 260, 8, fill="#2a2a2a", outline="")
        self.bar_rect = self.bar_canvas.create_rectangle(0, 0, 0, 8, fill=ACC, outline="")

        tk.Label(panel, text="SON KOMUT", bg=CARD, fg=DIM, font=reg10).place(x=16, y=140)
        self.komut_var = tk.StringVar(value="---")
        tk.Label(panel, textvariable=self.komut_var, bg=CARD, fg="#00ff99",
                 font=bold11, wraplength=260).place(x=16, y=160)

        tk.Frame(panel, bg=DIM, height=1, width=260).place(x=16, y=195)
        tk.Label(panel, text="HAREKET LİSTESİ", bg=CARD, fg=DIM, font=reg10).place(x=16, y=205)

        y = 228
        for h, etiket in KOMUT_ETIKET.items():
            tk.Label(panel, text=EL_SEMBOL[h], bg="#2a2a2a", fg="#FFFFFF",
                     font=bold11, width=3).place(x=16, y=y)
            tk.Label(panel, text=etiket, bg=CARD, fg=FG,
                     font=reg10).place(x=58, y=y+2)
            y += 26

        self.btn_var = tk.StringVar(value="BAŞLAT")
        self.btn = tk.Button(self.container, textvariable=self.btn_var,
                             bg=ACC, fg="#000000", font=bold14,
                             relief="flat", bd=0, cursor="hand2",
                             activebackground="#00b8cc", command=self.toggle)
        self.btn.place(x=380, y=520, width=200, height=44)

        self.yardim_btn = tk.Button(self.container, text="YARDIM",
                                    bg="#2a2a2a", fg="#FFFFFF", font=reg10,
                                    relief="flat", bd=0, cursor="hand2",
                                    activebackground="#3a3a3a", command=self.yardim_pencerelesi_ac)
        self.yardim_btn.place(x=770, y=525, width=170, height=30)

    def tam_ekrandan_cik(self, event=None):
        self.state('normal')

    def yardim_pencerelesi_ac(self):
        yardim_pencere = tk.Toplevel(self)
        yardim_pencere.title("Sistem Kullanım Kılavuzu")
        yardim_pencere.geometry("580x670+300+60")
        yardim_pencere.configure(bg="#1a1a1a")
        yardim_pencere.resizable(False, False)
        yardim_pencere.transient(self)
        yardim_pencere.grab_set()

        bold_baslik = tkfont.Font(family="Consolas", size=13, weight="bold")
        normal_metin = tkfont.Font(family="Consolas", size=10)

        tk.Label(yardim_pencere, text="KOMUT TANIMA SİSTEMİ KILAVUZU", 
                 bg="#1a1a1a", fg="#ffffff", font=bold_baslik).pack(pady=10)

        metin_alani = ScrolledText(yardim_pencere, bg="#0f0f0f", fg="#f0f0f0", 
                                   font=normal_metin, wrap=tk.WORD, bd=0, height=17, highlightthickness=0)
        metin_alani.pack(padx=20, pady=5, fill=tk.X)

        kullanim_metni = (
            "SİSTEMİN İŞLEYİŞİ:\n"
            "1. 'BAŞLAT' butonuna basarak kamerayı aktif hale getirin.\n"
            "2. Elinizi kameranın görebileceği tarafa doğru konumlandırın.\n"
            "3. MediaPipe yapay zeka modülü elinizdeki 21 eklem noktasını "
            "anlık olarak tespit edecektir.\n"
            "4. Tespit edilen koordinatlar arkadaki LSTM (Derin Öğrenme) "
            "modeline gönderilir ve hareketiniz tahmin edilir.\n\n"
            "KOMUT TETİKLEME:\n"
            "- Sistem, yanlış komut çalıştırmayı önlemek için bir onay mekanizmasına "
            "sahiptir. Belirlediğiniz el hareketini bozmadan ardışık olarak "
            "kısa bir süre kameraya göstermeniz gerekir.\n"
            "- Hareket onaylandığında 'SON KOMUT' kısmında yeşil renkle belirtilir "
            "ve bilgisayarınızda ilgili işlem açılır.\n\n"
            "EN İYİ PERFORMANS İÇİN KRİTİK UYARILAR:\n"
            " IŞIK AÇISI: Odadaki ışık kaynağının elinize dik gelmesine dikkat edin.\n\n"
            " SABİT DURUŞ: Elinizi doğrudan ilgili harekete getirip kararlı sunun.\n\n"
            " TEK EL: Sistem eşzamanlı olarak tek bir eli takip etmek üzere optimize edilmiştir.\n"
        )

        metin_alani.insert(tk.END, kullanim_metni)
        metin_alani.configure(state='disabled')

        tk.Label(yardim_pencere, text="HAREKET GÖRSELLERİ", 
                 bg="#1a1a1a", fg="#ffffff", font=tkfont.Font(family="Consolas", size=11, weight="bold")).pack(pady=(12, 4))

        gorsel_cerceve = tk.Frame(yardim_pencere, bg="#1a1a1a")
        gorsel_cerceve.pack(pady=5, padx=15, fill=tk.X)

        self.icon_images = [] 
        
        for i, dosya_adi in enumerate(GORUNTU_DOSYALARI):
            # 🛠️ Görsel yolu da dinamik yol bulucuya bağlandı:
            yol = kaynak_yolu(os.path.join("icons", dosya_adi))
            
            box = tk.Frame(gorsel_cerceve, bg="#1a1a1a")
            box.pack(side=tk.LEFT, expand=True, padx=2)
            
            tk.Label(box, text=f"{i+1}-", bg="#1a1a1a", fg="#FFFFFF", font=normal_metin).pack(side=tk.TOP)
            
            if os.path.exists(yol):
                try:
                    img = Image.open(yol)
                    img = img.resize((35, 35), Image.Resampling.LANCZOS)
                    imgtk = ImageTk.PhotoImage(img)
                    self.icon_images.append(imgtk) 
                    
                    lbl_img = tk.Label(box, image=imgtk, bg="#1a1a1a")
                    lbl_img.pack(side=tk.TOP, pady=2)
                except Exception as e:
                    tk.Label(box, text="[Hata]", bg="#1a1a1a", fg="red", font=reg10).pack(side=tk.TOP)
            else:
                tk.Label(box, text="[Yok]", bg="#1a1a1a", fg="#555555", font=reg10).pack(side=tk.TOP)

        kapat_btn = tk.Button(yardim_pencere, text="Anladım, Kapat", bg="#00e5ff", fg="#000000",
                              font=bold_baslik, relief="flat", command=yardim_pencere.destroy, cursor="hand2")
        kapat_btn.pack(side=tk.BOTTOM, pady=15, width=200, height=35)

    def toggle(self):
        if self.calisiyor:
            self.calisiyor = False
            self.btn_var.set("BAŞLAT")
            self.btn.configure(bg="#00e5ff", activebackground="#00b8cc")
            if self.kamera:
                self.kamera.release()
            bos = Image.new("RGB", (CAM_W, CAM_H), (26, 26, 26))
            imgtk = ImageTk.PhotoImage(image=bos)
            self.kamera_label.imgtk = imgtk
            self.kamera_label.configure(image=imgtk)
            self.koordinat_hafizasi.clear()
        else:
            self.kamera = cv2.VideoCapture(0)
            if not self.kamera.isOpened():
                return
            self.calisiyor = True
            self.btn_var.set("DURDUR")
            self.btn.configure(bg="#ff3b3b", activebackground="#cc2a2a")
            self.sayac = 0
            self.son_hareket = ""
            self.son_calistiran = ""
            self.koordinat_hafizasi.clear()
            self.after(15, self._kamera_dongu)

    def _kamera_dongu(self):
        if not self.calisiyor:
            return

        ok, kare = self.kamera.read()
        if ok:
            kare = cv2.flip(kare, 1)
            rgb = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)
            sonuc = eller.process(rgb)

            hareket_str = "---"
            guven_val = 0.0

            if sonuc.multi_hand_landmarks:
                el = sonuc.multi_hand_landmarks[0]
                cizim.draw_landmarks(kare, el, mp.solutions.hands.HAND_CONNECTIONS)

                ham_koord = [v for n in el.landmark for v in (n.x, n.y, n.z)]
                self.koordinat_hafizasi.append(ham_koord)
                
                if len(self.koordinat_hafizasi) > 5:
                    self.koordinat_hafizasi.pop(0)
                
                stabil_koord = np.mean(self.koordinat_hafizasi, axis=0)

                tahmin = model.predict(np.array([stabil_koord]), verbose=0)
                idx = np.argmax(tahmin)
                hareket = HAREKETLER[idx]
                guven = float(tahmin[0][idx])
                guven_val = guven

                if guven > 0.95:
                    hareket_str = KOMUT_ETIKET[hareket]

                    if hareket == self.son_hareket:
                        self.sayac += 1
                    else:
                        self.sayac = 0
                        self.son_hareket = hareket
                        if self.son_calistiran != hareket:
                            self.son_calistiran = ""

                    if self.sayac == 4 and self.son_calistiran != hareket:
                        self.komut_var.set(KOMUT_ETIKET[hareket])
                        threading.Thread(target=KOMUTLAR[hareket], daemon=True).start()
                        self.son_calistiran = hareket
                        self.sayac = 0
            else:
                self.koordinat_hafizasi.clear()

            self.hareket_var.set(hareket_str)
            self.guven_var.set(f"%{int(guven_val*100)}" if guven_val > 0 else "---")
            self.bar_canvas.coords(self.bar_rect, 0, 0, int(260*guven_val), 8)

            img = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img).resize((CAM_W, CAM_H))
            imgtk = ImageTk.PhotoImage(image=img)
            self.kamera_label.imgtk = imgtk
            self.kamera_label.configure(image=imgtk)

        self.after(15, self._kamera_dongu)

    def on_close(self):
        self.calisiyor = False
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()