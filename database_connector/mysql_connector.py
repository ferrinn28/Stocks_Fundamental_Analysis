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
            
        except pyodbc.Error as e:
            print(f"Error while establishing connection: {e}")

    def insert_basic_info(self, basic_info):
        # Insert Ticker's Sector, Industry, Website and Country to DB
        try:
            # Create Cursor
            cursor = self.connection.cursor()

            # Insert data into the basic_info table
            insert_query = "INSERT INTO basic_info (stock_id, sector_type, industry_type, website, country) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(insert_query, basic_info["Code"], basic_info["Sector"], basic_info["Industry"], \
                       basic_info["Website"], basic_info["Country"])

            # Commit the transaction
            self.connection.commit()
            print("INSERT DATA IS SUCCESSFULL")

        except pyodbc.Error as err:
            # Get Some Error Code and Error Message
            error_msg = err.args[1]
            print(error_msg)

        finally:
            # Close the cursor and connection
            cursor.close()
            self.connection.close()
            print("Connection Close")