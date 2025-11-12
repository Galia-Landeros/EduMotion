import time
from pynput.keyboard import Controller, Key

kb = Controller()
_last = 0

def _cooldown(sec=0.25):
    global _last
    now = time.time()
    if now - _last >= sec:
        _last = now
        return True
    return False

def dispatch(gesture: str, mode: str = "slides"):
    if not _cooldown():
        return

    # Dino: solo necesita SPACE con PINCH
    if mode == "dino":
        if gesture == "PINCH":
            kb.press(Key.space); kb.release(Key.space)

    # Presentaciones: OPEN=next, FIST=prev, PINCH=enter/click
    elif mode == "slides":
        if gesture == "OPEN":
            kb.press(Key.right); kb.release(Key.right)
        elif gesture == "FIST":
            kb.press(Key.left); kb.release(Key.left)
        elif gesture == "PINCH":
            kb.press(Key.enter); kb.release(Key.enter)

    # Video: PINCH play/pause, OPEN/FIST avanzar/retroceder
    elif mode == "video":
        if gesture == "PINCH":
            kb.press(Key.space); kb.release(Key.space)
        elif gesture == "OPEN":
            kb.press(Key.right); kb.release(Key.right)
        elif gesture == "FIST":
            kb.press(Key.left); kb.release(Key.left)
