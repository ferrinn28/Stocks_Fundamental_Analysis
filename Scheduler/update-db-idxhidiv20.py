from yahooquery import Ticker
from pprint import pprint
from dotenv import dotenv_values
from datetime import datetime
import mysql.connector

config = dotenv_values(".env.production")
current_date = datetime.now().date()

print("Current Date:", current_date)

LIST_STOCKS = ["ADRO", "AMRT", "ANTM", "ASII",
               "BBCA", "BBNI", "BBRI", "BJBR", "BJTM", "BMRI",
               "BNGA", "BSSR", "HEXA", "HMSP", "INDF",
               "ITMG", "MPMX", "PTBA", "TLKM", "UNTR"]

LIST_STOCKS_WITH_JK = [stock + ".JK" for stock in LIST_STOCKS]

tickers = Ticker(" ".join(LIST_STOCKS_WITH_JK))

df = tickers.history(period="1mo", interval="1d", start=current_date)

values = df["close"].to_list()

stock_value_dict = {stock: value for stock, value in tuple(zip(LIST_STOCKS, values))}
pprint(stock_value_dict)

# Establish the connection
connection = mysql.connector.connect(
    host=config["MYSQL_SERVER"],
    user=config["MYSQL_USERNAME"],
    password=config["MYSQL_PASSWORD"],
    database=config["MYSQL_DATABASE"]
)

# Define the update query
update_query = """
    UPDATE current_idxhidiv20
    SET current_price = %s,
        updated_at = CURDATE()
    WHERE stock_id = %s
"""

# Create a cursor
cursor = connection.cursor()

# Execute the update query for each entry in the dictionary
cursor = connection.cursor()
for stock_id, new_price_value in stock_value_dict.items():
    cursor.execute(update_query, (new_price_value,stock_id))
    connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

