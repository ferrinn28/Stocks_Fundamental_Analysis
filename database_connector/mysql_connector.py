import pyodbc
from dotenv import dotenv_values

class MysqlConnector:
    def __init__(self):
        # Load env file as Dictionary type
        config = dotenv_values(".env")

        # Create the connection string
        connection_string = f"DRIVER={{MySQL ODBC 8.0 Unicode Driver}};\
            SERVER={config['MYSQL_SERVER']};DATABASE={config['MYSQL_DATABASE']};\
                UID={config['MYSQL_USERNAME']};PWD={config['MYSQL_PASSWORD']};"

        try:
            # Establish the connection
            print("Connection Establish")
            self.connection = pyodbc.connect(connection_string)
            print("Connection Successfull")
            # Close the connection when done
            self.connection.close()
            
        except Exception as e:
            print(f"Error: {e}")
