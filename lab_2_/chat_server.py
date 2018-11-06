# chat_server.py

import socket
import sys, select


arglen=len(sys.argv)
if arglen<2:
    print('python udp_cliente.py <Puerto>')
    exit()

PORT=int(sys.argv[1])
SOCKET_LIST = []
RECV_BUFFER = 4096

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', PORT))
server_socket.listen(10)

SOCKET_LIST.append(server_socket)

print "Chat iniciando en el puerto " + str(PORT)

while 1:

    ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

    for sock in ready_to_read:
        if sock == server_socket:
            sockfd, addr = server_socket.accept()
            SOCKET_LIST.append(sockfd)
            print "Cliente (%s, %s) conectado" % addr

        else:
            try:
                data = sock.recv(RECV_BUFFER)
                if data:
                    for socket in SOCKET_LIST:
                        if socket == sock :
                            try :
                                if data.upper() == 'CERRAR\n':
                                    socket.send('\rRecibido. Cerrando la conexion')
                                    dir = socket.getpeername()
                                    print "\rCliente (%s, %s) desconectado" % dir
                                    socket.close()
                                    if socket in SOCKET_LIST:
                                        SOCKET_LIST.remove(socket)
                                else:
                                    socket.send('\rRecibido ' + data)
                            except :
                                socket.close()
                                if socket in SOCKET_LIST:
                                    SOCKET_LIST.remove(socket)

                else:
                    if sock in SOCKET_LIST:
                        SOCKET_LIST.remove(sock)

            except:
                continue

server_socket.close()
