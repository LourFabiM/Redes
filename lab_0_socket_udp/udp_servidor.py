

#UDPserver.py
#!/usr/bin/python
import socket
import sys


arglen=len(sys.argv)
if arglen<2:
    print('python udp_cliente.py <Puerto>')
    exit()

port=int(sys.argv[2])
historial = open('historial.txt', 'a')

#instanciamos un objeto para trabajar con el socket, dgram se utiliza solo para udp
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#Con el metodo bind le indicamos que puerto debe escuchar y de que servidor esperar conexiones
#Es mejor dejarlo en blanco para recibir conexiones externas si es nuestro caso
s.bind(("",port))

#Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
#la cantidad de bytes para recibir
data,addr=s.recvfrom(1024)

#Si se reciben datos nos muestra la IP y el mensaje recibido
recibido = 'IP: '+ addr[0] + ' Puerto: ' + str(addr[1]) +' Data: ' + data + '\n'

print recibido

historial.write(recibido)
historial.close()
