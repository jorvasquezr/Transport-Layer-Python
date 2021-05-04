
from .ServiceVendor import ServiceVendor
from threading import Thread 
from .configuration import FORMAT,BUFFER_SIZE,FOLDER_PATH
import json
from datetime import datetime

from .configuration import TCP_PORT,TCP_IP, CONNECTED,DISCONNECTED
import socket 
import time
class ClientConnection(Thread):
    def __init__(self,conn,ip,port):
        Thread.__init__(self) 
        self.conn = conn
        self.connected = True
        self.port=port
        self.ip = ip
        self.start_time = 0
        self.end_time = 0 
        
        
    def run(self):
        print((CONNECTED+
            f" {self.ip}:{self.port}"
            f" {datetime.now()}")
        )  
        
        self.start_time = datetime.now()
        self.conn.sendall(json.dumps(
            {'request':'OK',
              'msg': f'Welcome to the ClipConverter server.\t Connection started at: {datetime.now()}'
            }).encode(FORMAT))
        
        while self.connected:
            stri=self.conn.recv(BUFFER_SIZE)
            stri.decode(FORMAT)
            if(stri==""):
              self.connected=False
              break
            
            data = json.loads(stri)
            data["ip"]=str(self.ip)
            data["port"]=str(self.port)
            result=self.__manageRequest(data)
            self.conn.sendall(result.encode(FORMAT))
        self.conn.close()
        print((DISCONNECTED+
            f" {self.ip}:{self.port}"
            f" {datetime.now()}")
        )
        
        
    def __manageRequest(self,data):
        result = ""
        if data['request'] == "LIST":
            result =json.dumps(
            {'request':'OK',
              'msg': ServiceVendor.listFiles()
            })    
        elif data['request'] == "DELETE":
            result =json.dumps(
            {'request':'OK',
              'msg': ServiceVendor.deleteFile(self.conn, data)
            })
        elif data['request'] == "CONVERT":
          if(data['option']=='-t'):
            result =json.dumps(
            {'request':'OK',
              'msg': ServiceVendor.convert_temp(self.conn, data)
            })
          else:
            result =json.dumps(
            {'request':'OK',
              'msg': f'file {data["idfile"]} converted to {ServiceVendor.convert_stored( data)} '
            })
            
        elif data['request'] == "FBC":
            result =json.dumps(
            {'request':'OK',
              'msg': ServiceVendor.getFilesBeingConverted()
            })
        elif data['request'] == "ST":
                  result =json.dumps(
                  {'request':'OK',
                    'msg': f"{socket.gethostbyname(socket.gethostname())}:{TCP_PORT} {datetime.now()}"
                  })
        elif data['request'] == "RECEIVE_FILE":
            result =json.dumps(
            {'request':'OK',
              'msg': ServiceVendor.receive_file(self.conn, data)
            })
        elif data['request'] == "DOWNLOAD":
            result =json.dumps(
            {'request':'OK',
              'msg': ServiceVendor.send_file(self.conn, data)
            })
            
        elif data['request'] == "EXIT":
            self.connected=False
            self.end_time=datetime.now() -self.start_time
            endconnection = datetime.now()
            result =json.dumps(
            {'request':'DISCONNECTED',
              'msg':f'Thank you! we hope you come back soon\n Connection ended at {endconnection}\n Duration:{self.end_time}'
            })
            
        elif data['request'] == "HELP":
            result =json.dumps(
            {'request':'OK',
              'msg': ServiceVendor.getHelpMsg()
            })

        return result
         




    


        


