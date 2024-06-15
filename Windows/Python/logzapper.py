# Dependencies
from colorama import Fore, init, Style, Back
from pathlib import Path
from pywintypes import Time
from random import getrandbits
from pywintypes import error as wintError
import ctypes
from ctypes.wintypes import BOOL, HANDLE, LPCWSTR, DWORD
import datetime as dt
from win32file import *
from os import stat
import os
import time

try: 
    from pyuac import main_requires_admin
except:
    from os import system as s;s("pip install pyuac")

# Global variables
format = "%d.%m.%Y %H:%M:%S"

init()
fileColor=Fore.YELLOW
badFileColor=Fore.YELLOW+Back.RED
goodst=Fore.GREEN
warnst=Fore.RED
reset=Style.RESET_ALL

# Function to erase evtx logs
def clearEvtx():
    # Main Variables
    wevtapi = ctypes.WinDLL('wevtapi.dll')

    EvtClearLog = wevtapi.EvtClearLog
    EvtClearLog.argtypes = [HANDLE, LPCWSTR, LPCWSTR, DWORD]
    EvtClearLog.restype = BOOL

    EvtOpenLog = wevtapi.EvtOpenLog
    EvtOpenLog.argtypes = [HANDLE, LPCWSTR, DWORD]
    EvtOpenLog.restype = HANDLE
    
    EvtClose = wevtapi.EvtClose
    EvtClose.argtypes = [HANDLE]
    EvtClose.restype = BOOL

    NULL = None
    EVT_HANDLE = HANDLE
    EVT_LOG_READ_ACCESS = 0x1

    for logFile in ["Application", "Security", "Windows Powershell", "System", "Setup"]:
        h_log = EvtOpenLog(NULL, logFile, EVT_LOG_READ_ACCESS)
        if not h_log:
            raise ctypes.WinError(ctypes.get_last_error(), f"Failed to open log: {logFile}")
    
        success = EvtClearLog(NULL, logFile, NULL, 0)
        if not success:
            error_code = ctypes.get_last_error()
            EvtClose(h_log)
            raise ctypes.WinError(error_code, f"Failed to clear log: {logFile}")
    
        if not EvtClose(h_log):
            raise ctypes.WinError(ctypes.get_last_error(), f"Failed to close log handle: {logFile}")

        print(f"{goodst}[+]{reset} The file: {fileColor+logFile+reset} has been successfully cleared")


# Function to get headers of event logs
def getEvtx():
    evtxPath= "C:\ProgramData\Microsoft\Event Viewer\ExternalLogs"
    evtxPathContent = Path(evtxPath).iterdir()

    if Path(evtxPath).is_dir():
        for file in evtxPathContent:
                yield str(file)

# Verify is the file is used in any process
def checkStatus(filename:str) -> bool:
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
def getLog():
    dir_path = os.path.dirname("C:\\")

    for root, _, files in os.walk(dir_path):
        if os.path.basename(root).lower() == 'logs':
            for file in files:
                yield(os.path.join(root, file))
        for file in files:
            if file.lower().endswith('.log'):
                yield(os.path.join(root, file))

# Function to get timestamp of a file
def getTS(filePath:str) -> tuple:
    stat = Path(filePath).stat()

    access_time = dt.datetime.fromtimestamp(stat.st_atime_ns / 1_000_000_000).strftime(format)
    modify_time = dt.datetime.fromtimestamp(stat.st_mtime_ns / 1_000_000_000).strftime(format)
    change_time = dt.datetime.fromtimestamp(stat.st_ctime_ns / 1_000_000_000).strftime(format)

    return change_time, modify_time, access_time

