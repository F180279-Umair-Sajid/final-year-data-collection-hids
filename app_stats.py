import time
import psutil
import win32gui
import statistics
import ctypes


class AppStats:
    def __init__(self):
        self.current_app = ""
        self.penultimate_app = "-"
        self.current_app_foreground_time = 0
        self.current_app_processes = []

    def update(self):
        # Get the active processes and their executable names
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info['name']
                if name not in processes:
                    processes.append(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Calculate the number of active applications
        active_apps_count = len(processes)

        # Calculate the average number of processes for the current app
        current_app_average_processes = statistics.mean(self.current_app_processes) if self.current_app_processes else 0

        # Calculate the standard deviation of the number of processes for the current app
        current_app_stddev_processes = statistics.stdev(self.current_app_processes) if len(
            self.current_app_processes) > 1 else 0

        # Get the executable name of the current foreground window
        hwnd = win32gui.GetForegroundWindow()
        GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
        pid = ctypes.c_ulong()
        GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        pid = pid.value
        try:
            current_app = psutil.Process(pid).name()
        except psutil.NoSuchProcess:
            current_app = ""

        # Update the current app foreground time
        current_time = time.time()
        if current_app == self.current_app:
            self.current_app_foreground_time += current_time - self.last_time
        else:
            # Update the penultimate app and reset the current app foreground time and process list
            if self.current_app:
                self.penultimate_app = self.current_app
            self.current_app = current_app
            self.current_app_foreground_time = 0
            self.current_app_processes = []
        # Update the current app process list
        self.current_app_processes.append(len(psutil.Process(pid).children()))

        # Update the last time
        self.last_time = current_time

        return active_apps_count, self.current_app, self.penultimate_app, self.current_app_foreground_time, current_app_average_processes, current_app_stddev_processes
