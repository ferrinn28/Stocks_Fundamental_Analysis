import os

import pyodbc
from dotenv import load_dotenv

class MysqlConnector:
    def __init__(self):
        # Load env file
        load_dotenv()
        MYSQL_SERVER = os.getenv("MYSQL_SERVER")
        MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
        MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
        MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

        # Create the connection string
        connection_string = f"DRIVER={{MySQL ODBC 8.0 Unicode Driver}};\
            SERVER={MYSQL_SERVER};DATABASE={MYSQL_DATABASE};UID={MYSQL_USERNAME};PWD={MYSQL_PASSWORD};"

        try:
            # Establish the connection
            print("Connection Establish")
            self.connection = pyodbc.connect(connection_string)
            print("Connection Successfull")
            # Close the connection when done
            self.connection.close()
            
        except Exception as e:
            print(f"Error: {e}")
