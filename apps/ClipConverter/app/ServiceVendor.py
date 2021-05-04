from .configuration import BUFFER_SIZE,FORMAT,FOLDER_PATH
import os
import json
import enum
import socket
import struct


class ServiceVendor:
    @staticmethod
    def receive_file( conn, data):
        with open(f"{FOLDER_PATH}/{data['filename']}", "wb") as f:
            received_bytes = 0
            print(data['filesize'])
            while received_bytes < data['filesize'] :
                if(data['filesize']-received_bytes <BUFFER_SIZE):
                    chunk = conn.recv(data['filesize']-received_bytes)
                else:
                    chunk = conn.recv(BUFFER_SIZE)
                    
                if chunk:
                    f.write(chunk)
                    received_bytes += len(chunk)
        return "File received"
    
    @staticmethod                
    def send_file( conn, data):
        filePath=f"{FOLDER_PATH}/{data['filename']}"
        try:
            filesize = os.path.getsize(filePath)
            data["filesize"]=filesize
        except:
            return "File not found"
        conn.sendall(json.dumps(data).encode(FORMAT))
        # Enviar el archivo en bloques de 1024 bytes.
        with open(filePath, "rb") as f:
            while read_bytes := f.read(1024):
                conn.sendall(read_bytes)
        return "File sent"