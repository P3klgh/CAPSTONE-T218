from database import *
import logging
logging.basicConfig(level=logging.INFO)

databaseName = 'maindb'

def addBattery(batteryName, batteryMaxCapacity, batteryMinCapacity = 0):
    try:
        if batteryMaxCapacity == 0:
            raise Exception("maxBatteryCapacity is empty")
    except Exception as e:
        logging.error(f"Maximum Battery Capacity cannot be empty")
        return False

    connection = databaseConnection(databaseName)
    if testDataBaseConnection(connection) == True:
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO battery (batteryName, batteryMaxCapacity, batteryMinCapacity) VALUES (%s, %s, %s)"
            val = (batteryName, batteryMaxCapacity, batteryMinCapacity)
            cursor.execute(sql, val)
            logging.info(cursor.rowcount, "record inserted.")
            return True
        except Exception as e:
            if str(e).find('Duplicate entry') > 0:
                logging.error(f"Battery with name '{batteryName}' already exists")
                return False
            else:
                logging.error(f"An error occured: {e}")
                return False
    cursor.close()
    connection.commit()
    closeDatabaseConnection(connection)

