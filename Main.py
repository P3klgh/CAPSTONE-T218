import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy
import matplotlib.pyplot as plt

import getpass

# Securely store username and password
def secure_input():
    """
    Prompt the user to input their username and password securely.

    Returns:
        function: A function that provides access to the stored credentials.
    """
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    
    # Store them in a private variable
    _credentials = {'username': username, 'password': password}
    
    # Define an accessor function that can access the credentials
    def get_credentials():
        """Returns the stored credentials."""
        return _credentials
    
    return get_credentials

# A function that accesses the credentials securely
def access_credentials(get_credentials_func):
    """
    Access and use the securely stored credentials.

    Args:
        get_credentials_func (function): A function to get the credentials.
    """
    credentials = get_credentials_func()
# Usage
# get_credentials_func = secure_input()  # Store the function that accesses the credentials
# access_credentials(get_credentials_func)  # Access and use the credentials securely
