from QueryData import Data, CalculateQuarter

if __name__ == "__main__":
    ticker_code = input("Kode Emiten: ")

    sheet_overview = Data(ticker_code)
    list_date = sheet_overview.get_balance_sheet_quarter()['asOfDate'].dt.strftime('%Y-%m-%d').tolist()
    print("AVAILABLE DATE FOR THE REPORTS")
    for i, j in enumerate(list_date, start=1):
        print(f"{i}.", j)

    #Choose Date to Review
    date_input = int(input("Choose the Date: "))
    date = list_date[date_input -1]

    #Calculating Fundamental Parameter
    searching_data = CalculateQuarter(ticker_code, date)

    print("\n")
    print(f"Cumulative Revenue    {ticker_code} {date} :", searching_data.cumulative_revenue)
    print(f"Cumulative Net Income {ticker_code} {date} :", searching_data.cumulative_net_income)
    print(f"BV  of {ticker_code} {date} :", searching_data.calculate_book_value())
    print(f"PBV of {ticker_code} {date} :", searching_data.calculate_price_book_value())
    print(f"NPM of {ticker_code} {date} :", searching_data.calculate_net_profit_margin(), "%")
    print(f"ROE of {ticker_code} {date} :", searching_data.calculate_ROE(), "%")
    print(f"EPS of {ticker_code} {date} :", searching_data.calculate_EPS())
    print(f"PER of {ticker_code} {date} :", searching_data.calculate_PER())