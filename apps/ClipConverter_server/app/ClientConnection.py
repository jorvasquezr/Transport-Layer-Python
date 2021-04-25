
from .ServiceVendor import ServiceVendor
from threading import Thread 
from .configuration import FORMAT,BUFFER_SIZE,SERVER_DATA_PATH

class ClientConnection(Thread):
    def __init__(self,conn,ip,port):
        Thread.__init__(self) 
        self.conn = conn
        self.connected = True
        self.port=port
        self.ip = ip
        
        
    def run(self):
        self.conn.send("OK@Welcome to the ClipConverter server.".encode(FORMAT))
        while self.connected:
            data = self.conn.recv(BUFFER_SIZE).decode(FORMAT)
            data = data.split("@")
            request = data[0]
            result=self.__manageRequest(request,data)
        print(f"[DISCONNECTED] {addr} disconnected")
        self.conn.close()
        
        
    def __manageRequest(self, request,data):
        result = 0
        if request == "LIST":
            result = ServiceVendor.listFiles(self.conn, data)

        elif request == "UPLOAD":
            result = ServiceVendor.uploadFile(self.conn, data)
        

        elif request == "DELETE":
            result = ServiceVendor.deleteFile(self.conn, data)
            

        elif request == "LOGOUT":
            self.connected=false
            
        elif request == "HELP":
            data = "OK@"
            data += "LIST: List all the files from the server.\n"
            data += "UPLOAD <path>: Upload a file to the server.\n"
            data += "DELETE <filename>: Delete a file from the server.\n"
            data += "LOGOUT: Disconnect from the server.\n"
            data += "HELP: List all the commands."

            self.conn.send(data.encode(FORMAT))
        return result
         




    


        


