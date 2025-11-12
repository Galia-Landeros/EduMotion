import time
from pynput.keyboard import Controller, Key

kb = Controller()

print("Tienes 5 segundos para ir a la ventana del Dino o una presentación...")
time.sleep(5)

print("Enviando SPACE")
kb.press(Key.space)
kb.release(Key.space)

print("Enviando RIGHT")
time.sleep(1)
kb.press(Key.right)
kb.release(Key.right)

print("Listo.")
