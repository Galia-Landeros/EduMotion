import cv2 as cv
import mediapipe as mp
import random
import time
import json
import os

from gestures import classify, GestureStabilizer

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

def run_colors_game():
    session_start = time.time()
    session_id = int(session_start)
    username = "demo_user"  # luego lo hacemos parametrizable si quieres

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )
    stab = GestureStabilizer(window=4)

    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    # Rectángulos (x1,y1,x2,y2)
    left_box  = (50, 150, 250, 350)
    right_box = (390, 150, 590, 350)

    colors = ["ROJO", "AZUL"]
    target = random.choice(colors)
    last_feedback = ""
    last_feedback_time = 0
    score = 0
    attempts = 0
    last_choice_time = 0

    def draw_ui(frame):
        # Fondo
        h, w, _ = frame.shape
        cv.rectangle(frame, (0,0), (w,70), (0,0,0), -1)
        msg = f"Elige: {target}"
        cv.putText(frame, msg, (20,45),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        # Cuadro izquierdo (ROJO)
        x1,y1,x2,y2 = left_box
        cv.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), -1)
        cv.putText(frame, "ROJO", (x1+40,y2+30),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        # Cuadro derecho (AZUL)
        x1,y1,x2,y2 = right_box
        cv.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), -1)
        cv.putText(frame, "AZUL", (x1+40,y2+30),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

        # Puntaje
        txt = f"Puntos: {score}  Intentos: {attempts}"
        cv.putText(frame, txt, (20,h-20),
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv.flip(frame, 1)
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        res = hands.process(rgb)

        draw_ui(frame)

        if res.multi_hand_landmarks:
            hand = res.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            lm = hand.landmark
            gesture_raw = classify(lm, pinch_thr=0.05)
            gesture = stab.update(gesture_raw)

            # Coordenadas del índice para saber en qué cuadro está
            ix = int(lm[8].x * frame.shape[1])
            iy = int(lm[8].y * frame.shape[0])
            cv.circle(frame, (ix, iy), 8, (0,255,255), -1)

            now = time.time()
            # Si hace PINCH sobre un cuadro, cuenta como elección
            if gesture == "PINCH" and now - last_choice_time > 0.7:
                last_choice_time = now
                attempts += 1
                chosen = None

                x1,y1,x2,y2 = left_box
                if x1 <= ix <= x2 and y1 <= iy <= y2:
                    chosen = "ROJO"
                x1,y1,x2,y2 = right_box
                if x1 <= ix <= x2 and y1 <= iy <= y2:
                    chosen = "AZUL"

                if chosen:
                    if chosen == target:
                        score += 1
                        last_feedback = "✔ Correcto"
                        last_feedback_time = now
                    else:
                        last_feedback = "✖ Incorrecto"
                        last_feedback_time = now

                    # Nuevo objetivo
                    target = random.choice(colors)

        # Mostrar feedback breve
        if last_feedback and time.time() - last_feedback_time < 0.8:
            cv.putText(frame, last_feedback, (220,120),
                       cv.FONT_HERSHEY_SIMPLEX, 1.2,
                       (0,255,0) if "✔" in last_feedback else (0,0,255), 3)

        cv.imshow("EduMotion - Colores", frame)
        if cv.waitKey(1) & 0xFF == 27:
            break

    # --- Al salir, guardar resultados ---
    duration = time.time() - session_start
    result = {
        "session_id": session_id,
        "username": username,
        "score": score,
        "attempts": attempts,
        "accuracy": (score / attempts) if attempts > 0 else 0,
        "duration_sec": round(duration, 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", "colors_sessions.json")

    # Append-style JSON
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(result)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # --- Al salir, guardar resultados ---
    duration = time.time() - session_start
    result = {
        "session_id": session_id,
        "username": username,
        "score": score,
        "attempts": attempts,
        "accuracy": (score / attempts) if attempts > 0 else 0,
        "duration_sec": round(duration, 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", "colors_sessions.json")

    # --- Al salir, guardar resultados ---
    duration = time.time() - session_start
    result = {
        "session_id": session_id,
        "username": username,
        "score": score,
        "attempts": attempts,
        "accuracy": (score / attempts) if attempts > 0 else 0,
        "duration_sec": round(duration, 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", "colors_sessions.json")

    # --- Al salir, guardar resultados ---
    duration = time.time() - session_start
    result = {
        "session_id": session_id,
        "username": username,
        "score": score,
        "attempts": attempts,
        "accuracy": (score / attempts) if attempts > 0 else 0,
        "duration_sec": round(duration, 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

     # --- Al salir, guardar resultados ---
    duration = time.time() - session_start
    result = {
        "session_id": session_id,
        "username": username,
        "score": score,
        "attempts": attempts,
        "accuracy": (score / attempts) if attempts > 0 else 0,
        "duration_sec": round(duration, 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", "colors_sessions.json")

    # Append-style JSON
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(result)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    run_colors_game()
