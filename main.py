from QueryData import Data, CalculateQuarter

if __name__ == "__main__":
    ticker_code = input("Kode Emiten: ")

    sheet_overview = Data(ticker_code)
    print(sheet_overview.get_balance_sheet_quarter())

    date = "2022-12-31"
    searching_data = CalculateQuarter(ticker_code, date)

    #print(searching_data.get_balance_sheet_quarter())
    print("\n")
    print(f"Cumulative Revenue    {ticker_code} {date} :", searching_data.cumulative_revenue)
    print(f"Cumulative Net Income {ticker_code} {date} :", searching_data.cumulative_net_income)
    print(f"BV  of {ticker_code} {date} :", searching_data.calculate_book_value())
    print(f"PBV of {ticker_code} {date} :", searching_data.calculate_price_book_value())
    print(f"NPM of {ticker_code} {date} :", searching_data.calculate_net_profit_margin(), "%")
    print(f"ROE of {ticker_code} {date} :", searching_data.calculate_ROE(), "%")
    print(f"EPS of {ticker_code} {date} :", searching_data.calculate_EPS())
    print(f"PER of {ticker_code} {date} :", searching_data.calculate_PER())