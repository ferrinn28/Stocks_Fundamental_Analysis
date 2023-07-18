from .query_data import QueryData
import pandas as pd

#Calculate Annual Data Value
class CalculateAnnual(QueryData):

    def __init__(self, ticker, date_input):
        super().__init__(ticker)
        self.balance_sheet_annual = self.get_balance_sheet_annual()
        self.income_statement_annual = self.get_income_statement_annual()
        self.input_date = pd.to_datetime(date_input)

        #Gets Date Component (Year, Month, Date)
        self.year = self.input_date.year
        self.month = self.input_date.month
        self.day = self.input_date.day

        #Always Used Components
        ##Select Row Based on User Date Input
        rows = self.balance_sheet_annual[self.balance_sheet_annual['asOfDate'] == self.input_date]
        self.equity = rows["StockholdersEquity"][0]
        self.shares = rows["ShareIssued"][0]

        ##Collect 1 Month Historical Price
        self.historical_price = self.get_history_price(period="1mo", interval="1d", 
                                                       start=f"{self.year}-{self.month}-1", end=f"{self.year}-{self.month}-{self.day}")
        
        ##Select Some Annual in a Year based on user input date
        selected_income_statement = self.income_statement_annual[(self.income_statement_annual['asOfDate'].dt.year == self.year) 
                                                                 & (self.income_statement_annual['periodType'] == "12M")]
        
        ###Revenue in period of time
        self.revenue = selected_income_statement["TotalRevenue"][0]

        #Net Income in period of time
        self.net_income = selected_income_statement["NetIncomeCommonStockholders"][0]
        
    def get_specific_historical_price(self):
        #Change Date Index into New Column
        historical_price = self.historical_price.reset_index()
        historical_price["date"] = pd.to_datetime(historical_price["date"])
        
        #Check If On a date has a value
        selected_history = historical_price[historical_price["date"] == self.input_date]
        if selected_history.empty:
            i = 1
            while selected_history.empty:
                selected_history = historical_price[historical_price["date"].dt.day == self.day -i]
                i = i + 1

            return selected_history.iloc[0]["adjclose"]
        else:

            return selected_history.iloc[0]["adjclose"]

    def calculate_book_value(self):  
        # Calculate Book Value
        bv = (self.equity/self.shares)

        return int(bv)
    
    def calculate_price_book_value(self):
        #Get Historical Price
        historical_price = self.get_specific_historical_price()

        #Calculate Price Book Ratio
        pbv = historical_price/(self.calculate_book_value())

        return float(f'{pbv:.2f}')

    def calculate_ROE(self):
        #ROE Data
        roe = ((self.net_income)/(self.equity))*100

        return float(f'{roe:.2f}')
    
    def calculate_net_profit_margin(self):
        #NPM Data
        npm = (self.net_income/self.revenue)*100

        return float(f'{npm:.2f}')

    def calculate_EPS(self):
        #EPS Data
        eps = ((self.net_income)/(self.shares))

        return float(f'{eps:.2f}')
    
    def calculate_PER(self):
        #Get Historical Price
        historical_price = self.get_specific_historical_price()

        #Calculate Price Earning Ratio
        per = historical_price/(self.calculate_EPS())

        return float(f'{per:.2f}')
    
    def output(self):
        #Return Fundamentals Calculations
        data_fundamentals = {
            "Code": f"{self.code}",
            "Type Report": "Annual",
            "Date": self.input_date.strftime('%Y-%m-%d'),
            "Fundamental Data": {
                "Cumulative Revenue": self.revenue,                   #in rupiah
                "Cumulative Net Income": self.net_income,             #in rupiah
                "BV": self.calculate_book_value(),                    #in rupiah
                "PBV": self.calculate_price_book_value(),
                "NPM": self.calculate_net_profit_margin(),            #in %
                "ROE": self.calculate_ROE(),                          #in %
                "EPS": self.calculate_EPS(),                          #in rupiah
                "PER": self.calculate_PER()
            }
        }

        return data_fundamentals