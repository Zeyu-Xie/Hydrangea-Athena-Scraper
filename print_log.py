from datetime import datetime

from load_config import *


def print_log(msg):
    global CommandLineLog, FileLog, FileLogPath
    log = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]}] {msg}"
    if CommandLineLog:
        print(log)
    if FileLog:
        with open(FileLogPath, "a") as f:
            f.write(log + "\n")
