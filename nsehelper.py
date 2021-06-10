from nsetools import Nse

import urllib
import json


nse = Nse()


def get_quote(ticker):
    try:
        quote = nse.get_quote(ticker)
        return quote
    except urllib.error.HTTPError as exception:
        print("HTTPError")
        print(exception)
    except (urllib.error.URLError):
        print("URLError")
    except (json.decoder.JSONDecodeError):
        print("JSONDecodeError")
    except:
        print("Exception")
    return None


def get_index_quote(ticker):
    try:
        quote = nse.get_index_quote(ticker)
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


def is_valid_code(ticker):
    return nse.is_valid_code(ticker)


def get_output(tickers, is_index=False):
    output = ""
    for ticker in tickers:
        output += ticker + " "
        quote = {}
        if is_index:
            quote = get_index_quote(ticker)
        else:
            quote = get_quote(ticker)
        last_price = quote["lastPrice"]
        pct_change = str(quote["pChange"])
        direction = "↑" if pct_change[0] != "-" else "↓"
        output += (
            "{:.2f}".format(last_price) + " " + direction + " " + pct_change + "%\n"
        )
    return output
