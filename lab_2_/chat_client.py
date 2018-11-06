# chat_client.py

import sys, socket, select

arglen=len(sys.argv)
if(len(sys.argv) < 3) :
    print 'python chat_client.py <ip> <puerto>'
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

try :
    s.connect((host, port))
    usuario = raw_input('Nombre de usuario: ')
except :
    print 'Imposible conectar '
    sys.exit()

sys.stdout.write('> %s ' % usuario); sys.stdout.flush()

while 1:
    socket_list = [sys.stdin, s]

    read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

    for sock in read_sockets:
        if sock == s:
            data = sock.recv(4096)
            if not data:
                print '\nDesconectando chat '
                sock.close()
            else:
                sys.stdout.write(data)
                if data == '\rRecibido. Cerrando la conexion':
                    sys.exit()
                else:
                    sys.stdout.write('> %s ' % usuario); sys.stdout.flush()

        else :
            msg = sys.stdin.readline()
            s.send(msg)
            sys.stdout.write('> %s ' % usuario); sys.stdout.flush()
