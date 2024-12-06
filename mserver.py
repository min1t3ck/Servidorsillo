import socket
import threading

def clientthread(conn, addr):
    #conn.send(bytes(f"Bienvenido {addr}", 'utf-8'))
    conn.send(bytes('Bienvenido'),'utf-8')
    while True:
        try:
            message = conn.recv(BUFFER_SIZE).decode('utf-8')
            if message:
                msj = message
                if msj.startswith('<name>'):
                    nombresillo = str(msj.removeprefix('<name>'))
                    conn.send(bytes(nombresillo,'utf-8'))
                print(f"<{addr[0]}> {message}")
                # Reenviamos el mensaje recibido a todos los demás clientes.
                message_to_send = f"<{addr[0]}> {message}"
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            break

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(bytes(message, 'utf-8'))
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

if __name__ == "__main__":
    host = '0.0.0.0'  # Esta función nos da el nombre de la máquina
    port = 80
    BUFFER_SIZE = 1024  # Usamos un número pequeño para tener una respuesta rápida
    # Creamos un socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# AF_INET indica que se usarán direcciones IPv4; SOCK_STREAM indica protocolo TCP
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # .setsockopt() Indica que se configurará una opcion especifa del soket:
    # SOL_SOCKET indica que será modificado algo a nivel de sistema operativo.
    #SO_REUSEADDR es la opccion a modificar y hace referencia a la reutilizacion de direcciones y puertos (especialmente útil en servidores)
    # 1 es para habilitar que sí quieres reutilizar puertos y direcciones
    server.bind((host, port))#  .blind idica a quieén estará escuchando y el puerto por el que lo hará
    server.listen(100)  # Escuchamos hasta 100 clientes
    list_of_clients = []  # Lista de clientes conectados
    print(f"Escuchando conexiones en: {(host, port)}")
    try:
        while True:
            conn, addr = server.accept()  #     Espera a una conexion entrante
            #conn Representa un obejto soket
            #addr es una tupla contiene (host, puerto)
            #retorna en una tupla la direccion de la conexión del cliente
            list_of_clients.append(conn)  #     Agregamos a la lista de clientes
            print(f"Cliente conectado: {addr}")
            # Creamos y ejecutamos el hilo para atender al cliente
            threading.Thread(target=clientthread, args=(conn, addr)).start() # Método estático (no requiere de una instancia para ser invocado. o si puede ser instanciado)
            #Threading es la biblioteca para creación de hilos de pyton NOO de pyQT
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        conn.close()
        server.close()   
    print("Conexión terminada.")
