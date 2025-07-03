# 🕹️ Gesture-Controlled Car Racing Game

Control a racing car with just your **hand gestures** using a webcam! This fun and interactive Python project combines **MediaPipe** for hand tracking, **OpenCV** for camera capture, and **Pygame** for game development.

## 📽️ Demo

https://www.linkedin.com/posts/akhilshrivas_internship-paid-unpaid-activity-7295743354502365184-3tmn?utm_source=share&utm_medium=member_desktop&rcm=ACoAADsHIGABSCTWaXhuRSsTFx1p5j8TUAbpXF0

## 🎮 Features

* Control the car's **position** using your **wrist movement**
* **Speed up** the car by moving your hand **closer** to the camera
* **Obstacle cars (police cars)** move down the road — avoid crashing!
* **Scrolling road background** for a real highway effect
* Game over screen with option to **restart** or **quit**
* Dynamic difficulty: more obstacles and faster speed as score increases

---

## 🧠 How It Works

* Uses your **wrist landmark** detected via MediaPipe to map car position on the screen
* Closer hand = more speed, giving a pseudo 3D driving feel
* Randomly spawns **police car** obstacles
* Collision with any obstacle = game over

---

## 🛠️ Technologies Used

* [Python](https://www.python.org/)
* [OpenCV](https://opencv.org/)
* [MediaPipe](https://mediapipe.dev/)
* [Pygame](https://www.pygame.org/)

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/gesture-car-racing.git
cd gesture-car-racing

# Install required libraries
pip install opencv-python mediapipe pygame
```

---

## 🖼️ Assets Required

Ensure the following image files are placed in the same directory:

* `highway.jpg` → background road image
* `car.jpg` → player's car image
* `police car.png` → obstacle car image

> You can use your own images but ensure dimensions are adjusted accordingly in the code.

---

## 🚀 Running the Game

```bash
python car_race.py
```

* **Move hand left/right** to steer
* **Move hand closer to camera** to accelerate
* Press **'Q'** to quit or **'R'** to restart after crash

---

## 💡 Future Improvements

* Add sound effects and background music
* Add score saving and leaderboard
* Introduce multiple lanes or levels
* Use other hand gestures for power-ups or shooting

---

## 📄 License

This project is licensed under the MIT License.
