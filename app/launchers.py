# app/launchers.py
import os, time, subprocess, sys

def start_camera(mode="slides"):
    """Lanza el motor gestual como proceso aparte."""
    return subprocess.Popen([sys.executable, "app/camera.py", mode])

def launch_ppt_via_com(ppt_path: str) -> bool:
    """Intento robusto con COM (Windows + PowerPoint instalado)."""
    try:
        import win32com.client
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = True
        pres = powerpoint.Presentations.Open(os.path.abspath(ppt_path), WithWindow=True)
        pres.SlideShowSettings.Run()  # F5
        return True
    except Exception:
        return False

def launch_ppt_fallback(ppt_path: str, auto_f5: bool = True):
    """Fallback: abrir con OS y, si se puede, mandar F5 con pyautogui."""
    os.startfile(os.path.abspath(ppt_path))
    if auto_f5:
        try:
            import pyautogui
            time.sleep(2.5)
            pyautogui.press("f5")
        except Exception:
            pass
