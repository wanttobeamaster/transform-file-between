import socket
import os
import hashlib
import sys

host = sys.argv[1]

client = socket.socket()
ip_port = (host,8000)

client.connect(ip_port)
print("target servere has connected!")

while True:
	content = input(">>>>")
	print(type(content))
	print(content)
	if len(content) == 0:
		print("content is NULL")
		continue
	else:
		print("content not NULL")
		client.send(content.encode("utf-8"))	#send the command
		print("command has sended")
		file_size = int(client.recv(1024).decode("utf-8"))
		print("receive size : ",int(file_size))

		#send the confirm of the size
		client.send("Client has received size".encode("utf-8"))

		#	start receive the data
		f = open("copy"+content.split("/")[-1],"wb")

		received_size = 0
		m = hashlib.md5()

		while received_size < file_size:
			size = 0
			if file_size - received_size > 1024:
				size = 1024
			else:
				size = file_size - received_size

			data = client.recv(size)
			f.write(data)
			data_len = len(data)
			received_size += data_len
		#m.update(whole_data)
		f.close()

		f = open("copy"+content.split("/")[-1],"rb")
		whole_data = f.read()
		m.update(whole_data)


		# md5 check
		MD5_rece = client.recv(1024).decode()
		MD5_client = m.hexdigest()
		print("MD5 server send : ",MD5_rece)
		print("MD5 client check : ",MD5_client)
		if MD5_rece == MD5_client:
			break
		else:
			print("MD5 has changed")
			break
	client.close()

