import cv2
import mediapipe as mp
import pygame
import random

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture-Controlled Car Racing")

# Load background (highway)
road_img = pygame.image.load("highway.jpg").convert()
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# Load player car image
car_img = pygame.image.load("car.jpg").convert_alpha()
car_width, car_height = 60, 100
car_img = pygame.transform.scale(car_img, (car_width, car_height))

# Load police car (obstacle)
police_car_img = pygame.image.load("police car.png").convert_alpha()
police_car_width, police_car_height = 60, 100
police_car_img = pygame.transform.scale(police_car_img, (police_car_width, police_car_height))

# Game variables
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - 150
obstacle_speed = 5
obstacles = []
speed_factor = 1
score = 0
road_y = 0  # For scrolling effect

# Camera Setup
cap = cv2.VideoCapture(0)

def detect_hand_landmarks(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            return hand_landmarks
    return None

def get_hand_position(landmarks, width, height):
    x = int(landmarks.landmark[mp_hands.HandLandmark.WRIST].x * width)
    y = int(landmarks.landmark[mp_hands.HandLandmark.WRIST].y * height)
    return x, y

def spawn_obstacle():
    x = random.randint(100, WIDTH - 100)
    y = -random.randint(50, 200 - min(score, 100))  # Reducing gap as score increases
    return {"rect": pygame.Rect(x, y, police_car_width, police_car_height), "img": police_car_img}

def show_game_over_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 50))
    screen.blit(restart_text, (WIDTH//2 - 200, HEIGHT//2))
    pygame.display.update()

def reset_game():
    global car_x, car_y, obstacles, score, speed_factor, obstacle_speed
    car_x = WIDTH // 2 - car_width // 2
    car_y = HEIGHT - 150
    obstacles.clear()
    for _ in range(3):
        obstacles.append(spawn_obstacle())
    score = 0
    speed_factor = 1
    obstacle_speed = 5  # Reset speed

# Spawn initial obstacles
for _ in range(3):
    obstacles.append(spawn_obstacle())

running = True
while running:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # Detect hand and get position
    hand_landmarks = detect_hand_landmarks(frame)
    if hand_landmarks:
        hand_x, hand_y = get_hand_position(hand_landmarks, width, height)
        car_x = int((hand_x / width) * WIDTH) - car_width // 2
        speed_factor = 1 + ((height - hand_y) / height) * 2  # Closer hand increases speed

    # **Increase Difficulty Over Time**
    obstacle_speed = 5 + (score // 5)  # Speed increases every 5 points
    if score % 10 == 0 and len(obstacles) < 10:  # Spawn more obstacles gradually
        obstacles.append(spawn_obstacle())

    # Scroll road effect
    road_y += int(obstacle_speed * speed_factor)
    if road_y >= HEIGHT:
        road_y = 0

    # Update obstacles
    for obs in obstacles:
        obs["rect"].y += int(obstacle_speed * speed_factor)
        if obs["rect"].y > HEIGHT:
            obstacles.remove(obs)
            obstacles.append(spawn_obstacle())
            score += 1  # Increase score

    # Collision detection
    car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    for obs in obstacles:
        if car_rect.colliderect(obs["rect"]):
            show_game_over_screen()
            waiting = True
            while waiting:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                cv2.imshow("Hand Tracking", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    running = False
                    waiting = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                            waiting = False
                        if event.key == pygame.K_q:
                            running = False
                            waiting = False

    # Draw game elements
    screen.blit(road_img, (0, road_y))
    screen.blit(road_img, (0, road_y - HEIGHT))  # Looping effect

    # Draw police car obstacles
    for obs in obstacles:
        screen.blit(obs["img"], (obs["rect"].x, obs["rect"].y))

    # Draw player car
    screen.blit(car_img, (car_x, car_y))

    pygame.display.update()

    # Display camera feed
    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()
