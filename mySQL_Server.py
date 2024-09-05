import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_server_connection(host_name: str, get_credentials_func):
    """
    Establishes a connection to the MySQL database server using secure credentials.

    Args:
        host_name (str): The hostname of the MySQL server.
        get_credentials_func (function): A function that provides access to the stored credentials.

    Returns:
        connection: A MySQL connection object if successful, None otherwise.
    """
    # Retrieve credentials
    credentials = get_credentials_func()
    user_name = credentials['username']
    user_password = credentials['password']

    connection = None
    try:
        # Establish the connection to the MySQL server
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    
    return connection

# Usage
# get_credentials_func = secure_input()  # Store the function that accesses the credentials
# host = "localhost"  # Replace with your MySQL server host
# connection = create_server_connection(host, get_credentials_func)  # Connect to the MySQL server