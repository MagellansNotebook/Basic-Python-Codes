#imports the socket module which is used to communicate over the network
import socket
import os

# creates two variable for host and port
host, port = '', 8888

# socket.AF_INET means the socket is using an IPv4 to send information
# socket.SOCK_STREAM means it is using a TCP connection
web_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# binds an IP to a port connection. It also creates a tuple.
# leaving the IP value as blank automatically reverts back to localhost
web_server.bind(('', 8888))

# listens to any connections to the server
web_server.listen(1)

print('Serving HTTP on port %s' %(port))

while True:

	# accepts connection to the web_server
	# unpacks the value accepted by the web_server
	conn, addr = web_server.accept()

	# conn.recv(1024) indicates the maximum data it can recieve
	# this is also known as a blocking function which means the loop wont run until it recieves data
	request = conn.recv(1024)

	# prints the request data from conn
	print(request)

	# a variable to send a respose from the request
	# HTTP/1.1 200 OK is a standard response for HTTP request
	http_response = """\
	HTTP/1.1 200 OK

	Hello World
	"""

	# sends all string to the web application
	# http_response is 
	conn.sendall(str.encode(http_response))

	# closes the connection
	conn.close()

