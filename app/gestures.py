import math
from collections import deque

def fingers_up(lm):
    """
    Devuelve [pulgar, índice, medio, anular, meñique]
    1 = dedo extendido, 0 = doblado.
    """
    up = [0, 0, 0, 0, 0]

    # Pulgar: comparamos en eje X (funciona bien en modo espejo con mano derecha)
    up[0] = 1 if lm[4].x < lm[3].x else 0

    # Otros dedos: si la punta está más arriba (y menor) que la articulación intermedia
    up[1] = 1 if lm[8].y  < lm[6].y  else 0
    up[2] = 1 if lm[12].y < lm[10].y else 0
    up[3] = 1 if lm[16].y < lm[14].y else 0
    up[4] = 1 if lm[20].y < lm[18].y else 0

    return up

def pinch_distance(lm):
    """Distancia normalizada entre pulgar (4) e índice (8)."""
    ix, iy = lm[8].x, lm[8].y
    tx, ty = lm[4].x, lm[4].y
    return math.hypot(ix - tx, iy - ty)

def classify(lm, pinch_thr=0.05):
    """
    Clasifica gesto simple:
    - PINCH: pinza pulgar-índice
    - OPEN: mano abierta (4+ dedos arriba)
    - FIST: puño (0 dedos arriba)
    - NONE: nada relevante
    """
    up = fingers_up(lm)
    p = pinch_distance(lm)

    if p < pinch_thr:
        return "PINCH"
    if sum(up) >= 4:
        return "OPEN"
    if sum(up) == 0:
        return "FIST"
    return "NONE"

class GestureStabilizer:
    """
    Devuelve un gesto 'estable' solo si se repite N frames seguidos.
    Evita que parpadee entre gestos.
    """
    def __init__(self, window=4):
        self.window = window
        self.buf = deque(maxlen=window)
        self.current = "NONE"

    def update(self, raw_label):
        self.buf.append(raw_label)
        if len(self.buf) == self.window and len(set(self.buf)) == 1:
            self.current = raw_label
        return self.current
