
import os, time, subprocess, sys

def start_camera_slides():
    args = [sys.executable, "app/camera.py"]

     
    #Lanza el motor siempre en modo presentación
    return subprocess.Popen([sys.executable, "app/camera.py"])

def launch_ppt_via_com(ppt_path: str) -> bool:
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
    os.startfile(os.path.abspath(ppt_path))
    if auto_f5:
        try:
            import pyautogui
            time.sleep(2.5)
            pyautogui.press("f5")
        except Exception:
            pass

