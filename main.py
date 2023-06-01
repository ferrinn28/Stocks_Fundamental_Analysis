from QueryData import Data

if __name__ == "__main__":
    ticker_code = input("Kode Emiten: ")

    searching_data = Data(ticker_code)

    print(searching_data.get_balance_sheet_annual())