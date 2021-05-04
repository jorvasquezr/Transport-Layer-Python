# server.py
import socket
import struct


def receive_file(sck: socket.socket, filename):
    # Leer primero del socket la cantidad de 
    # bytes que se recibirán del archivo.
    filesize = receive_file_size(sck)
    # Abrir un nuevo archivo en donde guardar
    # los datos recibidos.
    with open(filename, "wb") as f:
        received_bytes = 0
        # Recibir los datos del archivo en bloques de
        # 1024 bytes hasta llegar a la cantidad de
        # bytes total informada por el cliente.
        while received_bytes < filesize:
            chunk = sck.recv(1024)
            if chunk:
                f.write(chunk)
                received_bytes += len(chunk)

with socket.create_server(("localhost", 6190)) as server:
    print("Esperando al cliente...")
    conn, address = server.accept()
    print(f"{address[0]}:{address[1]} conectado.")
    print("Recibiendo archivo...")
    receive_file(conn, "Pruebas MultipleConexion\imagen-recibida.png")
    print(conn)
    print("Archivo recibido.")
print("Conexión cerrada.")