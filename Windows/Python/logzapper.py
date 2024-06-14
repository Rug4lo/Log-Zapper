# Depencies
from colorama import Fore, init, Style, Back
from pathlib import Path
from pywintypes import Time
from random import getrandbits
from pywintypes import error as wintError
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

# Support functions
def getEvtx():
    # This path contains the headers of the most important file events in the winevt logs
    evtxPath= "C:\ProgramData\Microsoft\Event Viewer\ExternalLogs"
    evtxPathContent = Path(evtxPath).iterdir()

    if Path(evtxPath).is_dir():
        for file in evtxPathContent:
                yield str(file)

def checkStatus(filename:str) -> bool:
    # Verify is the file is used in a process
    try:
        file_handle = CreateFile(filename, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
        if file_handle:
            CloseHandle(file_handle)
            return False
    except wintError as e:
        if e.winerror == 32:
            return True
    return False

def getLog():
    # Filter by directories and extensions to find unknown logs
    dir_path = os.path.dirname("C:\\")

    for root, _, files in os.walk(dir_path):
        if os.path.basename(root).lower() == 'logs':
            for file in files:
                yield (os.path.join(root, file))
        for file in files:
            if file.lower().endswith('.log'):
                yield (os.path.join(root, file))

def getTS(filePath:str) -> tuple:
    # Obtain the timestamp of the files
    stat = Path(filePath).stat()

    access_time = dt.datetime.fromtimestamp(stat.st_atime_ns / 1_000_000_000).strftime(format)
    modify_time = dt.datetime.fromtimestamp(stat.st_mtime_ns / 1_000_000_000).strftime(format)
    change_time = dt.datetime.fromtimestamp(stat.st_ctime_ns / 1_000_000_000).strftime(format)

    return change_time, modify_time, access_time

def setTS(createTime:str, modifyTime:str, accessTime:str, filePath:str) -> None:
    # Configure new timestamp for the files
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

def gutmann(filePath:str) -> int:
    # First phase and patron for remove a file
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
        
    rnd = lambda : str(os.urandom(3))
    return fileSize

def overwriteCalulator(number:int):
    # Calculator for a with patrons and zeros
    if number <= 0:
        return 0, 0

    overwrite1 = round(number * 0.70)
    overwrite0 = round(number * 0.30)

    return overwrite1,overwrite0

def removeFile(filePath: str, fileSize: int, overwriteN: int=9):
    # Second phase for the file remover
    nOverWrite1, nOverWrite0 = overwriteCalulator(overwriteN)
        
    with open(filePath, "r+b") as dummy_file:
        # Overwrite the file with random patrons
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

    with open(filePath, "r+b") as dummy_file:
        # Overwrite the file with zeros
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
    # Main function
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
def main():
    # Main function with admin perms
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
    print("Make by Rug4lo & yoshl")