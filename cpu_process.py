import psutil

def get_process_percent():
    return psutil.cpu_percent(interval=1)