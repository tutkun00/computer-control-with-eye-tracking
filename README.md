# Göz Takibi ile Bilgisayar Kontrolü

Webcam ve yüz landmark tespiti kullanarak **gözlerinizle fare imlecini hareket ettirip tıklama yapabileceğiniz** bir erişilebilirlik aracı.

---

## Ne Yapar?

Bilgisayar kamerasından aldığı görüntüyü gerçek zamanlı olarak analiz eder. Gözlerinizin nereye baktığını ve göz kırpma hareketlerinizi algılayarak fareyi klavye veya fiziksel temas olmadan kontrol etmenizi sağlar.

| Hareket | Eylem |
|---------|-------|
| Gözleri sola/sağa/yukarı/aşağı yönlendirme | İmleç hareketi |
| Sol göz kırpma (3 kare boyunca) | Sol tık |
| Sağ göz kırpma (3 kare boyunca) | Sağ tık |
| Her iki göz birden kırpma (3 kare boyunca) | Çift tık |

---

## Nasıl Çalışır?

**1. Yüz Landmarkları — MediaPipe FaceLandmarker**

Google'ın MediaPipe kütüphanesi, yüzdeki 478 noktayı milisaniyeler içinde tespit eder. Bu noktalardan iris merkezi (landmark 468 ve 473) ile göz kenar noktaları kullanılır.

**2. İmleç Hareketi — İris Takibi**

Her iki gözün iris merkezi koordinatlarının ortalaması alınır. Bu koordinat, `X_ARALIGI = [0.4, 0.6]` ve `Y_ARALIGI = [0.35, 0.65]` aralıklarına göre ekran çözünürlüğüne haritalanır. Titremeyi önlemek için **üstel hareketli ortalama (alpha=0.25)** uygulanır; 15 pikselin altındaki mikro hareketler yok sayılır.

**3. Tıklama Tespiti — EAR (Eye Aspect Ratio)**

Göz açıklığı matematiksel olarak ölçülür:

```
EAR = (dikey_mesafe_1 + dikey_mesafe_2) / (2 × yatay_mesafe)
```

EAR değeri belirlenen eşiğin (`EAR_ESIGI = 0.25`) altına düştüğünde göz kapalı kabul edilir. Yanlışlıkla tetiklemeyi önlemek için **3 ardışık kare** boyunca kapalı kalması gerekir.

---

## Gereksinimler

```bash
pip install mediapipe opencv-python pyautogui numpy
```

Ayrıca MediaPipe'ın yüz landmark modelini indirip aynı dizine koymanız gerekiyor:

```bash
# face_landmarker.task dosyasını indirin
wget https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
```

---

## Kullanım

```bash
python eyecatch.py
```

- Kamera açılır ve yüzünüzü algılamaya başlar.
- Gözlerinizi ekranın farklı bölgelerine yönlendirerek imleci hareket ettirin.
- Çıkmak için `Q` tuşuna basın.

> **Not:** Yanlışlıkla köşeye gitmemek için `FAILSAFE = True` aktiftir. İmleci ekranın sol üst köşesine götürürseniz program otomatik durur.

---

## Ayarlar

`eyecatch.py` içindeki bu değerleri ortamınıza göre düzenleyebilirsiniz:

| Değişken | Varsayılan | Açıklama |
|----------|-----------|----------|
| `EAR_ESIGI` | `0.25` | Göz kırpma hassasiyeti — düşürünce daha kolay tetiklenir |
| `X_ARALIGI` | `[0.4, 0.6]` | Yatay göz hareketi aralığı |
| `Y_ARALIGI` | `[0.35, 0.65]` | Dikey göz hareketi aralığı |
| `alpha` | `0.25` | İmleç yumuşatma katsayısı — artırınca daha hızlı, azaltınca daha akıcı |

---

## Kısıtlar

- İyi aydınlatma şart; karanlık ortamda iris tespiti bozulur.
- Gözlük veya lens kullanımı hassasiyeti düşürebilir.


### English ------------------------



# Eye Tracking for Computer Control

An accessibility tool that lets you **move the mouse cursor and click with your eyes** using webcam and facial landmark detection.

---

## What it Does?

It analyzes the image it receives from the computer camera in real time. By detecting where your eyes are looking and your blinking movements, it allows you to control the mouse without a keyboard or physical contact.

| Movement | Action |
|---------|-------|
| Eye movement (left/right/up/down) | Cursor movement |
| Left blink (for 3 frames) | Left click |
| Right blink (for 3 frames) | Right click |

| Blinking both eyes (for 3 frames) | Double click |

---

## How it Works?

**1. Facial Landmarks — MediaPipe FaceLandmarker**

Google's MediaPipe library detects 478 points on the face in milliseconds. The iris center (landmarks 468 and 473) and the eye edge points are used from these points.

**2. Cursor Movement — Iris Tracking**

The average of the iris center coordinates of both eyes is taken. This coordinate is mapped to the screen resolution according to the ranges `X_RANGE = [0.4, 0.6]` and `Y_RANGE = [0.35, 0.65]`. **Exponential moving average (alpha=0.25)** is applied to prevent flickering; micro-movements below 15 pixels are ignored.

**3. Click Detection — EAR (Eye Aspect Ratio)**

Eye aspect ratio is measured mathematically:

```
EAR = (vertical_distance_1 + vertical_distance_2) / (2 × horizontal_distance)
```

When the EAR value falls below the defined threshold (`EAR_THRESHOLD = 0.25`), the eye is considered closed. It must remain closed for **3 consecutive squares** to prevent accidental triggering.

---

## Requirements

```bash
pip install mediapipe opencv-python pyautogui numpy
```

You also need to download MediaPipe's face landmark model and place it in the same directory:

```bash
# Download face_landmarker.task
wget https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
```

---

## Usage

```bash
python eyecatch.py
```

- The camera opens and starts detecting your face. - Move the cursor by directing your eyes to different areas of the screen. - Press `Q` to exit.

> **Note:** To avoid accidentally going to the corner, `FAILSAFE = True` is active. If you move the cursor to the top left corner of the screen, the program will stop automatically.

---

## Settings

You can adjust these values ​​in `eyecatch.py` according to your environment:

| Variable | Default | Description |
|----------|-----------|----------|
| `EAR_REST` | `0.25` | Blink sensitivity — easier to trigger when reduced |
| `X_RANGE` | `[0.4, 0.6]` | Horizontal eye movement range |
| `Y_RANGE` | `[0.35, 0.65]` | Vertical eye movement range |
| `alpha` | `0.25` | Cursor smoothing coefficient — faster when increased, smoother when decreased |

---

## Constraints

- Good lighting is essential; iris detection is impaired in dark environments. - Wearing glasses or contact lenses may reduce sensitivity.
