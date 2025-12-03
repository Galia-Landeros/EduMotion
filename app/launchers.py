# app/launchers.py
import os
import subprocess
import sys
import time


# Carpeta donde está este archivo (app/)
BASE_DIR = os.path.dirname(__file__)


def start_camera_slides():
    """
    Lanza el motor gestual SIEMPRE en modo presentación.
    Ejecuta: python [ruta_absoluta_a_camera.py]
    """
    camera_path = os.path.join(BASE_DIR, "camera.py")  # <--- OJO: solo "camera.py"
    return subprocess.Popen([sys.executable, camera_path])


def launch_ppt_via_com(ppt_path: str) -> bool:
    """Intenta abrir PowerPoint usando COM y lanzar la presentación."""
    try:
        import win32com.client
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = True
        pres = powerpoint.Presentations.Open(os.path.abspath(ppt_path), WithWindow=True)
        pres.SlideShowSettings.Run()
        return True
    except Exception:
        return False


def launch_ppt_fallback(ppt_path: str, auto_f5: bool = True):
    """Abre el PPT con os.startfile y opcionalmente manda F5 con pyautogui."""
    os.startfile(os.path.abspath(ppt_path))
    if auto_f5:
        try:
            import pyautogui
            time.sleep(2.5)
            pyautogui.press("f5")
        except Exception:
            pass
