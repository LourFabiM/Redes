#importamos el modulo socket
import socket
import sys

arglen=len(sys.argv)
if arglen<2:
    print('python udp_cliente.py <Puerto>')
    exit()

puerto=int(sys.argv[1])
historial = open('historial_echo.txt', 'a')

#instanciamos un objeto para trabajar con el socket, stream es para tcp y se refiere a una cadena de caraceres
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Con el metodo bind le indicamos que puerto debe escuchar y de que servidor esperar conexiones
#Es mejor dejarlo en blanco para recibir conexiones externas si es nuestro caso
servidor.bind(("", puerto))

#Aceptamos conexiones entrantes con el metodo listen, y ademas aplicamos como parametro
#El numero de conexiones entrantes que vamos a aceptar
servidor.listen(1)

# Esperando conexion
print >>sys.stderr, 'Esperando para conectarse'
cliente, cliente_addr = servidor.accept()

'''
Instanciamos un objeto cliente (socket cliente) para recibir datos, al recibir datos este
devolvera tambien un objeto 'cliente_addr' que representa una tupla con los datos de conexion: IP y puerto
El metodo accept() nos devuelve una conexion abierta entre el servidor y el cliente,
junto con la direccion del cliente. Los datos de la conexion se leen con el metodo recv()
y se transmiten con el metodo sendall().
'''

try:
    print >>sys.stderr, 'conexion desde', cliente_addr
    historial.write('IP: '+ cliente_addr[0] + ' Puerto: ' + str(cliente_addr[1]) +' Data: \n')


    # Recibe los datos en trozos y reetransmite
    while True:
        #con el metodo recv recibimos datos y como parametro
        #la cantidad de bytes para recibir
        recibido = cliente.recv(1024)
        print >>sys.stderr, 'recibido "%s"' % (recibido)
        historial.write(recibido + '\n')


        if recibido:
            if recibido.upper() == 'CERRAR':
                cliente.sendall('Cerrando la conexion')
                break

            print >>sys.stderr, 'Enviando mensaje de vuelta al cliente'
            cliente.sendall(recibido)

            #si el cliente envia cerrar se cierra la conecion

        else:
            print >>sys.stderr, 'No hay mas datos', cliente_addr
            break

finally:
    # Cerrando conexion y el historial
    print >>sys.stderr, 'Cerrando la conexion'
    historial.close()
    cliente.close()
