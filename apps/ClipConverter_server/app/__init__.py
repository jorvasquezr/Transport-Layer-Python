import socket 
from threading import Thread 
from socketserver import ThreadingMixIn 
from .configuration import BUFFER_SIZE
from .ClientConnection import ClientConnection
from datetime import datetime
from colorama import init, Fore
TCP_IP = '0.0.0.0' 
TCP_PORT = 5000 
# Multithreaded Python server : TCP Server Socket Program Stub

def startApp():
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    tcpServer.bind((TCP_IP, TCP_PORT)) 
    threads = []
    print((f"{Fore.BLUE}[SEVER STARTED]{Fore.RESET}"
           f" {TCP_IP}:{TCP_PORT}"
           f" {datetime.now()}")) 
    while True: 
        tcpServer.listen(4) 
        (conn, (ip,port)) = tcpServer.accept()
      
        newthread = ClientConnection(conn, ip, port)
        newthread.start() 
        threads.append(newthread) 

    for t in threads: 
        t.join() 
