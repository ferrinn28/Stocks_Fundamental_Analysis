from yahooquery import Ticker
#tickers = Ticker('BMRI.JK')

# Default period = ytd, interval = 1d
#df = tickers.history()
#print(df.head())

class Data(object):
    def __init__(self, ticker):
        code = ".".join([ticker, "JK"])
        self.query = Ticker(code)

    def get_balance_sheet_quarter(self):
        return(self.query.balance_sheet("q"))

    def get_balance_sheet_annual(self):
        return(self.query.balance_sheet("a"))
    
    def get_history_price(self, period="ytd", interval="1d", start=None, end=None):
        return(self.query.history(period=period, interval=interval, start=start, end=end))