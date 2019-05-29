# import socket is used to communicate within the network
import socket

# import threading allows the script to do multiple operations at once
import threading

# import queue it is useful for threading
# it exchange information safely between threads
# basically it puts a thread in a queue
from queue import Queue

# inserts a timer
from datetime import datetime

# defines the scanning function and passes in ip_addr, start_port, end_port
def port_scan(host_ip, first_port, last_port):

	# sets the timeout period to 0.25 seconds
	# this sets the time to wait before it moves to next thread
	socket.setdefaulttimeout(0.25)

	# theading.Lock() means it prevents simultaneous access to a function
	# it locks a function to a single theard process until its complete
	# also, this prevents collisions with other threads 
	thread_lock = threading.Lock()

	# re-assigns the Queue function into a variable
	q = Queue()

	# defines the port function and passes in get_port
	def port(get_port):
		
		try: 

			# the sock variable will use IPv4 to send information
			# uses a TCP connection
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			# binds an IP to a port connection
			conn = sock.connect((host_ip, get_port))

			# thread_lock prevents other threads to access get_port variable 
			# once complete, the print() function will print value
			with thread_lock:
					print('{0:<10}{1:<10}'.format(get_port,'OPEN'))

			# closes the connection
			conn.close()

		# if no port connection made it will continue to check other ports until a connection is made
		except:

			# do nothing if there is no connection
			pass

	# calls the main function for threading
	def threader():

		# sets a loop to continuously operate the threader until it is complete
		while True:

			# grabs the a variable from the queue in the for loop
			get_port = q.get()

			# calls the function port() and inserts the get_port variable
			port(get_port)

			# ends the queue task and repeats the loop
			q.task_done()

	# informs the user the start of IP scan
	print('Port Scan Report for: ', host_ip)
	print('{0:<10}{1:<10}'.format('PORT','STATUS'))

	# creates the number/size of threads to operate
	for x in range(100):

		# everytime a new port is discovered it passes in information to threader
		t = threading.Thread(target = threader)

		# the program can exit regardless of any existing thread still operating
		t.daemon = True

		# starts the threading
		t.start()

	# grabs the range of ports to be scanned
	for get_port in range(first_port, last_port):

		# places the get_port variable into queue
		q.put(get_port)

	# places a new thread to the queue after the previouse thread is complete
	q.join()

# the main function to run when the program is executed
def main():

	# create a loop
	while True:

		try:

			# prompts the user to enter the IP address to be scanned
			ip_addr = str(input('\nEnter the first IP address range: '))

			# gethostbyname function returns the IP address of the host
			# it also checks if a valid ip address was entered
			host_ip = socket.gethostbyname(ip_addr)

			# splits the ip_addr into a list
			ip_addr_octet = ip_addr.split('.')

			# creates a dot variable
			dot = '.'

			# joins the list up to the third octect
			full_ip_addr = ip_addr_octet[0] +dot+ ip_addr_octet[1] +dot+ ip_addr_octet[2] +dot

			# prompts the user to enter the last IP address range
			ip_addr_2nd = str(input('Enter the Last IP address range: '))

			# gethostbyname function returns the IP address of the host
			# it also checks if a valid ip address was entered
			host_ip_2nd = socket.gethostbyname(ip_addr_2nd)

			# splits the ip_addr into a list
			ip_addr_octet_2nd = ip_addr_2nd.split('.')

			# prompts the user to enter the first and last port to be scanned
			first_port = input('Enter the first port range: ')
			last_port = input('Enter the last port range: ')

			# starts and displays the timer
			timer_start = datetime.now()
			print('\nStarting Port Scan at: ', timer_start)

			# if no value entered in last port
			if not last_port:
				last_port = int(first_port) + 1

			# if no value is entered in ip_addr_2nd
			if not ip_addr_2nd:

				# calls the function for a single IP address scan
				port_scan(host_ip,int(first_port),(int(last_port) + 1))

			else:

				# if a range is provided then it will scanned all IP address within that range
				# the ranged used the last octet of the IP address
				# ip must be set to str
				for ip in range(int(ip_addr_octet[3]),(int(ip_addr_octet_2nd[3]) + 1)):
					ip_addr_full = full_ip_addr + str(ip)
					port_scan(ip_addr_full,int(first_port),(int(last_port) + 1))

			# timer ends and displays result
			timer_end = datetime.now()
			timer_total = timer_end - timer_start
			print('Port Scan complete at: ', timer_total)

		# triggers when a keyboard interrupt and exits the program
		except KeyboardInterrupt:
			print('\nProgram exit')
			exit(0)

		# triggers when a ctrl + z activated and ^Z entered
		except EOFError:
			print('\nProgram exit')
			exit(0)

		# when an invalid IP address is entered by the user
		except socket.gaierror:
			print('Invalid IP address')
			continue

		# when no IP address is entered
		except IndexError:
			print('Please enter an IP address')
			continue

		# when no Port number entered 
		except ValueError:
			print('Please enter a port number')
			continue

if __name__ == '__main__':
	main()