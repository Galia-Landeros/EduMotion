import cv2 as cv
import mediapipe as mp
import time
import sys
from gestures import classify, GestureStabilizer
from input_mapper import dispatch

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Define el modo según argumento o por defecto
MODE = "slides"
if len(sys.argv) > 1:
    MODE = sys.argv[1]  # "slides", "dino", "video"

print("EduMotion mode:", MODE)

def run():
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

    prev = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv.flip(frame, 1)
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        res = hands.process(rgb)

        raw_label = "NONE"
        stable_label = "NONE"

        if res.multi_hand_landmarks:
            hand = res.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            lm = hand.landmark
            raw_label = classify(lm, pinch_thr=0.05)
            stable_label = stab.update(raw_label)

            if stable_label != "NONE":
                dispatch(stable_label, MODE)

        now = time.time()
        fps = 1.0 / (now - prev) if prev else 0
        prev = now

        cv.putText(frame, f"MODE: {MODE}", (10, 25),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv.putText(frame, f"RAW: {raw_label}", (10, 50),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
        cv.putText(frame, f"STABLE: {stable_label}", (10, 75),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

        cv.imshow("EduMotion - Gestures", frame)
        if cv.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    run()

