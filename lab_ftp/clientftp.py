from select import select
import socket
import sys, argparse
from os import listdir

parser = argparse.ArgumentParser(description="FTP Cliente")
parser.add_argument("--p",required=False, default=20000, type=int)
parser.add_argument("--h",required=False,default='127.0.0.1')
namespace = parser.parse_args()

ip = namespace.h
port = namespace.p
serverName = str(ip)
serverPort = port

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


clientSocket.connect((serverName, serverPort))
print("Conexion establecida ...  ")
devices = [clientSocket, sys.stdin]

while True:
	print('\nIngrese "list" para listar los archivos de la carpeta "/tmp" en el servidor.\nIngrese "get" mas nombre del archivo a descargar.\nIngrese "quit" para desconectarse ...\n')

	clientSocket.send('list'.encode())
	filesInServer = clientSocket.recv(4096).decode().split(',')
	filesInClient = listdir("./")
	device, output, error = select(devices,[],[],60)
	if not device:
		print("Tiempo de espera excedido, se terminara la conexion ...")
		clientSocket.send("close\n".encode())
		clientSocket.close()
		break

	if sys.stdin in device :
		msgClient = sys.stdin.readline().rstrip("\n")


		if msgClient.lower() == 'quit' or msgClient.lower() == 'close':
			clientSocket.send(msgClient.encode())
			clientSocket.close()
			print("Conexion finalizada. ")
			break

		elif msgClient.lower() == 'list':
			for file in filesInServer:
				print(file)


		elif msgClient[0:4] == 'get ':
			filename = msgClient[4:]

			if filename in filesInServer:
				if filename not in filesInClient:
					print('  Descargando:', filename)
					clientSocket.send(msgClient.encode())


					with open(filename,'wb') as filercv:
						clientSocket.settimeout(1)
						print("Recibiendo ...")

						while True:
							try:
								fileFromServer = clientSocket.recv(4096)
								fileWrite = filercv.write(fileFromServer)
							except socket.timeout:
								print('Transferencia completada')
								break
				else:
					print('El archivo con nombre "{}" ya existe'.format(filename))

			else:
				print('El archivo con nombre "{}" no existe en el servidor'.format(filename))

		else:
			print('La palabra "{}" es un comando desconocido'.format(msgClient))
