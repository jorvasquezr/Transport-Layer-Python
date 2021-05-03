from .configuration import BUFFER_SIZE,FORMAT,FOLDER_PATH
import os
import json
import enum
import socket
import struct


class ServiceVendor:
    @staticmethod
    def deleteFile(filename):
        files = os.listdir(FOLDER_PATH)
        msg = ""
        if len(files) == 0:
            msg = "The server directory is empty"
        else:
            if filename in files:
                os.system(f"rm {FOLDER_PATH}/{filename}")
                msg = "File deleted successfully."
            else:
                msg = "File not found."
        return msg

    
    @staticmethod
    def listFiles():
        files = os.listdir(FOLDER_PATH)
        msg = ""
        if len(files) == 0:
            msg += "The server directory is empty"
        else:
            msg += "\n".join(f for f in files)
        return msg
    
    @staticmethod
    def receive_file( conn, data):
        with open(f"{FOLDER_PATH}/{data['filename']}", "wb") as f:
            received_bytes = 0
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
        except:
            return "File not found"
        
        conn.sendall(json.dumps({'request':'RECEIVE_FILE','filesize':filesize,'filename':data['filename']}).encode(FORMAT))
        # Enviar el archivo en bloques de 1024 bytes.
        with open(filePath, "rb") as f:
            while read_bytes := f.read(1024):
                conn.sendall(read_bytes)
        return "File sent"
        
    
    @staticmethod
    def getHelpMsg():
        return ("LIST: List all the files from the server.\n"
                "UPLOAD <path>: Upload a file to the server.\n"
                "DELETE <filename>: Delete a file from the server.\n"
                "LOGOUT: Disconnect from the server.\n"
                "HELP: List all the commands.\n")


        