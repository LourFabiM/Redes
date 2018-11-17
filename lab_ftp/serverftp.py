import socket
import sys, argparse
from os import listdir

parser = argparse.ArgumentParser(description="FTP Server")
parser.add_argument("--p",required=False, default=20000, type=int)
namespace = parser.parse_args()

port = namespace.p
serverPort = port


serverPort = port
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(1)

while True:
    print ("Esperando cliente ...")
    connectionSocket,address = serverSocket.accept()
    print ("Conexion  establecida ...")

    while True:

        msgClient = connectionSocket.recv(4096).decode('utf-8')

        if msgClient.lower() == "quit"  or msgClient.lower() == 'close':
            connectionSocket.close()
            print("Conexion terminada.")
            break

        if msgClient.lower() == 'list':
            a=connectionSocket.send(",".join(listdir(".")).encode('utf-8'))


        if msgClient[0:4].lower() == 'get ':
            filename = msgClient[4:]
            sys.stdout.write('Enviando ...  ' + filename + '\n'); sys.stdout.flush()
            with open(filename,'rb') as fileopen:
                data = fileopen.read()
                #filesend = connectionSocket.sendfile(fileopen)
                filesend = connectionSocket.send(data)
                sys.stdout.write(str(filesend) + " bytes" + '\n'); sys.stdout.flush()
