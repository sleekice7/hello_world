import MySQLdb

def connection():
	conn = MySQLdb.connect (
		host = "localhost", 
		user = "root", 
		passwd = "DB_connection12345", 
		db = "pythonprogramming")

	c = conn.cursor()

	return c, conn