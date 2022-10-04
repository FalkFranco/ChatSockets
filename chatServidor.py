import socket  
import threading


host = '127.0.0.1' # localhost
port = 55555 

# Crear Socket para la red
#Se almacena el socket en la variable server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP

#Se pasan los datos de conexion al socket
server.bind((host, port)) # Se enlazaa el servidor con el host y el puerto
server.listen()
print(f"Servidor Ejecutandose en {host}:{port}")


clientes = [] # Alamcena las conexiones de los usuarios
nombreUsuarios = [] # Almacena los nombres de usuarios de los clientes

#Enviar el mensaje a todos los clientes
def broadcast(message, _client):
    for client in clientes: # Para cada cliente en la lista de clientes
        if client != _client: # No enviar el mensaje al cliente que lo envio
            client.send(message) # Enviar el mensaje 

#Funcion para manejar mensajes de cada usuario
def manejar_mensajes(cliente):
    while True:
        try: #
            # Se optiene el mensaje del cliente
            message = cliente.recv(1024) # 1024 bytes
            broadcast(message, cliente) # Se envia el mensaje a todos los clientes
        except:
            index = clientes.index(cliente) # Se obtiene el indice del cliente
            nombreUsuario = nombreUsuarios[index] # Se obtiene el nombre de usuario del cliente
            broadcast(f"ChatBot: {nombreUsuario} Desconectado".encode('utf-8'), cliente) # Se envia el mensaje de que el cliente se desconecto
            clientes.remove(cliente) # Se elimina el cliente de la lista de clientes
            nombreUsuarios.remove(nombreUsuario) # Se elimina el nombre de usuario de la lista de nombres de usuario
            cliente.close() # Se cierra la conexion del cliente
            break


#Funcion para manejar la conexion de los clientes
def recibir_conexiones(): # Se ejecuta en un hilo
    while True: 
        cliente, address = server.accept() # Se acepta la conexion del cliente

        cliente.send("@nombreUsuario".encode("utf-8")) # Se envia el mensaje para que el cliente envie su nombre de usuario
        nombreUsuario = cliente.recv(1024).decode('utf-8') # Se recibe el nombre de usuario del cliente

        clientes.append(cliente) # Se agrega el cliente a la lista de clientes
        nombreUsuarios.append(nombreUsuario) # Se agrega el nombre de usuario a la lista de nombres de usuario

        print(f"{nombreUsuario} esta conectado con {str(address)}") # Se imprime el nombre de usuario y la direccion del cliente

        message = f"ChatBot: {nombreUsuario} entró al chat!".encode("utf-8") # Se crea el mensaje de que el cliente se conecto
        broadcast(message, cliente) # Se envia el mensaje a todos los clientes
        cliente.send("Conectado al servidor".encode("utf-8")) # Se envia el mensaje de que el cliente se conecto al servidor

        thread = threading.Thread(target=manejar_mensajes, args=(cliente,)) # Se crea un hilo para manejar los mensajes del cliente
        thread.start() # Se inicia el hilo

recibir_conexiones() # Se ejecuta la funcion para manejar las conexiones de los clientes

