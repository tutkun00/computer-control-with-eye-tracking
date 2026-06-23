import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui as pg
import cv2
import numpy as np
import math
from time import sleep


# 1. Modeli yükle
base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1
    )
detector = vision.FaceLandmarker.create_from_options(options)

# 2. PyAutoGUI ayarları
pg.PAUSE = 0         
pg.FAILSAFE = True   

ekran_w, ekran_h = pg.size()

# 3. Göz kırpma eşiği
EAR_ESIGI = 0.25           

# 4. Click gecikmesi için sayaçlar
lcounter = 0
rcounter = 0 
lrcounter = 0

# 5. Göz hareketi için aralıklar (kamerada 0.0-1.0 arası)
X_ARALIGI = [0.4, 0.6]
Y_ARALIGI = [0.35, 0.65]  

# 6. Eski konum (başlangıçta ekranın ortası)
eski_x, eski_y = ekran_w / 2, ekran_h / 2

# 7. Mesafe hesaplama fonksiyonu (iki nokta arasındaki uzaklık)
def mesafe_hesapla(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

# 8. Eye Aspect Ratio (EAR) hesaplama fonksiyonu
def ear_hesapla(landmarks, ust1, alt1, ust2, alt2, ic, dis):
    dikey1 = mesafe_hesapla(landmarks[ust1], landmarks[alt1])
    dikey2 = mesafe_hesapla(landmarks[ust2], landmarks[alt2])
    yatay = mesafe_hesapla(landmarks[ic], landmarks[dis])
    return (dikey1 + dikey2) / (2.0 * yatay)

# 9. Click fonksiyonu
def click(type):
    global lcounter, rcounter, lrcounter
    if type == "sag":
        pg.click(button='right')
        rcounter = 0
    elif type == "sol":
        pg.click(button='left')
        lcounter = 0
    elif type == "cift":
        pg.doubleClick(button='left')
        lrcounter = 0
    sleep(0.15)    

# 10. Hareket fonksiyonu
def hareket_et(iris_x, iris_y):
    global eski_x, eski_y

    hedef_x = np.interp(iris_x, X_ARALIGI, [0, ekran_w])
    hedef_y = np.interp(iris_y, Y_ARALIGI, [0, ekran_h])

    hedef_x = np.clip(hedef_x, 0, ekran_w - 1)
    hedef_y = np.clip(hedef_y, 0, ekran_h - 1)

    dx = hedef_x - eski_x
    dy = hedef_y - eski_y
    mesafe = math.hypot(dx, dy)

    if mesafe < 15:
        return

    alpha = 0.25   
    yeni_x = eski_x * (1 - alpha) + hedef_x * alpha
    yeni_y = eski_y * (1 - alpha) + hedef_y * alpha

    if abs(yeni_x - eski_x) < 3 and abs(yeni_y - eski_y) < 3:
        return

    try:
        pg.moveTo(int(yeni_x), int(yeni_y))
        eski_x, eski_y = yeni_x, yeni_y
    except pg.FailSafeException:
        pass

# 11. MediaPipe ile yüz ve göz takibi fonksiyonu
def mediaPipe(img):
    global lcounter, rcounter, lrcounter
    h, w, _ = img.shape
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
    detection_result = detector.detect(mp_image)
    landmarks = None

    if detection_result.face_landmarks:
        landmarks = detection_result.face_landmarks[0]
        
        
        LEFT_EYE_INDICES = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        RIGHT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        
        
        for indices in [LEFT_EYE_INDICES, RIGHT_EYE_INDICES]:
            points = np.array([[int(landmarks[i].x * w), int(landmarks[i].y * h)] for i in indices], np.int32)
            cv2.polylines(img, [points], True, (255, 0, 0), 1) 

        # # Sağ göz sol ve sağ sınırları
        # x_min = min(landmarks[33].x, landmarks[133].x)
        # x_max = max(landmarks[33].x, landmarks[133].x)

        # # Sağ göz üst ve alt sınırları
        # y_min = min(landmarks[159].y, landmarks[145].y)
        # y_max = max(landmarks[159].y, landmarks[145].y)

        # riris = landmarks[473]
        # roran_x = (riris.x - x_min) / (x_max - x_min)
        # roran_y = (riris.y - y_min) / (y_max - y_min)

        # # Sol göz sol ve sağ sınırları
        # x_min = min(landmarks[362].x, landmarks[263].x)
        # x_max = max(landmarks[362].x, landmarks[263].x)

        # # Sol göz üst ve alt sınırları
        # y_min = min(landmarks[386].y, landmarks[374].y)
        # y_max = max(landmarks[386].y, landmarks[374].y)

        # liris = landmarks[468]
        # loran_x = (liris.x - x_min) / (x_max - x_min)
        # loran_y = (liris.y - y_min) / (y_max - y_min)   

        # ort_oran_x = np.clip((roran_x + loran_x) / 2.0, 0.0, 1.0)
        # ort_oran_y = np.clip((roran_y + loran_y) / 2.0, 0.0, 1.0)


        riris = landmarks[473]   # Sağ iris merkezi
        liris = landmarks[468]   # Sol iris merkezi
 
        # İki iris ortalaması → kamerada 0.0-1.0 arası
        iris_x = (riris.x + liris.x) / 2.0
        iris_y = (riris.y + liris.y) / 2.0 
       
        cv2.circle(img, (int(riris.x * w), int(riris.y * h)), 2, (0, 0, 255), -1)
        cv2.circle(img, (int(liris.x * w), int(liris.y * h)), 2, (0, 0, 255), -1)


        sol_ear = ear_hesapla(landmarks, 159, 145, 158, 153, 133, 33)
        sag_ear = ear_hesapla(landmarks, 386, 374, 385, 380, 362, 263)

        if sag_ear < EAR_ESIGI and sol_ear < EAR_ESIGI:
         if lrcounter >= 3:
            click("cift")
            cv2.putText(img, "Cift Tiklama", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)             
         else:
            lrcounter += 1
            rcounter = 0
            lcounter = 0
        elif sag_ear < EAR_ESIGI:
         if rcounter >= 3:
            click("sag")
            cv2.putText(img, "Sag Tiklama", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)             
         else:
            rcounter += 1
            lcounter = 0
            lrcounter = 0
        elif sol_ear < EAR_ESIGI:
         if lcounter >= 3:
            click("sol")
            cv2.putText(img, "Sol Tiklama", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)             
         else:
            lcounter += 1
            rcounter = 0
            lrcounter = 0
        else:
         hareket_et(iris_x, iris_y)
         lrcounter = rcounter = lcounter = 0
 
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow("Goz Takibi ile Bilgisayar Kontrolu", img_bgr)                      


# 12. Kamera açma ve ana döngü
def camera():
    cv2.namedWindow("Goz Takibi ile Bilgisayar Kontrolu", cv2.WINDOW_NORMAL)
    cap = cv2.VideoCapture(0)
    while True:
        result, img = cap.read()
        if not result:
            print("Kamera calisamadi, tekrar deneyiniz.")
            break
    
        img = cv2.flip(img, 1)      
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        mediaPipe(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break



camera()

        