# import the Structured Query Language to intercat with the database
import sqlite3

def create_database():

	# creates a database 
	db_name = "database.db"

	# creates a table statement
	sql = """CREATE TABLE database
			(ProductID INTEGER,
			Name TEXT,
			Price REAL,
			PRIMARY KEY(ProductID))"""

	# calls the create table function
	create_table(db_name, "database", sql)

# the function enables to create a table which will pass the name of the database, the table and the sql 
def create_table(db_name, table_name, sql):

	# opens, runs, queries, closes the database
	with sqlite3.connect(db_name) as db:

		# cursor is used to navigate around the database
		cursor = db.cursor()

		# additional query to check for an existing table in "sqlite_master" otherwise an error will occur
		# this expects a tuple statement hence (table_name,)
		cursor.execute("SELECT name FROM sqlite_master WHERE name=?",(table_name,))

		# get result 
		result = cursor.fetchall()

		# decides whether to keep the or recreate the table using boolean value
		keep_table = True

		# check the length of the result. 
		# if result is equal to 1 then the statment is True
		if len(result) == 1:

			# asks the user of table will be recreated
			response = input('The table {0} already exists, do you wish to recreate it (y/n): '.format(table_name))

			# recreates the table if "y" was selected
			if response == "y":
				keep_table = False

				# warns the user
				print("The {0} table will be recreated = all existing data will be lost".format(table_name))

				# drops the existing table
				cursor.execute("drop table if exists {0}".format(table_name))
				db.commit()

			else:

				# if "n" was selected the keep the existing table
				print("No changes made to the {0} table".format(table_name))

		else:
			keep_table = False

		if not keep_table:

			# runs the sql statment
			cursor.execute(sql)

			# anychanges made is saved in the database
			db.commit()

# a function that inserts data 
def insert_data(value):

	# opens, runs, queries, closes the database
	with sqlite3.connect("database.db") as db:

		# cursor is used to navigate around the database
		cursor = db.cursor()

		# this allows any values to be created and pass in the "Name" and "Price" attributes
		sql = "INSERT INTO database (Name, Price) VALUES (?,?)"

		# runs the sql statement and passed in the values of "Name" and "Price"
		cursor.execute(sql, value)

		# any changes made is saved in the database
		db.commit()

def edit_data(data):

	# opens, runs, queries, closes the database
	with sqlite3.connect("database.db") as db:

		# cursor is used to navigate around the database
		cursor = db.cursor()

		# update the Product table
		sql = "update database set Name=?, Price=? where ProductID=?"

		# runs the sql statement and passed in the data
		cursor.execute(sql, data)

		# anychanges made is saved in the database
		db.commit()

# a function that deletes data 
def delete_product(data):

	# opens, runs, queries, closes the database
	with sqlite3.connect("database.db") as db:

		# cursor is used to navigate around the database
		cursor = db.cursor()

		# deletes the product name
		sql = "DELETE FROM database WHERE Name=?"

		# runs the sql statement and passed in the data
		cursor.execute(sql, data)

		# anychanges made is saved in the database
		db.commit()

# a function that selects all data 
def select_all_product():

	# opens, runs, queries, closes the database
	with sqlite3.connect("database.db") as db:

		# cursor is used to navigate around the database
		cursor = db.cursor()

		# selects all attributes of the product using *
		# products is displayed by ProductID in ascending order
		# you can use different attribute such as Name or Price and set it to a "desc" descending order
		cursor.execute("SELECT * FROM database ORDER BY ProductID ASC")

		# returns all of the results
		products = cursor.fetchall()

		return products

# selects individual 
def select_product(name):

	# opens, runs, queries, closes the database
	with sqlite3.connect("database.db") as db:

		# cursor is used to navigate around the database
		cursor = db.cursor()

		# selects selects only Name and Price
		cursor.execute("SELECT ProductID, Name, Price FROM database WHERE Name=?", (name,))

		# returns all of the results
		products = cursor.fetchone()

		return products

def main():

	while True:

		try:

			# displays the menu for the user
			print("\nMain Menu\n")
			print("[1] Create/Recreate Product Table")
			print("[2] Add new product")
			print("[3] Edit existing product")
			print("[4] Delete existing product")
			print("[5] Display all products")
			print("[6] Search for individual product")
			print("[0] Exit\n")

			# requires the user to enter an input
			selection_opt = int(input("Please select an option: "))

			# if arguements
			if selection_opt == 1:
				print("\nProduct\n")

				# calls for the create_database() function
				create_database()

			elif selection_opt == 2:
				print("\nAdd new product\n")

				# prompts the user to enter the name of the new product
				# the input value must use single qoutation to add value into the datase
				name = input('Enter the name of the new product: ')

				# reassigns the first letter of the name variable into upper case
				name = name[0].upper() + name[1:]

				# prompts the user to enter the price value
				# float allows the user to add decimal numbers
				price = float(input('Enter the price of the new product: '))

				products = (name, price)

				# calls for the insert_data function
				insert_data(products)

			elif selection_opt == 3:
				print("\nEdit Product\n")

				# prompts the user to enter first the ProductID
				productID = int(input('Enter the serial of the product to edit: '))

				# prompts the user to enter the new name of the product
				name = input('Enter the new name of the product: ')

				# reassigns the first letter of the name variable into upper case
				name = name[0].upper() + name[1:]

				# prompts the user to add a new price using float
				# float allows the user to add decimal numbers
				price = float(input('Enter the new price of the product: '))

				data = (name, price, productID)

				edit_data(data)

			elif selection_opt == 4:
				print("\nDelete Product\n")

				# prompts the user to enter the name of the product to be deleted
				name = input('Enter the product name to be deleted: ')

				# reassigns the first letter of the name variable into upper case
				name = name[0].upper() + name[1:]

				# assigns the input into the data variable
				# the func expects a tuple value, hence it has a comma after the variable "name"
				data = (name,)

				# calls the delete_product function
				delete_product(data)

			elif selection_opt == 5:
				print("\nDisplay Product\n")

				# displays all product
				products = select_all_product()

				# indents the title into proper spacing
				print("{0:<10}{1:<15}{2:<1}\n".format("Serial", "Product Name", "Value"))

				# unpacks the tuple variables and displays them below the title
				for i in products:
					print("{0:<10}{1:<15}{2:<1}".format(i[0], i[1], i[2]))

			elif selection_opt == 6:
				print("\nDisplay Product\n")

				# prompts the user to enter the serial number of the product
				name = input('Enter the product Name to search: ')

				# reassigns the first letter of the name variable into upper case
				name = name[0].upper() + name[1:]

				# assigns the value of name and calls the select_product function
				products = select_product(name)

				# indents the title into proper spacing
				print("{0:<10}{1:<15}{2:<1}\n".format("Serial", "Product Name", "Value"))

				# a list was created to prevent a TypeError from occuring
				products_list = []

				# unpacks the tuple variables and add them to the products_list list
				for i in products:
					products_list.append(i)
				
				# displays the variable
				print("{0:<10}{1:<15}{2:<1}".format(products_list[0], products_list[1], products_list[2]))

			elif selection_opt == 0:
				print("\nExiting program...\n")

				# exits the program
				exit(0)

		# exits the programs if keyboard interrupt occurs
		except KeyboardInterrupt:
			print("\nKeyboardInterrupt...")

			# exits the program
			exit()

		# error occurs when a ctrl+z "^Z" was entered as an input
		except EOFError:
			print("\nError Occurs")

		# error occurs when a string was entered instead of an integer
		except ValueError:
			print("\nA ValueError Occur")

if __name__ == "__main__":
	main()
