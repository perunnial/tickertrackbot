from nsetools import Nse

import urllib
import json


nse = Nse()


def get_quote(ticker):
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


def is_valid_code(ticker):
    return nse.is_valid_code(ticker)
