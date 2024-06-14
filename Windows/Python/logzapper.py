# Dependencies
from colorama import Fore, init, Style, Back
from pathlib import Path
from pywintypes import Time
from random import getrandbits
from pywintypes import error as wintError
import datetime as dt
from win32file import *
import zipfile
import requests
import subprocess
import os
import time
import sys

try:
    from pyuac import isUserAdmin, runAsAdmin
except ImportError:
    os.system("pip install pyuac")
    from pyuac import isUserAdmin, runAsAdmin

# Global variables
FORMAT = "%d.%m.%Y %H:%M:%S"

init()
FILE_COLOR = Fore.YELLOW
BAD_FILE_COLOR = Fore.YELLOW + Back.RED
GOOD_STATUS = Fore.GREEN
WARN_STATUS = Fore.RED
RESET = Style.RESET_ALL

SDELETE_URL = "https://download.sysinternals.com/files/SDelete.zip"
SDELETE_DIR = os.path.join(os.environ['TEMP'], "SDelete")
SDELETE_EXE = os.path.join(SDELETE_DIR, "sdelete.exe")

# Function to download and extract SDelete
def download_and_extract_sdelete():
    if not Path(SDELETE_EXE).is_file():
        print(f"{GOOD_STATUS}[+] Downloading SDelete...{RESET}")
        response = requests.get(SDELETE_URL)
        os.makedirs(SDELETE_DIR, exist_ok=True)
        with open(os.path.join(SDELETE_DIR, "SDelete.zip"), "wb") as file:
            file.write(response.content)

        print(f"{GOOD_STATUS}[+] Extracting SDelete...{RESET}")
        with zipfile.ZipFile(os.path.join(SDELETE_DIR, "SDelete.zip"), 'r') as zip_ref:
            zip_ref.extractall(SDELETE_DIR)

        print(f"{GOOD_STATUS}[+] SDelete is ready to use.{RESET}")

# Function to get event logs
def get_evtx():
    evtx_path = "C:\\ProgramData\\Microsoft\\Event Viewer\\ExternalLogs"
    if Path(evtx_path).is_dir():
        for file in Path(evtx_path).iterdir():
            yield str(file)

