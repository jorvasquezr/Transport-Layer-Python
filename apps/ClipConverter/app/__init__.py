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
        
        elif data[0] == "FBC":
            conn.send(json.dumps({'request':data[0]}).encode(FORMAT))
            break
        elif data[0] == "ST":
            conn.send(json.dumps({'request':data[0]}).encode(FORMAT))
            break
        
        elif data[0] == "EXIT":
            conn.send(json.dumps({'request':data[0]}).encode(FORMAT))
            break
      
        elif data[0] == "LIST":
            conn.send(json.dumps({'request':data[0]}).encode(FORMAT))
            break
        
        elif data[0] == "CONVERT":
            if(len(data)<2):
                print(f"{Fore.RED}Wrong amount of parameters{Fore.RESET}")
            else:
                if(data[1]=="-s"):
                    if(len(data)!=5):
                        print(f"{Fore.RED}Wrong amount of parameters{Fore.RESET}")
                    else:
                        conn.send(json.dumps({'request':data[0],'option':data[1],'idfile':data[2],'filename':data[3],'extension':data[4]}).encode(FORMAT))
                        break

                        
                if(data[1]=="-t"):
                    if(len(data)!=4):
                        print(f"{Fore.RED}Wrong amount of parameters{Fore.RESET}")
                    else:
                        msg = ServiceVendor.send_file(conn, {'request':data[0],'option':data[1],'filesize':0,'filename':data[2],'extension':data[3]})
                        if(msg != "File not found"):
                            break
            continue

        
        elif data[0] == "UPLOAD":
            if(len(data)!=2):
                print(f"{Fore.RED}Wrong amount of parameters{Fore.RESET}")
            else:
                msg = ServiceVendor.send_file(conn, {'request':'RECEIVE_FILE','filesize':0,'filename':data[1]})
                if(msg != "File not found"):
                    break
            continue
        
        elif data[0] == "DOWNLOAD":
            if(len(data)!=3):
                print(f"{Fore.RED}Wrong amount of parameters{Fore.RESET}")
            else:
                conn.send(json.dumps({'request':data[0],'idfile':data[1],'filename':data[2]}).encode(FORMAT))
                break
            continue
        
        elif data[0] == "DELETE":
            if(len(data)!=2):
                print(f"{Fore.RED}Wrong amount of parameters{Fore.RESET}")
            else:
                conn.send(json.dumps({'request':data[0],'filename':data[1]}).encode(FORMAT))
                break
            continue
        
        print(f"{Fore.RED}Unknown command{Fore.RESET}")

