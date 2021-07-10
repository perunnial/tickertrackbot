import yfinance as yf


def get_quote(ticker):
    ticker += ".NS"
    return yf.Ticker(ticker).info


def is_valid_code(ticker):
    ticker += ".NS"
    try:
        curr_price = yf.Ticker(ticker).info["currentPrice"]
    except:
        return False
    return True


def get_output(tickers):
    output = ""
    for ticker in tickers:
        output += ticker + " "
        quote = {}
        quote = get_quote(ticker)
        curr_price = quote["currentPrice"]
        prev_close = quote["previousClose"]
        pct_change = "{:.2f}".format(100 * (curr_price - prev_close) / prev_close)
        direction = "↑" if pct_change[0] != "-" else "↓"
        output += (
            "{:.2f}".format(curr_price) + " " + direction + " " + pct_change + "%\n"
        )
    return output
