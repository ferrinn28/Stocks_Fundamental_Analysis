from yahooquery import Ticker
import pandas as pd

# Query Data for Specific Ticker
class QueryData:
    def __init__(self, ticker):
        self.ticker = ticker
        code = ".".join([ticker, "JK"])
        self.query = Ticker(code.upper())

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
    
    def get_basic_info(self):
        basic_data = self.query.asset_profile
        additional_data = self.query.quote_type
        ticker_code = ".".join([self.ticker, "JK"])

        # Get Sector, Industry, Website, and Country
        basic_info = {
            "Name": f"{additional_data[ticker_code]['longName']}",
            "Code": f"{self.ticker}",
            "Sector": f"{basic_data[ticker_code]['sector']}",
            "Industry": f"{basic_data[ticker_code]['industry']}",
            "Website": f"{basic_data[ticker_code]['website']}",
            "Country": f"{basic_data[ticker_code]['country']}"
        }

        return basic_info