import os
import telepot
import schedule
from dotenv import load_dotenv

import nsehelper
import tickerstore


class TickerTracker(telepot.helper.ChatHandler):
    CHAT_ID_UNINITIALIZED = -1

    def __init__(self, *args, **kwargs):
        super(TickerTracker, self).__init__(*args, **kwargs)
        self._store = tickerstore.TickerStore()
        self._scheduled = False
        load_dotenv()
        if os.environ["TT_ENVIRONMENT"] == "local":
            self.market_close_time = "15:30"
        else:
            self.market_close_time = "10:00"  # heroku timezone is UTC
        self._commands = [
            "/list",
            "/add",
            "/delete",
            "/description",
            "/summary",
            "/history",
            "/dividends",
            "/splits",
            "/sustainability",
        ]
        self._callbacks = {}
        for command in self._commands:
            self._callbacks[command] = getattr(self, "on_" + command[1:])

    def send_wrapper(self, msg):
        # pylint: disable=no-member
        self.sender.sendMessage(msg)

    def on_h(self):
        self.send_wrapper(
            """Commands -
/list - List portfolio
/add - Add a ticker to portfolio
/delete - Delete a ticker from portfolio
/description - Get ticker description
/summary - Get ticker summary
/history - Get ticker history
/dividends - Get ticker dividends
/splits - Get ticker splits
/sustainability - Get ticker sustainability"""
        )

    def on_list(self, chat_id, msg_tokens):
        if self._store.len(chat_id):
            self.send_wrapper(nsehelper.get_output(self._store.get()))

    def on_add(self, chat_id, msg_tokens):
        if len(msg_tokens) != 2:
            self.send_wrapper("Invalid syntax. Usage : /<command> <ticker>")
            return
        if not nsehelper.is_valid_code(msg_tokens[1]):
            self.send_wrapper("Invalid ticker : " + msg_tokens[1])
            return
        self._store.put(msg_tokens[1].upper())
        self.send_wrapper(nsehelper.get_output(self._store.get()))

    def on_delete(self, chat_id, msg_tokens):
        if len(msg_tokens) != 2:
            self.send_wrapper("Invalid syntax. Usage : /<command> <ticker>")
            return
        if not nsehelper.is_valid_code(msg_tokens[1]):
            self.send_wrapper("Invalid ticker : " + msg_tokens[1])
            return
        if not self._store.exists(msg_tokens[1].upper()):
            self.send_wrapper("Ticker (" + msg_tokens[1].upper() + ") not in portfolio")
            return
        self._store.remove(chat_id, msg_tokens[1].upper())
        if self._store.len(chat_id):
            self.send_wrapper(nsehelper.get_output(self._store.get()))

    def on_description(self, chat_id, msg_tokens):
        if len(msg_tokens) != 2:
            self.send_wrapper("Invalid syntax. Usage : /<command> <ticker>")
            return
        if not nsehelper.is_valid_code(msg_tokens[1]):
            self.send_wrapper("Invalid ticker : " + msg_tokens[1])
            return
        # pylint: disable=no-member
        self.sender.sendPhoto(nsehelper.get_logo_url(msg_tokens[1].upper()))
        self.send_wrapper(nsehelper.get_description(msg_tokens[1].upper()))

    def on_summary(self, chat_id, msg_tokens):
        if len(msg_tokens) != 2:
            self.send_wrapper("Invalid syntax. Usage : /<command> <ticker>")
            return
        if not nsehelper.is_valid_code(msg_tokens[1]):
            self.send_wrapper("Invalid ticker : " + msg_tokens[1])
            return
        self.send_wrapper(nsehelper.get_summary(msg_tokens[1].upper()))

    def on_history(self, chat_id, msg_tokens):
        if len(msg_tokens) != 2:
            self.send_wrapper("Invalid syntax. Usage : /<command> <ticker>")
            return
        if not nsehelper.is_valid_code(msg_tokens[1]):
            self.send_wrapper("Invalid ticker : " + msg_tokens[1])
            return
        self.send_wrapper(nsehelper.get_history(msg_tokens[1].upper()))

    def on_dividends(self, chat_id, msg_tokens):
        if len(msg_tokens) != 2:
            self.send_wrapper("Invalid syntax. Usage : /<command> <ticker>")
            return
        if not nsehelper.is_valid_code(msg_tokens[1]):
            self.send_wrapper("Invalid ticker : " + msg_tokens[1])
            return
        self.send_wrapper(nsehelper.get_dividends(msg_tokens[1].upper()))

    def on_splits(self, chat_id, msg_tokens):
        if len(msg_tokens) != 2:
            self.send_wrapper("Invalid syntax. Usage : /<command> <ticker>")
            return
        if not nsehelper.is_valid_code(msg_tokens[1]):
            self.send_wrapper("Invalid ticker : " + msg_tokens[1])
            return
        self.send_wrapper(nsehelper.get_splits(msg_tokens[1].upper()))

    def on_sustainability(self, chat_id, msg_tokens):
        if len(msg_tokens) != 2:
            self.send_wrapper("Invalid syntax. Usage : /<command> <ticker>")
            return
        if not nsehelper.is_valid_code(msg_tokens[1]):
            self.send_wrapper("Invalid ticker : " + msg_tokens[1])
            return
        self.send_wrapper(nsehelper.get_sustainability(msg_tokens[1].upper()))

    def on_chat_message(self, msg):
        # pylint: disable=unbalanced-tuple-unpacking
        content_type, chat_type, chat_id = telepot.glance(msg)
        if chat_type != "private" or content_type != "text":
            self.on_h()
            return
        msg_text = msg["text"].lower()
        # fetch from db if chat id is uninitialized
        if self._store.chat_id() == self.CHAT_ID_UNINITIALIZED:
            self._store.fetch_tickers(chat_id)
            # schedule market close notification job after chat is initiated
            if not self._scheduled:
                # schedule only on weekdays
                # still could be a holiday and markets could be closed
                schedule.every().monday.at(self.market_close_time).do(
                    self.on_market_close
                )
                schedule.every().tuesday.at(self.market_close_time).do(
                    self.on_market_close
                )
                schedule.every().wednesday.at(self.market_close_time).do(
                    self.on_market_close
                )
                schedule.every().thursday.at(self.market_close_time).do(
                    self.on_market_close
                )
                schedule.every().friday.at(self.market_close_time).do(
                    self.on_market_close
                )
                self._scheduled = True
        print(chat_id, msg_text)
        msg_tokens = msg_text.split()
        if msg_tokens[0] not in self._commands:
            self.on_h()
            return
        self._callbacks[msg_tokens[0]](chat_id, msg_tokens)

    def on_market_close(self):
        if self._store.len(self._store.chat_id()):
            self.send_wrapper("** Market Close **")
            self.send_wrapper(nsehelper.get_output(self._store.get()))

    def on__idle(self, event):
        # commit to the db on idle event
        self._store.commit_tickers()
