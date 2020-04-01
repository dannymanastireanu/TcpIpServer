import socket
from os import path
import gzip
from threading import Thread


class TcpIp():
	def __init__(self, ip, port):
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serversocket.bind((ip, port))
		self.serversocket.listen(5)
		self.th_sockets = []


	def close_connection(self):
		print('Wait for server socket to close (host {}, port {})'.format(self.host, self.port))

		if not self.th_sockets:
			for th in self.th_sockets:
				th.stop()
				th.join()

		if self.serversocket:
			self.serversocket.close()
			self.serversocket = None


	def process(self, client_socket, client_addr):
		data = client_socket.recv(1024)

		if not data:
			return

		print('Receive: ' + str(data))


	def run(self):
		print('====== Start Server ======')

		while True:
			print ('Serverul asculta potentiali clienti.')

			try:
				client_socket, client_addr = self.serversocket.accept()
			except Exception:
				client_socket = None

			if client_socket:
				th = Thread(target=self.process, args=(client_socket, client_addr, ))
				self.th_sockets.append(th)
				th.start()

		self.close_connection()



def main():
	server = TcpIp('localhost', 5678)
	server.run()



if __name__ == "__main__":
	main()
