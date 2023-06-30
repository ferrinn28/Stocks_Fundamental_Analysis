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
    
    def get_income_statement_quarter(self):
        return(self.query.income_statement("q"))
    
    def get_income_statement_annual(self):
        return(self.query.income_statement("a"))
    
    def get_history_price(self, period="ytd", interval="1d", start=None, end=None):
        return(self.query.history(period=period, interval=interval, start=start, end=end))
    
#Sub Class
class CalculateQuarter(Data):
    def __init__(self, ticker, date_input):
        super().__init__(ticker)
        self.balance_sheet_quartal = self.get_balance_sheet_quarter()
        self.income_statement_quartal = self.get_income_statement_quarter()
        self.input_date = pd.to_datetime(date_input)

        #Gets Date Component (Year, Month, Date)
        self.year = self.input_date.year
        self.month = self.input_date.month
        self.day = self.input_date.day

    def calculate_book_value(self):  
        #Select Row Based on User Date Input
        rows = self.balance_sheet_quartal[self.balance_sheet_quartal['asOfDate'] == self.input_date]

        # Calculate Book Value
        BV = (rows["StockholdersEquity"][0])/(rows["ShareIssued"][0])
        return int(BV)
    
    def calculate_price_book_value(self):
        #Collect Historical Price Up to Next 15 Days From User Date Input
        historical_price = self.get_history_price(period="1mo", interval="1d", 
                                                  start=self.input_date, end=f"{self.year}-{self.month+1}-15")
        selected_history = historical_price.iloc[0]["adjclose"]

        #Calculate Price Book Ratio
        PBV = selected_history/(self.calculate_book_value())
        return float(f'{PBV:.2f}')
    
    def calculate_cumulative_revenue(self):
        #Select Range of Time based on User Date Input
        selected_revenue = self.income_statement_quartal[(self.income_statement_quartal['asOfDate'].dt.year == self.year) 
                                                           & (self.income_statement_quartal['asOfDate'].dt.month <= self.month)
                                                           & (self.income_statement_quartal['periodType'] == "3M")]
        
        #Sum All revenue in period of time
        cumulative_revenue = selected_revenue["TotalRevenue"].sum()
        return cumulative_revenue
    
    def calculate_cumulative_net_income(self):
        #Select Range of Time based on User Date Input
        selected_net_income = self.income_statement_quartal[(self.income_statement_quartal['asOfDate'].dt.year == self.year) 
                                                           & (self.income_statement_quartal['asOfDate'].dt.month <= self.month)
                                                           & (self.income_statement_quartal['periodType'] == "3M")]
        
        #Sum All Net Income in period of time
        cumulative_net_income = selected_net_income["NetIncomeCommonStockholders"].sum()
        return cumulative_net_income