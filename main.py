from QueryData import Data, CalculateQuarter, CalculateAnnual
import json
import pandas as pd

if __name__ == "__main__":
    ticker_code = input("Kode Emiten: ")
    sheet_overview = Data(ticker_code)
    checking = input("Check Annual (a) or Quartal (q)?:")

    if checking.lower() == "q":
        list_date = sheet_overview.get_balance_sheet_quarter()['asOfDate'].dt.strftime('%Y-%m-%d').tolist()
        print("AVAILABLE DATE FOR THE REPORTS")
        for i, j in enumerate(list_date, start=1):
            print(f"{i}.", j)

        #Choose Date to Review
        date_input = int(input("Choose the Date: "))
        date = list_date[date_input -1]

        #Calculating Fundamental Parameter
        searching_data = CalculateQuarter(ticker_code, date)

        #Output in Dictionary
        pd.options.display.float_format = '{:.2f}'.format

        data_fundamentals = {
            "Code": f"{ticker_code}",
            "Type Report": f"{checking}",
            "Date": date,
            "Fundamental Data": {
                "Cumulative Revenue": searching_data.cumulative_revenue,        #in rupiah
                "Cumulative Net Income": searching_data.cumulative_net_income,  #in rupiah
                "BV": searching_data.calculate_book_value(),                    #in rupiah
                "PBV": searching_data.calculate_price_book_value(),
                "NPM": searching_data.calculate_net_profit_margin(),            #in %
                "ROE": searching_data.calculate_ROE(),                          #in %
                "EPS": searching_data.calculate_EPS(),                          #in rupiah
                "PER": searching_data.calculate_PER()
            }
        }

        #Convert into json format
        json_format = json.dumps(data_fundamentals, indent=4)
        print(json_format, "\n")

        #Convert into Dataframe
        df_upload = pd.DataFrame(json.loads(json_format))
        print(df_upload)
        #print(df_upload.index.values)
        #print(df_upload.loc["BV"]["Code"])
        #df_upload.to_excel(excel_writer="C:\\Users\\ASUS\\Documents\\FInancial Startegy\\Project_Fundamental\\Testing\\output.xlsx", sheet_name=f'{ticker_code}')

    elif checking.lower() =="a":
        list_date = sheet_overview.get_balance_sheet_annual()['asOfDate'].dt.strftime('%Y-%m-%d').tolist()
        print("AVAILABLE DATE FOR THE REPORTS")
        for i, j in enumerate(list_date, start=1):
            print(f"{i}.", j)

        #Choose Date to Review
        date_input = int(input("Choose the Date: "))
        date = list_date[date_input -1]

        #Calculating Fundamental Parameter
        searching_data = CalculateAnnual(ticker_code, date)

        #Output in Dictionary
        pd.options.display.float_format = '{:.2f}'.format

        data_fundamentals = {
            "Code": f"{ticker_code}",
            "Type Report": f"{checking}",
            "Date": date,
            "Fundamental Data": {
                "Cumulative Revenue": searching_data.revenue,                   #in rupiah
                "Cumulative Net Income": searching_data.net_income,             #in rupiah
                "BV": searching_data.calculate_book_value(),                    #in rupiah
                "PBV": searching_data.calculate_price_book_value(),
                "NPM": searching_data.calculate_net_profit_margin(),            #in %
                "ROE": searching_data.calculate_ROE(),                          #in %
                "EPS": searching_data.calculate_EPS(),                          #in rupiah
                "PER": searching_data.calculate_PER()
            }
        }

        #Convert into json format
        json_format = json.dumps(data_fundamentals, indent=4)
        print(json_format, "\n")

        #Convert into Dataframe
        df_upload = pd.DataFrame(json.loads(json_format))
        print(df_upload)
        #print(df_upload.index.values)
        #print(df_upload.loc["BV"]["Code"])
        #df_upload.to_excel(excel_writer="C:\\Users\\ASUS\\Documents\\FInancial Startegy\\Project_Fundamental\\Testing\\output.xlsx", sheet_name=f'{ticker_code}')