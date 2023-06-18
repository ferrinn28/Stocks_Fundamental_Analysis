from yahooquery import Ticker
import pandas as pd

# Default period = ytd, interval = 1d
#df = tickers.history()
#print(df.head())

#Super Class
class Data:
    def __init__(self, ticker):
        code = ".".join([ticker, "JK"])
        self.query = Ticker(code)

    def get_balance_sheet_quarter(self):
        return(self.query.balance_sheet("q"))

    def get_balance_sheet_annual(self):
        return(self.query.balance_sheet("a"))
    
    def get_history_price(self, period="ytd", interval="1d", start=None, end=None):
        return(self.query.history(period=period, interval=interval, start=start, end=end))
    
#Sub Class
class CalculateQuarter(Data):
    def __init__(self, ticker, date_input):
        super().__init__(ticker)
        self.balance_sheet_quartal = self.get_balance_sheet_quarter()
        self.input_date = pd.to_datetime(date_input)

        #Gets Date Component (Year, Month, Date)
        self.year = self.input_date.year
        self.month = self.input_date.month
        self.day = self.input_date.day

    def calculate_book_value(self):
        #date = pd.to_datetime(date_input)

        print(f"Date of PBV {self.year}-{self.month}-{self.day}")
        
        #Select Row Based on User Date Input
        rows = self.balance_sheet_quartal[self.balance_sheet_quartal['asOfDate'] == self.input_date]

        # Calculate Book Value
        BV = (rows["StockholdersEquity"][0])/(rows["ShareIssued"][0])
        return int(BV)