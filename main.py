import subprocess
import os
import re
import sys
import time

try:
    import win32gui
except ImportError:
    os.system(sys.executable + " -m pip install pywin32")
    import win32gui

import win32con
import win32process


last_window_hwnd = -1

def close_window(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE)

def is_distracting_executable(hwnd):
    # Get the windows process ID
    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
    # Loop over running processes to find the one with the same process ID
    for process in get_running_processes():
        if int(process["pid"]) == process_id:
            process_executable: str = process["image"]
            print(process_executable)
            # Read file for list of distracting apps
            with open("distracting_executables.txt") as file:
                for line in file.readlines():
                    if line.strip() in process_executable:
                        print("DISTRACTING!!")
                        return True
    return False

def is_distracting_process(hwnd) -> bool:
    window_text = win32gui.GetWindowText(hwnd)

    if is_distracting_executable(hwnd): return True

    return False

def switched_window(prev_hwnd, current_hwnd):
    new_window_text = win32gui.GetWindowText(current_hwnd)
    if not new_window_text:
        return
    print(f"Switched from {win32gui.GetWindowText(prev_hwnd)} to {new_window_text}")

    if is_distracting_process(current_hwnd):
        close_window(current_hwnd)

def get_running_processes() -> list[dict]:
    tasks_output = subprocess.check_output(['tasklist']).splitlines()
    # Convert from bytes object to string for rejex and remove the b' part from the start
    tasks = [str(task)[2::] for task in tasks_output]
    processes = []
    for task in tasks:
        matches = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*",task)
        if matches is not None:
            processes.append({"image":matches.group(1), "pid":matches.group(2), "session_name":matches.group(3), "session_num":matches.group(4),"mem_usage":matches.group(5)})
    return processes


# Scan Loop
while True:
    current_window_hwnd = win32gui.GetForegroundWindow()
    if current_window_hwnd == 0 or not win32gui.GetWindowText(current_window_hwnd): continue
    if current_window_hwnd != last_window_hwnd:
        switched_window(last_window_hwnd, current_window_hwnd)
        last_window_hwnd = current_window_hwnd
    time.sleep(1)