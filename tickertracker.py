import telepot

import nsehelper
import tickerstore


class TickerTracker(telepot.helper.ChatHandler):
    CHAT_ID_UNINITIALIZED = -1

    def __init__(self, *args, **kwargs):
        super(TickerTracker, self).__init__(*args, **kwargs)
        self._store = tickerstore.TickerStore()
        self._commands = ["/l", "/a", "/d", "/h"]
        self._callbacks = {}
        for command in self._commands:
            self._callbacks[command] = getattr(self, "on_" + command[1:])

    def send_wrapper(self, msg):
        # pylint: disable=no-member
        self.sender.sendMessage(msg)

    def on_h(self):
        self.send_wrapper(
            """Commands -
/l - list ticker collection
/a - append to ticker collection
/d - delete from ticker collection"""
        )

    def on_l(self, chat_id, msg_tokens):
        if len(msg_tokens) != 1:
            self.send_wrapper("invalid syntax")
            return
        if self._store.len(chat_id):
            self.send_wrapper(nsehelper.get_output(self._store.get()))

    def on_a(self, chat_id, msg_tokens):
        if len(msg_tokens) != 2:
            self.send_wrapper("invalid syntax")
            return
        if not nsehelper.is_valid_code(msg_tokens[1]):
            self.send_wrapper("invalid ticker")
            return
        self._store.put(msg_tokens[1].upper())
        self.send_wrapper(nsehelper.get_output(self._store.get()))

    def on_d(self, chat_id, msg_tokens):
        if len(msg_tokens) != 2:
            self.send_wrapper("invalid syntax")
            return
        if not nsehelper.is_valid_code(msg_tokens[1]):
            self.send_wrapper("invalid ticker")
            return
        if not self._store.exists(msg_tokens[1].upper()):
            self.send_wrapper("non-existent ticker")
            return
        self._store.remove(chat_id, msg_tokens[1].upper())
        if self._store.len(chat_id):
            self.send_wrapper(nsehelper.get_output(self._store.get()))

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
        print(chat_id, msg_text)
        msg_tokens = msg_text.split()
        if msg_tokens[0] not in self._commands:
            self.on_h()
            return
        self._callbacks[msg_tokens[0]](chat_id, msg_tokens)

    def on__idle(self, event):
        # commit to the db on idle event
        self._store.commit_tickers()
