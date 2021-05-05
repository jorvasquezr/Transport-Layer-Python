import socket
from .configuration import FORMAT,BUFFER_SIZE,CLIENT,SERVER,ERROR,IP,PORT,ADDR,RESULT
import json
def receive(connection):
    stri=connection.recv(BUFFER_SIZE).decode(FORMAT)
    data = json.loads(stri)
    print(RESULT.format('SERVER:'+data['request'])+f"source: {IP+':'+str(PORT)} destination: {connection.getsockname()[0]+':'+str(connection.getsockname()[1])} ")    
    return data

def send(connection,dicData):
    print(RESULT.format('CLIENT:'+dicData['request'])+f"source: {connection.getsockname()[0]+':'+str(connection.getsockname()[1])} destination: {IP+':'+str(PORT)}")    
    connection.sendall(json.dumps(dicData).encode(FORMAT))