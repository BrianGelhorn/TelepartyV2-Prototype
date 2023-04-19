import hashlib
from threading import Thread
import socket
import os

def compareIntegritys(hash1, hash2):
    if(hash1 == hash2):
        return True
    else:
        return False

def checkIntegrity(path):
    with open(path, 'rb') as file_to_check:
        data = file_to_check.read()
        datamd5 = hashlib.md5(data).hexdigest()
        return datamd5

def filterData(data: str, replace: str):
    return data.replace(replace, "")

def checkDataType(data: str, type: str):
    if(data.startswith(type)):
        return True
    else:
        return False

def startThread(target: object, daemon: bool = True):
    thread = Thread(target=target, daemon=daemon)
    thread.start()
    return thread

def sendDataToSocket(socket: socket.socket, data: str):
    return socket.send(data.encode("utf-8"))

def checkForDownloadedMovies(path_folder: str) -> list[tuple]:
    md5List = []
    for file in os.listdir(path_folder):
        with open(os.path.join(path_folder, file), "r") as f:
            md5List.append((checkIntegrity(f.name), f.name))
    return md5List