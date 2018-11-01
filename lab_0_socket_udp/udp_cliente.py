

#UDPclient.py
#!/usr/bin/python
import socket
import sys


arglen=len(sys.argv)
if arglen<3:
    print('python udp_cliente.py <IP> <Puerto>')
    exit()

addr=sys.argv[1]
port=int(sys.argv[2])
data=raw_input("Mensaje a enviar: ")

#Creamos un objeto socket para el servidor
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#Con la instancia del objeto servidor (s) y el metodo sendto, enviamos el mensaje introducido
s.sendto(data,(addr,port))

print data
