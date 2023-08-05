from .query_data import QueryData
import pandas as pd

# Calculate Annual Fundamental Data
class CalculateAnnual(QueryData):
    def __init__(self, ticker, date_input):
        super().__init__(ticker)
        self.balance_sheet_annual = self.get_balance_sheet_annual()
        self.income_statement_annual = self.get_income_statement_annual()
        self.input_date = pd.to_datetime(date_input)

        # Gets Date Component (Year, Month, Date)
        self.year = self.input_date.year
        self.month = self.input_date.month
        self.day = self.input_date.day

        # Always Used Components
        ## Select Row Based on User Date Input
        rows = self.balance_sheet_annual[self.balance_sheet_annual["asOfDate"] == self.input_date]
        self.equity = rows["StockholdersEquity"][0]
        self.shares = rows["ShareIssued"][0]

        ## Collect 1 Month Historical Price
        self.historical_price = self.get_history_price(period="1mo", interval="1d", 
                                                       start=f"{self.year}-{self.month}-1", end=f"{self.year}-{self.month}-{self.day}")
        
        ## Select Annual Income in Specific Year Based on User Input Date
        selected_income_statement = self.income_statement_annual[(self.income_statement_annual["asOfDate"].dt.year == self.year) 
                                                                 & (self.income_statement_annual["periodType"] == "12M")]
        
        ### Revenue in Period of Time
        self.revenue = selected_income_statement["TotalRevenue"][0]

        ## Net Income in Period of Time
        self.net_income = selected_income_statement["NetIncomeCommonStockholders"][0]
        
    def get_specific_historical_price(self):
        # Change Date Index into New Column
        historical_price = self.historical_price.reset_index()
        historical_price["date"] = pd.to_datetime(historical_price["date"])
        
        # Check If on Specific Date has a Value
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
        # Book Value Data
        bv = (self.equity/self.shares)

        return int(bv)
    
    def calculate_price_book_value(self):
        # Get Historical Price
        historical_price = self.get_specific_historical_price()

        # Price Book Ratio Data
        pbv = historical_price/(self.calculate_book_value())

        return float(f"{pbv:.2f}")

    def calculate_roe(self):
        # Retrun on Equity Data
        roe = ((self.net_income)/(self.equity))*100

        return float(f"{roe:.2f}")
    
    def calculate_net_profit_margin(self):
        # Net Profit Margin Data
        npm = (self.net_income/self.revenue)*100

        return float(f"{npm:.2f}")

    def calculate_eps(self):
        # Earning per Shares Data
        eps = ((self.net_income)/(self.shares))

        return float(f"{eps:.2f}")
    
    def calculate_per(self):
        # Get Historical Price
        historical_price = self.get_specific_historical_price()

        # Calculate Price Earning Ratio
        per = historical_price/(self.calculate_eps())

        return float(f"{per:.2f}")
    
    def output(self):
        # Return Fundamentals Calculations
        data_fundamentals = {
            "Code": f"{self.ticker}",
            "Type Report": f"{self.ticker}-ANN-{self.year}",
            "Date": self.input_date.strftime("%Y-%m-%d"),
            "Fundamental Data": {
                "Cumulative Revenue": self.revenue,                   # In Rupiah
                "Cumulative Net Income": self.net_income,             # In Rupiah
                "BV": self.calculate_book_value(),                    # In Rupiah
                "PBV": self.calculate_price_book_value(),
                "NPM": self.calculate_net_profit_margin(),            # In %
                "ROE": self.calculate_roe(),                          # In %
                "EPS": self.calculate_eps(),                          # In Rupiah
                "PER": self.calculate_per()
            }
        }

        return data_fundamentals