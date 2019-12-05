import socket
import os
import hashlib
import requests
import re

PASSWD = "xxxxxxx"

print("Server Start...")

#get the ip of the system:
req = requests.get("http://txt.go.sohu.com/ip/soip")
ip = re.findall(r'\d+.\d+.\d+.\d+',req.text)[0]
print("the ip of the system : ",ip)

server = socket.socket()

#server.bind(("121.248.55.149",8000))
server.bind((ip,8000))


server.listen(5)
print("Listen...")
i = 0

while True:
	if i == 1:
		break
	conn,addr = server.accept()
	print("connected : ",conn,"\naddr : ",addr)
	while True:
		i = 1
		#conn.send("please enter the passwd".encode("utf-8"))
		conn.send("please enter the passwd".encode("utf-8"))
		passwd = conn.recv(1024).decode("utf-8")
		if passwd != PASSWD:
			conn.shutdown(2)
			conn.close()
			server.close()
			break
		else:
			conn.send("which file".encode("utf-8"))
		data = conn.recv(1024).decode("utf-8")		#receive the command
		if not data:
			print("command trans finished!")
			break
		print("Command : ",data)	#print the command
		filename = data
		try:
			if os.path.isfile(filename):	#whether the file exist
				size = os.stat(filename).st_size
				conn.send(str(size).encode("utf-8"))		#send the size
				#print("send size : ",size)

				print(conn.recv(1024).decode("utf-8"))	#receive the client confirm size

				m = hashlib.md5()
				f = open(filename,"rb")		#open file
				data = f.read()				#read file
				conn.send(data)				#send file
				m.update(data)
				f.close()

				md5 = m.hexdigest()
				print("md5 : ",md5)
				conn.send(md5.encode("utf-8"))		#send md5 message
			conn.shutdown(2)
			conn.close()
			server.close()
			break
		except:
			print("ERROR")
			server.close()







