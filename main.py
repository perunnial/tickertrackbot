import os
import time

from dotenv import load_dotenv
import telepot
from telepot.loop import MessageLoop
from nsetools import Nse

import urllib
import json

load_dotenv()
bot = telepot.Bot(os.environ["BOT_TOKEN"])
nse = Nse()


def get_nse_quote(ticker):
    try:
        quote = nse.get_quote(ticker)
        return quote
    except (urllib.error.HTTPError):
        print("HTTPError")
    except (urllib.error.URLError):
        print("URLError")
    except (json.decoder.JSONDecodeError):
        print("JSONDecodeError")
    except:
        print("Exception")
    return None


def handle(msg):
    # pylint: disable=unbalanced-tuple-unpacking
    content_type, chat_type, chat_id = telepot.glance(msg)
    response = "unknown!"
    if chat_type == "private" and content_type == "text":
        msg_text = msg["text"]
        print(chat_id, msg_text)
        if msg_text == "/start":
            response = "hello!"
        elif not nse.is_valid_code(msg_text):
            response = "invalid!"
        else:
            quote = get_nse_quote(msg_text)
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
    bot.sendMessage(chat_id, response)


MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(10)
