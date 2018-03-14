import json
import socket

class ClientSocket(object):
	def __init__(self, address='127.0.0.1', port=4444):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._address = address
		self._port = port

	def connect(self):
		self.socket.connect((self._address, self._port))
	
	def sendPath(self, path):
		if (self.socket):
			data = {'command':'go','filePath':path}
			self._send(data)

	def close(self):
		if (self.socket):
			self.socket.close()
			self.socket = None

	def _send(self, data):
		serialized = json.dumps(data).encode()
		self.socket.send(serialized)
		response = self._recv()
		print(response)

	def _recv(self):
		data = self.socket.recv(1024).decode()
		return json.loads(data)