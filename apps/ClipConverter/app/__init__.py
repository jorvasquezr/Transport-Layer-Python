import socket
from .configuration import FORMAT,BUFFER_SIZE
import json
from colorama import init, Fore
from .ServiceVendor import ServiceVendor
IP = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDR = (IP, PORT)

def startApp():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(ADDR)
    mainThread(conn)
    print("Disconnected from the server.")
    conn.close()
    
def mainThread(conn):
    
    while True:
        data = json.loads(conn.recv(BUFFER_SIZE).decode(FORMAT))   
        if data['request'] == "DISCONNECTED":
            print(f"[SERVER]: {data['msg']}")
            break
        elif data['request'] == "OK":
            print(f"[SERVER]: {data['msg']}")
            
        elif data['request'] == "RECEIVE_FILE":
            print(ServiceVendor.receive_file(conn,data))
            continue


        commandHandler(conn,data)

def commandHandler(conn,data):
    while True:
        data = input("> ")
        data = data.split(" ")
        
        if data[0] == "":
            continue
        
        elif data[0] == "HELP":
            conn.send(json.dumps({'request':data[0]}).encode(FORMAT))
            break
        
        elif data[0] == "LOGOUT":
            conn.send(json.dumps({'request':data[0]}).encode(FORMAT))
            break
      
        elif data[0] == "LIST":
            conn.send(json.dumps({'request':data[0]}).encode(FORMAT))
            break
        
        elif data[0] == "UPLOAD":
            if(len(data)!=2):
                print(f"{Fore.RED}Wrong amount of parameters{Fore.RESET}")
            else:
                msg = ServiceVendor.send_file(conn, {'filename':data[1]})
                print(msg)
                if(msg == "File not found"):
                    continue
            break
        
        elif data[0] == "DOWNLOAD":
            if(len(data)!=2):
                print(f"{Fore.RED}Wrong amount of parameters{Fore.RESET}")
            else:
                conn.send(json.dumps({'request':data[0],'filename':data[1]}).encode(FORMAT))
            break
        
        elif data[0] == "DELETE":
            if(len(data)!=2):
                print(f"{Fore.RED}Wrong amount of parameters{Fore.RESET}")
            else:
                conn.send(json.dumps({'request':data[0],'filename':data[1]}).encode(FORMAT))
            break
        
        print(f"{Fore.RED}Unknown command{Fore.RESET}")

