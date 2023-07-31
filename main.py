from analysis_data import QueryData, CalculateQuarter, CalculateAnnual
from create_report import CreateExcel
from database_connector import MysqlConnector

PATH = 'C:\\Users\\ASUS\\Documents\\FInancial Startegy\\Project_Fundamental\\Testing'

if __name__ == "__main__":
    ticker_code = input("Kode Emiten: ")
    sheet_overview = QueryData(ticker_code)
    checking = input("Check Annual (a) or Quartal (q)?:")

    if checking.lower() == "q":
        list_date = sheet_overview.get_balance_sheet_quarter()['asOfDate'].dt.strftime("%Y-%m-%d").tolist()
        print("AVAILABLE DATE FOR THE REPORTS")
        for i, j in enumerate(list_date, start=1):
            print(f"{i}.", j)

        # Choose Date to Review
        date_input = int(input("Choose the Date: "))
        date = list_date[date_input -1]

        # Calculating Fundamental Parameter
        searching_data = CalculateQuarter(ticker_code, date)
        output = searching_data.output()

        user_status = input("Generate Report? [y/N]: ")

        if user_status == "y":
            # Create a Excel Report
            CreateExcel(PATH, output).create_report()

        else:
            print(output)
            print(sheet_overview.get_basic_info())

            store_db = input("Store Basic Data into DB? [y/N]: ")
            if store_db == "y":
                MysqlConnector().insert_basic_info(sheet_overview.get_basic_info())
            else:
                pass

    elif checking.lower() =="a":
        list_date = sheet_overview.get_balance_sheet_annual()['asOfDate'].dt.strftime("%Y-%m-%d").tolist()
        print("AVAILABLE DATE FOR THE REPORTS")
        for i, j in enumerate(list_date, start=1):
            print(f"{i}.", j)

        # Choose Date to Review
        date_input = int(input("Choose the Date: "))
        date = list_date[date_input -1]

        # Calculating Fundamental Parameter
        searching_data = CalculateAnnual(ticker_code, date)
        output = searching_data.output()

        user_status = input("Generate Report? [y/N]: ")

        if user_status == "y":
            # Create a Excel Report
            CreateExcel(PATH, output).create_report()

        else:
            print(output)
            print(sheet_overview.get_basic_info())