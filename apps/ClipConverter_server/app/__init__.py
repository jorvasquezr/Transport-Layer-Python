import socket 
from threading import Thread 
from socketserver import ThreadingMixIn 
from .configuration import BUFFER_SIZE,TCP_IP,TCP_PORT,SERVERSTATED
from .ClientConnection import ClientConnection
from datetime import datetime
# Multithreaded Python server : TCP Server Socket Program Stub

def startApp():
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    tcpServer.bind((TCP_IP, TCP_PORT)) 
    threads = []
    print((SERVERSTATED+
           f" {socket.gethostbyname(socket.gethostname())}:{TCP_PORT}"
           f" {datetime.now()}")) 
    while True: 
        

        tcpServer.listen(10)

        (conn, (ip,port)) = tcpServer.accept()
        
      
        newthread = ClientConnection(conn, ip, port)
        newthread.start() 
        threads.append(newthread) 

    for t in threads: 
        t.join() 
