# app/input_mapper.py
import time
from pynput.keyboard import Controller, Key

kb = Controller()
_last = 0

def _cooldown(sec=0.8):  # antes 0.25
    global _last
    now = time.time()
    if now - _last >= sec:
        _last = now
        return True
    return False

def dispatch(gesture: str, mode: str = "slides"):
    """
    Gestos:
      - OPEN  -> Right (siguiente diapositiva)
      - FIST  -> Left (anterior)
      - PINCH -> Enter (animaciones/hipervínculos)
    """
    if not _cooldown():
        return

    if gesture == "OPEN":
        kb.press(Key.right); kb.release(Key.right)
    elif gesture == "FIST":
        kb.press(Key.left); kb.release(Key.left)
    elif gesture == "PINCH":
        kb.press(Key.enter); kb.release(Key.enter)