# Function to check if file is in use
def check_status(filename: str) -> bool:
    try:
        file_handle = CreateFile(filename, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
        if file_handle:
            CloseHandle(file_handle)
            return False
    except wintError as e:
        if e.winerror == 32:
            return True
    return False

# Function to get common log files
def get_log():
    dir_path = os.path.dirname("C:\\")
    for root, _, files in os.walk(dir_path):
        if os.path.basename(root).lower() == 'logs':
            for file in files:
                yield os.path.join(root, file)
        for file in files:
            if file.lower().endswith('.log'):
                yield os.path.join(root, file)

# Function to get timestamp of a file
def get_ts(file_path: str) -> tuple:
    stat = Path(file_path).stat()
    access_time = dt.datetime.fromtimestamp(stat.st_atime_ns / 1_000_000_000).strftime(FORMAT)
    modify_time = dt.datetime.fromtimestamp(stat.st_mtime_ns / 1_000_000_000).strftime(FORMAT)
    change_time = dt.datetime.fromtimestamp(stat.st_ctime_ns / 1_000_000_000).strftime(FORMAT)
    return change_time, modify_time, access_time

# Function to set timestamp of a file
def set_ts(create_time: str, modify_time: str, access_time: str, file_path: str) -> None:
    fh = CreateFile(file_path, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
    try:
        create_time = Time(time.mktime(time.strptime(create_time, FORMAT)))
        access_time = Time(time.mktime(time.strptime(access_time, FORMAT)))
        modify_time = Time(time.mktime(time.strptime(modify_time, FORMAT)))
    except RuntimeError:
        time.sleep(0.3)
        create_time = Time(time.mktime(time.strptime(create_time, FORMAT)))
        access_time = Time(time.mktime(time.strptime(access_time, FORMAT)))
        modify_time = Time(time.mktime(time.strptime(modify_time, FORMAT)))
        
    SetFileTime(fh, create_time, access_time, modify_time)
    CloseHandle(fh)

# Function to perform Gutmann method secure erase
def gutmann(file_path: str) -> None:
    file_size = (os.stat(file_path)).st_size
    rnd = lambda: os.urandom(3)
    data = [
        rnd(), rnd(), rnd(), rnd(),
        b'\x55', b'\xAA', b'\x92\x49\x24', b'\x49\x24\x92', b'\x24\x92\x49',
        b'\x00', b'\x11', b'\x22', b'\x33', b'\x44', b'\x55', b'\x66', b'\x77',
        b'\x88', b'\x99', b'\xAA', b'\xBB', b'\xCC', b'\xEE', b'\xFF',
        b'\x92\x49\x24', b'\x49\x24\x92', b'\x24\x92\x49',
        b'\x6D\x86\xD8', b'\xD6\xDB\x6D', b'\xDB\x6D\xB6',
        rnd(), rnd(), rnd(), rnd()
    ]
    with open(file_path, mode='r+b') as dummy_file:
        for loop in data:
            dummy_file.seek(0)
            if len(loop) == 1:
                dummy_file.write(loop * 65536)
            else:
                dummy_file.write(loop * 21845)

# Function to perform SDelete secure erase
def sdelete_file(file_path: str) -> None:
    command = [SDELETE_EXE, "-p", "3", "-s", file_path]  # 3 pasadas de sobrescritura con aleatorización
    subprocess.run(command, check=True)

# Function to clean event logs
def clean_event_logs() -> None:
    subprocess.run(["wevtutil", "cl", "System"], check=True)
    subprocess.run(["wevtutil", "cl", "Security"], check=True)
    subprocess.run(["wevtutil", "cl", "Application"], check=True)

# Function to choose secure erase method and perform deletion
def secure_erase(file_path: str, method: str) -> None:
    if method == 'gutmann':
        gutmann(file_path)
    elif method == 'sdelete':
        sdelete_file(file_path)

# Main function
def joiner(log_file, method='sdelete'):
    try:
        if check_status(log_file):
            print(f"\n{WARN_STATUS}[!]{RESET} Skipping {BAD_FILE_COLOR + log_file + RESET} as it is used by another process")
            return
        ct, mt, at = get_ts(log_file)
        secure_erase(log_file, method=method)
        set_ts(ct, mt, at, file_path=log_file)
    except PermissionError:
        print(f"\n{WARN_STATUS}[!]{RESET} Skipping {BAD_FILE_COLOR + log_file + RESET} due to insufficient permissions")
    except Exception as e:
        print(f"\n{WARN_STATUS}[!]{RESET} Error processing {BAD_FILE_COLOR + log_file + RESET}: {e}")

def main():
    download_and_extract_sdelete()  # Descarga y extrae SDelete

    method = ''
    while method not in ['gutmann', 'sdelete']:
        method = input(f"{Fore.CYAN}[?]{RESET} Choose the method for file deletion ({Fore.GREEN}sdelete{RESET}/{Fore.YELLOW}gutmann{RESET}): ").strip().lower()

    evtx_logs = get_evtx()
    for log_file in evtx_logs:
        joiner(log_file, method=method)
        print(f"{GOOD_STATUS}[+]{RESET} The file: {FILE_COLOR + log_file + RESET} has been securely deleted")
        time.sleep(0.1)
    
    common_logs = get_log()
    for log_file in common_logs:
        joiner(log_file, method=method)
        print(f"{GOOD_STATUS}[+]{RESET} The file: {FILE_COLOR + log_file + RESET} has been securely deleted")
        time.sleep(0.2)
    
    clean_event_logs()  # Limpiar logs de eventos al final

if __name__ == '__main__':
    if not isUserAdmin():
        print(f"{WARN_STATUS}[!] The script requires administrative privileges. Attempting to restart with admin rights...{RESET}")
        runAsAdmin()
    else:
        main()
        print(f"{GOOD_STATUS}[++]{RESET} Thanks for using the tool, enjoy your new free log windows")
        print("Made by Rug4lo & yoshl")