# Function to set timestamp of a file
def setTS(createTime:str, modifyTime:str, accessTime:str, filePath:str) -> None:
    fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0) 
    try:
        createTime = Time(time.mktime(time.localtime(time.mktime(time.strptime(createTime,format))+0)))
        accessTime = Time(time.mktime(time.localtime(time.mktime(time.strptime(accessTime,format))+0)))
        modifyTime = Time(time.mktime(time.localtime(time.mktime(time.strptime(modifyTime,format))+0)))
    except RuntimeError as _:
        time.sleep(0.3)
        createTime = Time(time.mktime(time.localtime(time.mktime(time.strptime(createTime,format))+0)))
        accessTime = Time(time.mktime(time.localtime(time.mktime(time.strptime(accessTime,format))+0)))
        modifyTime = Time(time.mktime(time.localtime(time.mktime(time.strptime(modifyTime,format))+0)))
        
    SetFileTime(fh, createTime, accessTime, modifyTime) 
    CloseHandle(fh)

# Function to perform Gutmann method
def gutmann(filePath:str) -> int:
    fileSize=(os.stat(filePath)).st_size
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

    with open(filePath, mode='r+b') as dummy_file:
        for loop in data:
            dummy_file.seek(0)
            if len(loop) == 1:
                dummy_file.write(loop * 65536)
            else:
                dummy_file.write(loop * 21845)
        
    return fileSize

# Function to calculate the number of types of overwrites
def overwriteCalulator(number:int):
    if number <= 0:
        return 0, 0

    overwrite1 = round(number * 0.70)
    overwrite0 = round(number * 0.30)

    return overwrite1,overwrite0

# Function to erase correctly a file
def removeFile(filePath: str, fileSize: int, overwriteN: int=9):
    nOverWrite1, nOverWrite0 = overwriteCalulator(overwriteN)

              # Overwrite with random patrons
    with open(filePath, "r+b") as dummy_file:
        for n in range(nOverWrite1):
            dummy_file.truncate(0)
            dummy_file.seek(0)
            dummy_file.write(bytearray(getrandbits(8) for _ in range(fileSize)))
            
            dummy_file.seek(0)
            dummy_file.write(bytearray(0 for _ in range(fileSize)))

            dummy_file.seek(0)
            dummy_file.write(bytearray(getrandbits(8) for _ in range(fileSize)))

            dummy_file.seek(0)
            dummy_file.write(bytearray(255 for _ in range(fileSize)))

               # Overwrite the file with zeros
    with open(filePath, "r+b") as dummy_file:
        for n in range(nOverWrite0):
            dummy_file.seek(0)
            dummy_file.write(bytearray(getrandbits(8) for _ in range(fileSize)))

            dummy_file.seek(0)
            dummy_file.write(bytearray(0 for _ in range(fileSize)))
            
            dummy_file.seek(0)
            dummy_file.write(bytearray(getrandbits(8) for _ in range(fileSize)))

            dummy_file.seek(0)
            dummy_file.write(bytearray(255 for _ in range(fileSize)))     

def joiner(logFile):
    try:
        if checkStatus(logFile):
            print(f"\n{warnst}[!]{reset} Skipping {badFileColor+logFile+reset} as it is use by another process")
            return
        
        at, mt, ct = getTS(logFile)
        fileSize = gutmann(logFile)
        removeFile(logFile, fileSize, overwriteN=9)
        setTS(at,mt,at,filePath=logFile)

    except PermissionError:
        print(f"\n{warnst}[!]{reset} Skipping {badFileColor+logFile+reset} due to insufficient permissions")

@main_requires_admin
# Main function with admin perms
def main():
    clearEvtx()
                
    evtxLogs=getEvtx()
    for logFile in evtxLogs:
        joiner(logFile)
        print(f"{goodst}[+]{reset} The file: {fileColor+logFile+reset} has been successfully cleared")
        time.sleep(0.1)    
    commonLogs=getLog()
    for logFile in commonLogs:
        joiner(logFile)
        print(f"{goodst}[+]{reset} The file: {fileColor+logFile+reset} has been successfully cleared")
        time.sleep(0.2)

if __name__ == '__main__':
    main()

    print(f"{goodst}[++]{reset} Thanks for using the tool, enjoy your new free log windows")
    print("Made by Rug4lo & yoshl")
