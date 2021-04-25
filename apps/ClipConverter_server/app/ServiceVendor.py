from .configuration import *
import os
import json
import enum

class Result(enum.Enum):
   SUCCESS = 0
   FAILURE = 1

class ServiceVendor:
    @staticmethod
    def deleteFile(self,conn,data):
        try:
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]
            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}")
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            self.__conn.send(send_data.encode(FORMAT))
            return Result.SUCCESS
        except:
            return Result.FAILURE
    
    @staticmethod
    def uploadFile(self,conn, data): 
        try:
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            with open(filepath, "w") as f:
                f.write(text)

            send_data = "OK@File uploaded successfully."
            self.__conn.send(send_data.encode(FORMAT))
            return Result.SUCCESS
        except:
            return Result.FAILURE
    
    @staticmethod
    def listFiles(self,conn, data):
        try:
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            self.__conn.send(send_data.encode(FORMAT))
            return Result.SUCCESS
        except:
            return Result.FAILURE


    