import os
import sys
import time
try:
    import win32gui
except ImportError:
    os.system(sys.executable + " -m pip install pywin32")
    import win32gui

import pywintypes
import win32con

last_window_hwnd = -1

def close_window(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE)
    pass

def switched_window(prev_hwnd, current_hwnd):
    new_window_text = win32gui.GetWindowText(current_hwnd)
    if not new_window_text:
        return
    print(f"Switched from {win32gui.GetWindowText(prev_hwnd)} to {new_window_text}")
    if "Feather" in new_window_text:
        close_window(current_hwnd)

while True:
    current_window_hwnd = win32gui.GetForegroundWindow()
    if current_window_hwnd == 0 or not win32gui.GetWindowText(current_window_hwnd): continue
    if current_window_hwnd != last_window_hwnd:
        switched_window(last_window_hwnd, current_window_hwnd)
        last_window_hwnd = current_window_hwnd
    time.sleep(1)
