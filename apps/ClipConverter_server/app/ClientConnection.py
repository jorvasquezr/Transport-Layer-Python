
from .ServiceVendor import ServiceVendor
from threading import Thread 
from .configuration import FORMAT,BUFFER_SIZE,FOLDER_PATH
import json
from datetime import datetime
from colorama import init, Fore
from .configuration import TCP_PORT,TCP_IP
import socket 
class ClientConnection(Thread):
    def __init__(self,conn,ip,port):
        Thread.__init__(self) 
        self.conn = conn
        self.connected = True
        self.port=port
        self.ip = ip
        
        
    def run(self):
        print((f"{Fore.GREEN}[CONNECTED]{Fore.RESET}"
            f" {self.ip}:{self.port}"
            f" {datetime.now()}")
        )  
          
        self.conn.sendall(json.dumps(
            {'request':'OK',
              'msg': 'Welcome to the ClipConverter server.'
            }).encode(FORMAT))
        
        while self.connected:
            stri=self.conn.recv(BUFFER_SIZE).decode(FORMAT)
            if(stri==""):
              self.connected=False
              break
            data = json.loads(stri)
            data["ip"]=str(self.ip)
            data["port"]=str(self.port)
            result=self.__manageRequest(data)
            self.conn.sendall(result.encode(FORMAT))
        self.conn.close()
        print((f"{Fore.RED}[DISCONNECTED]{Fore.RESET}"
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
            result =json.dumps(
            {'request':'OK',
              'msg': ServiceVendor.onlyConvert(self.conn, data)
            })
        elif data['request'] == "STATUS":
            result =json.dumps(
            {'request':'OK',
              'msg': ServiceVendor.getStatus(data)
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
            result =json.dumps(
            {'request':'DISCONNECTED',
              'msg':'Thank you! we hope you come back soon'
            })
            
        elif data['request'] == "HELP":
            result =json.dumps(
            {'request':'OK',
              'msg': ServiceVendor.getHelpMsg()
            })

        return result
         




    


        


