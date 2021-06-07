class TickerStore:
    CHAT_ID_UNINITIALIZED = -1

    def __init__(self):
        self._chat_id = self.CHAT_ID_UNINITIALIZED
        self._tickers = set()

    def fetch_tickers(self, chat_id):
        self._chat_id = chat_id

    def commit_tickers(self):
        return

    def get(self):
        return list(self._tickers)

    def put(self, ticker):
        self._tickers.add(ticker)

    def exists(self, ticker):
        return ticker in self._tickers

    def remove(self, chat_id, ticker):
        self._tickers.remove(ticker)

    def len(self, chat_id):
        return len(self._tickers)
