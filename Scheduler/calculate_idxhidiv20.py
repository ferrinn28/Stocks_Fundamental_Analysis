from dotenv import dotenv_values
import mysql.connector

# Credential DB
config = dotenv_values(".env.production")

# Establish the connection
connection = mysql.connector.connect(
    host=config["MYSQL_SERVER"],
    user=config["MYSQL_USERNAME"],
    password=config["MYSQL_PASSWORD"],
    database=config["MYSQL_DATABASE"]
)

# Define the query
query_current_idxhidiv20 = """
SELECT * FROM current_idxhidiv20 ORDER BY stock_id ASC
"""

query_base_idxhidiv20 = """
SELECT * FROM base_idxhidiv20 ORDER BY stock_id ASC
"""

query_base_index = """
SELECT * FROM idxhidiv20 WHERE date_time = %s
"""

insert_current_index = """
INSERT INTO idxhidiv20 (index_value, date_time)
    VALUES (%s, CURDATE())
"""

try:
    # Create a cursor
    cursor = connection.cursor()

    # Get Current Stock of IDXHIDIV20 Data
    cursor.execute(query_current_idxhidiv20)
    current_idxhidiv20 = cursor.fetchall()

    # Get Base Stock of IDXHIDIV20 Data
    cursor.execute(query_base_idxhidiv20)
    base_idxhidiv20 = cursor.fetchall()

    # Get Base IDXHIDIV20 Value for Specific Range of Time
    base_date = base_idxhidiv20[0][3].strftime("%Y-%m-%d")
    cursor.execute(query_base_index, (base_date,))
    idx_base = cursor.fetchall()

    # Calculate Sums of Current and Base Market IDXHIDIV20
    sum_base = sum(row[1] * row[2] for row in base_idxhidiv20)
    sum_current = sum(row[1] * base_idxhidiv20[i][1] for i, row in enumerate(current_idxhidiv20))

    # Calculate Current IDXHIDIV20
    percentage_idx = sum_current/sum_base
    idx_now = percentage_idx * idx_base[0][0]

    #Insert Current IDXHIDIV20 Value
    cursor.execute(insert_current_index, (idx_now,))
    connection.commit()

except mysql.connector.Error as err:
    print("MySQL Error:", err)

finally:
    # Close the Cursor
    cursor.close()
    # Close the connection
    if connection.is_connected():
        connection.close()
