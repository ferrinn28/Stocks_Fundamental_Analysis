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
            insert_query = """
            INSERT INTO basic_info 
            (stock_id, sector_type, industry_type, website, country) 
            VALUES (?, ?, ?, ?, ?)
            """

            cursor.execute(insert_query, 
                           basic_info["Code"], basic_info["Sector"], basic_info["Industry"], 
                           basic_info["Website"], basic_info["Country"])

            # Commit the transaction
            self.connection.commit()
            print("INSERT DATA IS SUCCESSFULL")

        except pyodbc.Error as err:
            # Get Some Error Code and Error Message
            #error_msg = err.args[1]
            #print(error_msg)
            print(err)

        finally:
            # Close the cursor and connection
            cursor.close()
            self.connection.close()
            print("Connection Close")

    def insert_quarter_fundamental(self, quarter_data):
        # Insert Ticker's Quarter Fundamental Datas
        try:
            # Create Cursor
            cursor = self.connection.cursor()

            # Insert data into the basic_info table
            insert_query = """
            INSERT INTO quarter_fundamental 
            (report_id, stock_id, date, book_value, price_book_value, 
            net_profit_margin, return_of_equity, earning_per_shares, price_earning_ratio) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query,
                           quarter_data["Type Report"], quarter_data["Code"], 
                           quarter_data["Date"], quarter_data["Fundamental Data"]["BV"], 
                           quarter_data["Fundamental Data"]["PBV"], quarter_data["Fundamental Data"]["NPM"],
                           quarter_data["Fundamental Data"]["ROE"], quarter_data["Fundamental Data"]["EPS"],
                           quarter_data["Fundamental Data"]["PER"])

            # Commit the transaction
            self.connection.commit()
            print("INSERT DATA IS SUCCESSFULL")
            
        except pyodbc.Error as err:
            # Get Some Error Code and Error Message
            #error_msg = err.args[1]
            #print(error_msg)
            print(err)
        
        finally:
            # Close the cursor and connection
            cursor.close()
            self.connection.close()
            print("Connection Close")