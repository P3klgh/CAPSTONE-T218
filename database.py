#install "MySQL Connector" using 'python -m pip install mysql-connector-python' in the terminal
import mysql.connector
import logging

logging.basicConfig(level=logging.INFO)

#db connection to azure server
db_server_name = "capstone-t218-train-simulator.mysql.database.azure.com"
db_username = "team218"
db_password = "TrainSim1"

def databaseConnection(databaseName):
    connection = None
    try:
        connection = mysql.connector.connect(
        host=db_server_name,
        user=db_username,
        password=db_password,
        database = databaseName
        )
        logging.info(f"Successfully connected to database '{databaseName}'")
        return connection
    except mysql.connector.Error as e:
        if str(e).find('database') > 0:
            logging.error(f"The database '{databaseName}' does not exist.")
        elif str(e).find('server') > 0:
            logging.error(f"Can't connect to server '{db_server_name}'.  Please check username, password and server name")
        else:
            logging.error(f"An error occured: {e}")
            return None


def closeDatabaseConnection(connection):
    if connection and connection.is_connected():
        try:
            connection.close()
            logging.info("Database connection closed successfully.")
        except Exception as e:
            logging.error(f"Error closing database connection: {e}")


def testDataBaseConnection(connection):
    if connection is None:
        logging.warning("No active database connection")
        return False
    try:
        if connection.is_connected():
            logging.info(f"The database '{connection.database}' is connected.")
            return True
        else:
            logging.warning(f"The database is not connected")
            return False
    except mysql.connector.Error as e:
        logging.error(f"Error occured: '{e}'")
        return False



'''

mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
mycursor.execute("USE mainDB; CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633')
]

mycursor.executemany(sql, val)

maindb.commit()

print(mycursor.rowcount, "was inserted.")
'''