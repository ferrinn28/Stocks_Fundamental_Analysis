from .query_data import QueryData
import pandas as pd

# Calculate Quarter Fundamental Data
class CalculateQuarter(QueryData):
    def __init__(self, ticker, date_input):
        super().__init__(ticker)
        self.balance_sheet_quartal = self.get_balance_sheet_quarter()
        self.income_statement_quartal = self.get_income_statement_quarter()
        self.input_date = pd.to_datetime(date_input)

        # Gets Date Component (Year, Month, Date)
        self.year = self.input_date.year
        self.month = self.input_date.month
        self.day = self.input_date.day

        # Always Used Components
        ## Collect 1 Month Historical Price
        self.historical_price = self.get_history_price(period="1mo", interval="1d", 
                                                  start=f"{self.year}-{self.month}-1", end=f"{self.year}-{self.month}-{self.day}")
        
        ## Select Some Quartals in a Year Based on User Input Date
        selected_income_statement = self.income_statement_quartal[(self.income_statement_quartal["asOfDate"].dt.year == self.year) 
                                                           & (self.income_statement_quartal["asOfDate"].dt.month <= self.month)
                                                           & (self.income_statement_quartal["periodType"] == "3M")]
        ### Check Total Quartal
        total_of_quartal = selected_income_statement.shape
        self.quartal = total_of_quartal[0]
        
        ## Select Row Based on User Date Input
        rows = self.balance_sheet_quartal[self.balance_sheet_quartal["asOfDate"] == self.input_date]
        self.shares = rows["ShareIssued"].iloc[0]

        # Check Financial Currency USD or IDR?
        if self.currency_type == "IDR":
            self.equity = rows["StockholdersEquity"].iloc[0]

            ### Sum All Revenue in Period of Time
            self.cumulative_revenue = selected_income_statement["TotalRevenue"].sum()

            # Sum All Net Income in Period of Time
            self.cumulative_net_income = selected_income_statement["NetIncomeCommonStockholders"].sum()

        elif self.currency_type == "USD":
            # Get USDIDR Value
            data_usdidr = self.get_usd_idr_value(start=f"{self.year}-{self.month}-{self.day}")
            price_usdidr = data_usdidr["adjclose"].iloc[0]

            self.equity = (rows["StockholdersEquity"].iloc[0])*price_usdidr

            ### Sum All Revenue in Period of Time
            self.cumulative_revenue = (selected_income_statement["TotalRevenue"].sum())*price_usdidr

            # Sum All Net Income in Period of Time
            self.cumulative_net_income = (selected_income_statement["NetIncomeCommonStockholders"].sum())*price_usdidr

    def get_specific_historical_price(self):
        # Change Date Index into New Column
        historical_price = self.historical_price.reset_index()
        historical_price["date"] = pd.to_datetime(historical_price["date"])
        
        # Check If Specific Date has a Value
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
        # Annualization
        cumulative_net_income = self.cumulative_net_income
        total_quartal = self.quartal

        # Return of Equity Data
        roe = ((cumulative_net_income * (4/total_quartal))/(self.equity))*100

        return float(f"{roe:.2f}")
    
    def calculate_net_profit_margin(self):
        # Get Components
        cumulative_revenue = self.cumulative_revenue
        cummulative_net_income = self.cumulative_net_income

        # Net Profit Margin Data
        npm = (cummulative_net_income/cumulative_revenue)*100

        return float(f"{npm:.2f}")

    def calculate_eps(self):
        # Annulaization
        cumulative_net_income = self.cumulative_net_income
        total_quartal = self.quartal
        
        # Earning per Shares Data
        eps = ((cumulative_net_income * (4/total_quartal))/(self.shares))

        return float(f"{eps:.2f}")
    
    def calculate_per(self):
        # Get Historical Price
        historical_price = self.get_specific_historical_price()

        # Calculate Price Earning Ratio
        per = historical_price/(self.calculate_eps())

        return float(f"{per:.2f}")
    
    def check_quarter_value(self):
        q1 = [1, 2, 3]
        q2 = [4, 5, 6]
        q3 = [7, 8, 9]
        q4 = [10, 11, 12]
        
        if self.month in q1:
            return "Q1"
        elif self.month in q2:
            return "Q2"
        elif self.month in q3:
            return "Q3"
        elif self.month in q4:
            return "Q4"
    
    def output(self):
        # Return Fundamentals Calculations
        data_fundamentals = {
            "Code": f"{self.ticker}",
            "Type Report": f"{self.ticker}-{self.check_quarter_value()}-{self.year}",
            "Date": self.input_date.strftime("%Y-%m-%d"),
            "Fundamental Data": {
                "Cumulative Revenue": self.cumulative_revenue,                  # In Rupiah
                "Cumulative Net Income": self.cumulative_net_income,            # In Rupiah
                "BV": self.calculate_book_value(),                              # In Rupiah
                "PBV": self.calculate_price_book_value(),
                "NPM": self.calculate_net_profit_margin(),                      # In %
                "ROE": self.calculate_roe(),                                    # In %
                "EPS": self.calculate_eps(),                                    # In Rupiah
                "PER": self.calculate_per()
            }
        }

        return data_fundamentals