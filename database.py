#install "MySQL Connector" using 'python -m pip install mysql-connector-python' in the terminal
import mysql.connector

#db connection to azure server
# This is bad security btw, will change in the future
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
        return connection
    except mysql.connector.Error as e:
        if str(e).find('database') > 0:
            print(f"The database '{databaseName}' does not exist.")

def addBattery(connection, batteryName, batteryMinCapacity, batteryMaxCapacity):
    cursor = connection.cursor()
    sql = "INSERT INTO battery (batteryName, batteryMinCapacity, batteryMaxCapacity) VALUES (%s, %s, %s)"
    val = (batteryName, batteryMinCapacity, batteryMaxCapacity)
    cursor.execute(sql, val)
    cursor.close()
    connection.commit()
    print(cursor.rowcount, "record inserted.")

connection = databaseConnection('maindb')
print(connection)

mycursor = connection.cursor()

addBattery(connection, 'battery2', 0, 800)

mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)

mycursor.close()
connection.close()

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