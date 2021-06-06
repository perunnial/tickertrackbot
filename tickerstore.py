class TickerStore:
    def __init__(self):
        self._db = {}

    def get(self, chat_id):
        if chat_id not in self._db:
            return []
        tickers = self._db[chat_id]
        return list(tickers)

    def put(self, chat_id, ticker):
        if chat_id not in self._db:
            self._db[chat_id] = set()
        self._db[chat_id].add(ticker)

    def exists(self, chat_id, ticker):
        if chat_id not in self._db:
            return False
        return ticker in self._db[chat_id]

    def remove(self, chat_id, ticker):
        if chat_id in self._db:
            self._db[chat_id].remove(ticker)

    def len(self, chat_id):
        if chat_id not in self._db:
            return 0
        return len(self._db[chat_id])
