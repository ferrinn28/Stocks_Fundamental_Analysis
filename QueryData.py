from yahooquery import Ticker
import pandas as pd

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

        #Always Used Components
        ##Select Row Based on User Date Input
        rows = self.balance_sheet_quartal[self.balance_sheet_quartal['asOfDate'] == self.input_date]
        self.equity = rows["StockholdersEquity"][0]
        self.shares = rows["ShareIssued"][0]

        ##Collect 1 Month Historical Price
        self.historical_price = self.get_history_price(period="1mo", interval="1d", 
                                                  start=f"{self.year}-{self.month}-1", end=f"{self.year}-{self.month}-31")

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
    
    def calculate_cumulative_revenue(self):
        #Select Range of Time based on User Date Input
        selected_revenue = self.income_statement_quartal[(self.income_statement_quartal['asOfDate'].dt.year == self.year) 
                                                           & (self.income_statement_quartal['asOfDate'].dt.month <= self.month)
                                                           & (self.income_statement_quartal['periodType'] == "3M")]
        
        #Check Total Quartal
        quartal = selected_revenue.shape
        
        #Sum All revenue in period of time
        cumulative_revenue = selected_revenue["TotalRevenue"].sum()

        return cumulative_revenue, quartal[0]
    
    def calculate_cumulative_net_income(self):
        #Select Range of Time based on User Date Input
        selected_net_income = self.income_statement_quartal[(self.income_statement_quartal['asOfDate'].dt.year == self.year) 
                                                           & (self.income_statement_quartal['asOfDate'].dt.month <= self.month)
                                                           & (self.income_statement_quartal['periodType'] == "3M")]
        
        #Check Total Quartal
        quartal = selected_net_income.shape

        #Sum All Net Income in period of time
        cumulative_net_income = selected_net_income["NetIncomeCommonStockholders"].sum()

        return cumulative_net_income, quartal[0]
    
    def calculate_ROE(self):
        #Annualization
        cumulative_net_income = self.calculate_cumulative_net_income()[0]
        total_quartal = self.calculate_cumulative_net_income()[1]
        roe = ((cumulative_net_income * (4/total_quartal))/(self.equity))*100

        return float(f'{roe:.2f}')
    
    def calculate_net_profit_margin(self):
        #Get Components
        cumulative_revenue = self.calculate_cumulative_revenue()[0]
        cummulative_net_income = self.calculate_cumulative_net_income()[0]

        #NPM Data
        npm = (cummulative_net_income/cumulative_revenue)*100

        return float(f'{npm:.2f}')

    def calculate_EPS(self):
        #Annulaization
        cumulative_net_income = self.calculate_cumulative_net_income()[0]
        total_quartal = self.calculate_cumulative_net_income()[1]
        eps = ((cumulative_net_income * (4/total_quartal))/(self.shares))

        return float(f'{eps:.2f}')
    
    def calculate_PER(self):
        #Get Historical Price
        historical_price = self.get_specific_historical_price()

        #Calculate Price Earning Ratio
        per = historical_price/(self.calculate_EPS())

        return float(f'{per:.2f}')