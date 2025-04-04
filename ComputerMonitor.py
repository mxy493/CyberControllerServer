import threading
from ctypes import *
import time
import subprocess


class ComputerMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.started = False

    def monitor(self):
        self.monit_windows_lock()

    def monit_windows_lock(self):
        while True:
            process_name = 'LogonUI.exe'
            callall = 'TASKLIST'
            outputall = subprocess.check_output(callall)
            outputstringall = str(outputall)
            if process_name in outputstringall:
                print("Locked.")
                if self.callback:
                    self.callback()
            time.sleep(2)  # 可以改进

    def start(self):
        monitor_threading = threading.Thread(target=self.monitor, args=())
        monitor_threading.start()
        self.started = True
