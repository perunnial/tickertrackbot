import os
import time

from dotenv import load_dotenv
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space
import schedule

import tickertracker

load_dotenv()
bot = telepot.DelegatorBot(
    os.environ["TT_BOT_TOKEN"],
    [
        pave_event_space()(
            per_chat_id(),
            create_open,
            tickertracker.TickerTracker,
            timeout=300,
        ),
    ],
)


MessageLoop(bot).run_as_thread()
while True:
    schedule.run_pending()  # poll for market close job
    time.sleep(10)
