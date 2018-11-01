#importamos el modulo para trabajar con sockets
import socket
import sys


arglen=len(sys.argv)
if arglen<3:
    print('python udp_cliente.py <IP> <Puerto>')
    exit()

addr=sys.argv[1]
port=int(sys.argv[2])

#Creamos un objeto socket para el servidor. Podemos dejarlo sin parametros pero si
#quieren pueden pasarlos de la manera server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print >>sys.stderr, 'conectando a %s puerto %d' % (addr, port)

#Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
#Nos conectamos al servidor con el metodo connect. Tiene dos parametros
#El primero es la IP del servidor y el segundo el puerto de conexion
cliente.connect((addr,port))


try:
    while True:
        # Enviando datos
        mensaje = raw_input("Mensaje a enviar ")
        print >>sys.stderr, 'enviando "%s"' % (mensaje)
        cliente.sendall(mensaje)

        #Recibe la confirmacion, desde el servidor, del mensaje enviado
        respuesta = cliente.recv(1024)
        print >>sys.stderr, 'Recibido "%s"' % (respuesta)

        if mensaje.upper() == 'CERRAR':
            break


finally:
    print >>sys.stderr, 'Cerrando la conexion'
    cliente.close()
