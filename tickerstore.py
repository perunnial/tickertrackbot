import os
from dotenv import load_dotenv
import psycopg2


class TickerStore:
    CHAT_ID_UNINITIALIZED = -1

    def __init__(self):
        self._chat_id = self.CHAT_ID_UNINITIALIZED
        self._tickers = set()
        load_dotenv()

    def open_db(self):
        self._conn = psycopg2.connect(os.environ["TT_DATABASE_URL"])
        self._cur = self._conn.cursor()

    def close_db(self):
        self._conn.commit()
        self._cur.close()
        self._conn.close()

    def chat_id(self):
        return self._chat_id

    def fetch_tickers(self, chat_id):
        self._chat_id = chat_id
        # subsequent commands until idle event will work on in-memory data
        print("fetching...")
        try:
            self.open_db()
            self._cur.execute(
                "SELECT * FROM chatid_vs_tickers WHERE chatid = %s",
                [self._chat_id],
            )
            records = self._cur.fetchall()
            if len(records):
                self._tickers = set(records[0][1])
            print(self._tickers)
        finally:
            self.close_db()

    def commit_tickers(self):
        print("committing...")
        print(self._tickers)
        try:
            self.open_db()
            self._cur.execute(
                "INSERT INTO chatid_vs_tickers (chatid, tickers) VALUES (%s, %s) ON CONFLICT (chatid) DO NOTHING",
                (self._chat_id, list(self._tickers)),
            )
            self._cur.execute(
                "UPDATE chatid_vs_tickers SET tickers=(%s) WHERE chatid=(%s)",
                (list(self._tickers), self._chat_id),
            )
        finally:
            self.close_db()
        # set chat id to uninitialized so the next command fetches from db
        self._chat_id = self.CHAT_ID_UNINITIALIZED

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
