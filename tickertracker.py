import telepot

import nsehelper


class TickerTracker(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(TickerTracker, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        # pylint: disable=unbalanced-tuple-unpacking
        content_type, chat_type, chat_id = telepot.glance(msg)
        response = "unknown!"
        if chat_type == "private" and content_type == "text":
            msg_text = msg["text"]
            print(chat_id, msg_text)
            if msg_text == "/start":
                response = "hello!"
            elif not nsehelper.is_valid_code(msg_text):
                response = "invalid!"
            else:
                quote = nsehelper.get_quote(msg_text)
                if quote is not None:
                    last_price = quote["lastPrice"]
                    pct_change = str(quote["pChange"])
                    direction = "↑" if pct_change[0] != "-" else "↓"
                    response = (
                        "{:.2f}".format(last_price)
                        + " "
                        + direction
                        + " "
                        + pct_change
                        + "%"
                    )
                else:
                    response = "unknown!"
        print(response)
        # pylint: disable=no-member
        self.sender.sendMessage(response)
