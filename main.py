from QueryData import Data, CalculateQuarter

if __name__ == "__main__":
    ticker_code = input("Kode Emiten: ")

    searching_data = CalculateQuarter(ticker_code, "2023-03-31")

    print(searching_data.get_balance_sheet_annual())
    print("\n")
    print(f"Book Value of {ticker_code} :", searching_data.calculate_book_value())
    print(f"Price Book Value of {ticker_code} :", searching_data.calculate_price_book_value())
    print(f"Cumulative Revenue {ticker_code} Q1 :", searching_data.calculate_cumulative_revenue()[0])
    print(f"Cumulative Net Income {ticker_code} Q1 :", searching_data.calculate_cumulative_net_income()[0])
    print(f"ROE of {ticker_code} :", searching_data.calculate_ROE())