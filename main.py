import time
import utils

try:
    import win32gui
except ImportError:
    utils.import_lib("pywin32")
    import win32gui

import win32con
import win32process

last_window_hwnd = -1


def close_window(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE)
    utils.popup(win32gui.GetWindowText(hwnd))


def is_distracting_executable(hwnd):
    executable_name = utils.get_executable(hwnd)
    with open("distracting_executables.txt") as file:
        for line in file.readlines():
            if line.strip() in executable_name:
                return True
    return False


def is_distracting_window_title(hwnd):
    window_text = win32gui.GetWindowText(hwnd)
    with open("distracting_window_titles.txt") as file:
        for line in file.readlines():
            if line.strip() in window_text:
                return True
    return


def is_distracting_process(hwnd) -> bool:
    window_text = win32gui.GetWindowText(hwnd)

    if is_distracting_window_title(hwnd): return True
    if is_distracting_executable(hwnd): return True

    # A java window may be another process, so we need to check the window text
    # Also, a window with Minecraft in the title may not always be the game
    # If it is both a java window and has Minecraft in the title, it is likely the game
    if utils.get_executable(hwnd) == "javaw.exe":
        with open("minecraft_titles.txt") as file:
            for line in file.readlines():
                if line.strip() in window_text:
                    return True
    return False


def switched_window(prev_hwnd, current_hwnd):
    new_window_text = win32gui.GetWindowText(current_hwnd)
    if not new_window_text:
        return
    print(f"Switched from {win32gui.GetWindowText(prev_hwnd)} to {new_window_text}")

    if is_distracting_process(current_hwnd):
        close_window(current_hwnd)


# Scan Loop
while True:
    current_window_hwnd = win32gui.GetForegroundWindow()
    if current_window_hwnd == 0 or not win32gui.GetWindowText(current_window_hwnd): continue
    if current_window_hwnd != last_window_hwnd:
        switched_window(last_window_hwnd, current_window_hwnd)
        last_window_hwnd = current_window_hwnd
    time.sleep(1)
