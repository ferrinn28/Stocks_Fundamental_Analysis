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