import subprocess
import re
import sys
import os

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

def import_lib(library: str):
    os.system(sys.executable + " -m pip3 install " + library)