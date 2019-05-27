# import socket to communicate within a network
import socket

# import thread allows the script to do multiple things at once
import threading

# socket.AF_INET means the socket is using an IPv4 to send information
# socket.SOCK_STREAM means it is using a TCP connection
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# binds an IP to a port connection which creates a tuple.
server_sock.bind(('0.0.0.0', 10000))

# listens to any connections to the server
server_sock.listen(1)

# the list displays the connections to the server
connection = []

# handles the connection and recieves data to the connection
def handler(conn, addr):

	# allows access to the connection list outside the function
	global connection

	while True:

		# conn.recv(1024) indicates the maximum data it can recieve
		# this is also known as a blocking function which means the loop wont run until it recieves data
		data = conn.recv(1024)

		# when a data is recieve it will echo data back towards the client
		for message in connection:

			# in order not to send raw bytes use bytes(data). bytes is a function that converts from string to bytes
			message.send(bytes(data))

		# if no data receive close connection
		if not data:
			connection.remove(conn)
			conn.close()
			break

# handles the connection
while True:

	# connection returns the value of conn and its IP addrress
	conn, addr = server_sock.accept()

	# everytime a connection is accepted create a new thread
	# this passes the conn and addr to the function handler
	conn_thread = threading.Thread(target=handler, args=(conn, addr))

	# the program will be able to exit regardless if there are any threads still running
	conn_thread.daemon = True

	# starts the thread
	conn_thread.start()

	# whenver a connection occurs it will be added to the list
	connection.append(conn)

	# prints the clients information when connected to the server
	print(connection)
