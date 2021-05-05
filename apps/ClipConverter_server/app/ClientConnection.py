
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
        

    def getAddr(self):
      return (self.ip,self.port)
            
    def run(self):
        print((CONNECTED+
            f" {self.ip}:{self.port}"
            f" {datetime.now()}")
        )
       
        
        self.start_time = datetime.now()
        ServiceVendor.send( self.conn, self.getAddr(), {'request':'OK','msg': f'Welcome to the ClipConverter server.\t Connection started at: {datetime.now()}'})
              
              
        ServiceVendor.connections+=[self.ip+':'+str(self.port)]
        while self.connected:
            data=ServiceVendor.receive( self.conn, self.getAddr())
            if(data==None):
              break

            data["ip"]=str(self.ip)
            data["port"]=str(self.port)
            result=self.__manageRequest(data)
            ServiceVendor.send( self.conn, self.getAddr(), result)

        self.conn.close()
        if (self.ip+':'+str(self.port)) in  ServiceVendor.connections:
            ServiceVendor.connections.remove(self.ip+':'+str(self.port))
        print((DISCONNECTED+
            f" {self.ip}:{self.port}"
            f" {datetime.now()}")
        )
        
        
    def __manageRequest(self,data):
        result = ""
        if data['request'] == "LIST":
            result =(
            {'request':'OK',
              'msg': ServiceVendor.listFiles()
            })    
            
        elif data['request'] == "DELETE":
            result =(
            {'request':'OK',
              'msg': ServiceVendor.deleteFile(data)
            })
        elif data['request'] == "CONNECTIONS":
                  result =(
                  {'request':'OK',
                    'msg': "\n".join(ServiceVendor.connections)
                  })
        elif data['request'] == "CONVERT":
          if(data['option']=='-t'):
            result =(
            {'request':'OK',
              'msg': ServiceVendor.convert_temp(self.conn, data,self.getAddr())
            })
          else:
            result =(
            {'request':'OK',
              'msg': f'file {data["idfile"]} converted to {ServiceVendor.convert_stored( data)} '
            })
            
        elif data['request'] == "FBC":
            result =(
            {'request':'OK',
              'msg': ServiceVendor.getFilesBeingConverted()
            })
        elif data['request'] == "ST":
                  result =(
                  {'request':'OK',
                    'msg': f"{socket.gethostbyname(socket.gethostname())}:{TCP_PORT} {datetime.now()}"
                  })
        elif data['request'] == "RECEIVE_FILE":
            result =(
            {'request':'OK',
              'msg': ServiceVendor.receive_file(self.conn, data)
            })
        elif data['request'] == "DOWNLOAD":
            result =(
            {'request':'OK',
              'msg': ServiceVendor.send_file(self.conn, data,self.getAddr())
            })
        elif data['request'] == "DSFF":
                    result =(
                    {'request':'OK',
                      'msg': ServiceVendor.sendSupportedFormats(self.conn, self.getAddr())
                    }) 
        elif data['request'] == "EXIT":
            self.connected=False
            self.end_time=datetime.now() -self.start_time
            endconnection = datetime.now()
            result =(
            {'request':'DISCONNECTED',
              'msg':f'Thank you! we hope you come back soon\n Connection ended at {endconnection}\n Duration:{self.end_time}'
            })
            
        elif data['request'] == "HELP":
            result =(
            {'request':'OK',
              'msg': ServiceVendor.getHelpMsg()
            })

        return result
         




    


        


