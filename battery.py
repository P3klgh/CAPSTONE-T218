from database import *
databaseName = 'maindb'

def addBattery(connection, batteryName, batteryMinCapacity, batteryMaxCapacity):
    cursor = connection.cursor()
    sql = "INSERT INTO battery (batteryName, batteryMinCapacity, batteryMaxCapacity) VALUES (%s, %s, %s)"
    val = (batteryName, batteryMinCapacity, batteryMaxCapacity)
    cursor.execute(sql, val)
    cursor.close()
    connection.commit()
    closeDatabaseConnection(connection)
    print(cursor.rowcount, "record inserted.")