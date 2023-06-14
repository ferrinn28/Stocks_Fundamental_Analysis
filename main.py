from QueryData import Data, CalculateQuarter

if __name__ == "__main__":
    ticker_code = input("Kode Emiten: ")

    searching_data = CalculateQuarter(ticker_code)

    print(searching_data.get_balance_sheet_annual())
    print("\n")
    searching_data.calculate_book_value("2023-03-31")