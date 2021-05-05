from .configuration import BUFFER_SIZE,FORMAT,FOLDER_PATH,RESULT,TCP_PORT
import os
import json
import enum
import socket
import struct
import time 
from datetime import datetime

class ServiceVendor:
    files_being_converted={}
    connections=[]
    fileid=0
    
    
    @staticmethod
    def deleteFile(data):
        print(data)
        files = os.listdir(FOLDER_PATH)
        msg = ""
        if len(files) == 0:
            msg = "The server directory is empty"
        else:
            if str(data['idfile'])+'_'+data['filename'] in files:
                os.system(f"rm {FOLDER_PATH}/{str(data['idfile'])+'_'+data['filename']}")
                msg = "File deleted successfully."
            else:
                msg = "File not found."
        return msg

    @staticmethod
    def splitFilename(text):
        elements = text.split('_')
        filename = '_'.join(elements[1:])
        fileid = elements[0]
        return fileid + ' ' + filename
        


    @staticmethod
    def listFiles():
        files = os.listdir(FOLDER_PATH)
        msg = ""
        if len(files) == 0:
            msg += "The server directory is empty"
        else:
            msg += "\nid filename\n"
            msg += "\n".join(list(map(ServiceVendor.splitFilename,files)))
        return msg

    @staticmethod
    def getFileId(text):
        return  int(text.split('_')[0])

    
    @staticmethod
    def getNewId():
        try:
            files = os.listdir(FOLDER_PATH)
            ServiceVendor.fileid=max(list(map(ServiceVendor.getFileId,files)))+1
            return ServiceVendor.fileid
        except: 
            if ServiceVendor.fileid<len(os.listdir(FOLDER_PATH)):
                ServiceVendor.fileid = len(os.listdir(FOLDER_PATH))
            idf = ServiceVendor.fileid
            ServiceVendor.fileid+=1
            return idf
    
    @staticmethod
    def getFilesBeingConverted():
        listFBC="\nip port idfile filename extension\n"
        for key in ServiceVendor.files_being_converted:
            valor=ServiceVendor.files_being_converted.get(key)
            keyvalues=key.split(":")
            listFBC+= f"{keyvalues[0]} {keyvalues[1]} {valor[0]} {valor[1]} {valor[2]}\n"
        return listFBC
            
        
    
    
    @staticmethod
    def convert_temp(conn, data,addr):
        data["idfile"]=ServiceVendor().getNewId()
        fileStatus = ServiceVendor.receive_file(conn, data)
        
        if(fileStatus!="File received"):
            return "Error while receiving file"

        convertResult = ServiceVendor.convert_stored(data)
        if(convertResult) == "Error while converting file":
            return convertResult
        
        sendResult=ServiceVendor.send_file(conn, {"filename":convertResult,"idfile":data["idfile"]},addr)
        if(sendResult!="File sent"):
            return "Error to send file"
        try:
            ServiceVendor.deleteFile({"filename":data["filename"],"idfile":data["idfile"]})
            ServiceVendor.deleteFile({"filename":convertResult,"idfile":data["idfile"]})
        except:
            pass
        
        return "File received, converted and sent"
        
        
        
    
    @staticmethod
    def convert_stored(data):
        try:
            ServiceVendor.files_being_converted[(data["ip"]+":"+data["port"])]=[str(data["idfile"]),data["filename"],data["extension"]]
            newfilename='.'.join(data['filename'].split('.')[0:-1]) +'.'+ data['extension']
            os.system(f"ffmpeg -i {FOLDER_PATH+'/'+str(data['idfile'])+'_'+data['filename']} {FOLDER_PATH+'/'+str(data['idfile'])+'_'+newfilename}")
            ServiceVendor.files_being_converted.pop(data["ip"]+":"+data["port"])
            return newfilename
        except:
            return "Error while converting file"
    
    @staticmethod
    def receive_file( conn, data):
        if not 'idfile' in data :
            data["idfile"]=ServiceVendor().getNewId()
        with open(f"{FOLDER_PATH}/{data['idfile']}_{data['filename']}", "wb") as f:
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
    def receive(connection,addr):
        try:
            var = connection.recv(BUFFER_SIZE).decode(FORMAT)
            data = json.loads( var)
            print(RESULT.format('CLIENT:'+data['request'])+f"source: {addr[0]+':'+str(addr[1])} destination: {socket.gethostbyname(socket.gethostname())+':'+str(TCP_PORT)} ")    
            return data
        except:
            return None
    @staticmethod 
    def send(connection,addr,dicData):
        print(RESULT.format('SERVER:'+dicData['request'])+f"source: {socket.gethostbyname(socket.gethostname())+':'+str(TCP_PORT)} destination: {addr[0]+':'+str(addr[1])}")    
        connection.sendall(json.dumps(dicData).encode(FORMAT))
   
        
    @staticmethod                
    def send_file( conn, data,addr):
        filePath=f"{FOLDER_PATH}/{data['idfile']}_{data['filename']}"

        try:
            filesize = os.path.getsize(filePath)
        except:
            return "File not found"
        
        ServiceVendor.send(conn,addr, {'request':'RECEIVE_FILE','filesize':filesize,'filename':data['filename']})
        # Enviar el archivo en bloques de 1024 bytes.
        with open(filePath, "rb") as f:
            while read_bytes := f.read(1024):
                conn.sendall(read_bytes)
        return "File sent"
    
   
    @staticmethod
    def getHelpMsg():
        return ("LIST: List all the files from the server.\n"
                "UPLOAD <filename>: Upload a file to the server.\n"
                "DOWNLOAD <idfile> <filename>: Download expecific file.\n"
                "DELETE <idfile> <filename>: Delete a file from the server.\n"
                "CONVERT -s <idfile> <filename> <new extension>: convert a stored file\n"
                "CONVERT -t <filename> <new extension>: convert a temporal file\n"
                "CONNECTIONS: established connections\n"
                "ST: show server time and ip.\n"
                "FBC: List files being converted.\n"
                "EXIT: Disconnect from the server.\n"
                "HELP: List all commands.\n"
                "DSFF: Download the supported formats file"
                )
    def sendSupportedFormats(conn,addr):
        filePath=f"{FOLDER_PATH}/../supportedFormats.txt"

        try:
            filesize = os.path.getsize(filePath)
        except:
            return "File not found"
        
        ServiceVendor.send(conn,addr, {'request':'RECEIVE_FILE','filesize':filesize,'filename':'supportedFormats.txt'})
        # Enviar el archivo en bloques de 1024 bytes.
        with open(filePath, "rb") as f:
            while read_bytes := f.read(1024):
                conn.sendall(read_bytes)
        return "supported formarts file sent"
    




           