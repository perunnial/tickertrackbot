import os
import time

from dotenv import load_dotenv
import telepot
from telepot.loop import MessageLoop
from nsetools import Nse

load_dotenv()
bot = telepot.Bot(os.environ['BOT_TOKEN'])
nse = Nse()

def handle(msg):
    # pylint: disable=unbalanced-tuple-unpacking
    content_type, chat_type, chat_id = telepot.glance(msg)
    response = 'unknown!'
    if chat_type == 'private' and content_type == 'text':
        msg_text = msg['text']
        print(chat_id, msg_text)
        if msg_text == '/start':
            response = 'hello!'
        elif not nse.is_valid_code(msg_text):
            response = 'invalid!'
        else:
            quote = nse.get_quote(msg_text)
            last_price = quote['lastPrice']
            if last_price:
                prev_close = quote['previousClose']
                pct_change = 100 * (last_price - prev_close) / prev_close
                direction = '↑' if pct_change > 0 else '↓'
                # avoiding percent change available as quote['pChange']
                # it is a float for positive values, str for negative values
                response = '{:.2f}'.format(last_price) + ' ' + direction + ' ' + '{:.2f}'.format(pct_change) + '%'
            else:
                response = 'unknown!'
    print(response)
    bot.sendMessage(chat_id, response)

MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(10)