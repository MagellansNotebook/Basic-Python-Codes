# it is a cryptographic function that encrypts a sting or group of string
import hashlib

# create a function to encrypt a string
def encrypt(word_string):

	# .sha256() calls the function to hash the word_string
	# .encode() converts the string into a bytestring in order to be hashed
	# .hexdigest() displays the hashed word string into hexadecimal digits
	word_encrypt = hashlib.sha256(word_string.encode()).hexdigest()

	# prints the hashed string
	print(word_encrypt)

# prompts the user to enter a string
word_string = str(input('Enter the word to encrypt: '))

# calls the encrypt function
encrypt(word_string)

