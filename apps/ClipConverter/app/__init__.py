import socket
from .configuration import FORMAT,BUFFER_SIZE,CLIENT,SERVER,ERROR,IP,PORT,ADDR
import json
from .ServiceVendor import ServiceVendor
from .connectionServices import receive,send


def startApp():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(ADDR)

    mainThread(conn)
    conn.close()
    
def mainThread(conn):
    
    while True:
        data = receive(conn) 
        if data['request'] == "DISCONNECTED":
            print(f"{SERVER}{data['msg']}")
            break 
        elif data['request'] == "OK":
            print(f"{SERVER}{data['msg']}")
            
        elif data['request'] == "RECEIVE_FILE":
            print(CLIENT+ServiceVendor.receive_file(conn,data))
            continue


        commandHandler(conn,data)

def commandHandler(conn,data):
    while True:
        data = input(CLIENT)
        data = data.split(" ")
        
        if data[0] == "":
            continue
        
        elif data[0] in ["HELP","FBC","ST","CONNECTIONS","EXIT","LIST","DSFF"]:
            send(conn,{'request':data[0]}) 
            break

        
        elif data[0] == "CONVERT":
            if(len(data)<2):
                print(f"{ERROR} Wrong amount of parameters ")
            else:
                if(data[1]=="-s"):
                    if(len(data)!=5):
                        print(f"{ERROR} Wrong amount of parameters ")
                    else:
                        send(conn,{'request':data[0],'option':data[1],'idfile':data[2],'filename':data[3],'extension':data[4]}) 
                        break

                        
                if(data[1]=="-t"):
                    if(len(data)!=4):
                        print(f"{ERROR} Wrong amount of parameters ")
                    else:
                        msg = ServiceVendor.send_file(conn, {'request':data[0],'option':data[1],'filesize':0,'filename':data[2],'extension':data[3]})
                        if(msg != "File not found"):
                            break
            continue

        
        elif data[0] == "UPLOAD":
            if(len(data)!=2):
                print(f"{ERROR} Wrong amount of parameters ")
            else:
                msg = ServiceVendor.send_file(conn, {'request':'RECEIVE_FILE','filesize':0,'filename':data[1]})
                if(msg != "File not found"):
                    break
            continue
        
        elif data[0] == "DOWNLOAD":
            if(len(data)!=3):
                print(f"{ERROR}Wrong amount of parameters")
            else:
                send(conn,{'request':data[0],'idfile':data[1],'filename':data[2]}) 
                break
            continue
        
        elif data[0] == "DELETE":
            if(len(data)!=3):
                print(f"{ERROR}Wrong amount of parameters ")
            else:
                send(conn,{'request':data[0],'idfile':data[1],'filename':data[2]})
                break
            continue
        
        print(ERROR+"Unknown command")

