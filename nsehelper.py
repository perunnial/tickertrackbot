import yfinance as yf

CRORE = 100 * 100 * 1000


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


def get_summary(ticker):
    quote = {}
    quote = get_quote(ticker)
    info_text = quote["longName"] + "\n"
    info_text += "    Sector : " + quote["sector"] + "\n"
    info_text += "    Industry : " + quote["industry"] + "\n"
    info_text += (
        "    Market Cap : "
        + "{:,d}".format(int(quote["marketCap"] / CRORE))
        + " crores\n"
    )
    info_text += "    Beta (5Y monthly) : " + "{:.2f}".format(quote["beta"]) + "\n"
    info_text += "    PE (TTM) : " + "{:.2f}".format(quote["trailingPE"]) + "\n"
    info_text += "    EPS (TTM) : " + "{:.2f}".format(quote["trailingEps"]) + "\n"
    info_text += (
        "    Forward Dividend Yield : "
        + "{:.2f}".format(100 * float(quote["dividendYield"]))
        + "%\n"
    )
    info_text += (
        "    Previous Close : "
        + "{:.2f}".format(quote["regularMarketPreviousClose"])
        + "\n"
    )
    info_text += "    Open : " + "{:.2f}".format(quote["regularMarketOpen"]) + "\n"
    info_text += (
        "    Day's Range : "
        + "{:.2f}".format(quote["regularMarketDayLow"])
        + " - "
        + "{:.2f}".format(quote["regularMarketDayHigh"])
        + "\n"
    )
    info_text += (
        "    52 Week Range : "
        + "{:.2f}".format(quote["fiftyTwoWeekLow"])
        + " - "
        + "{:.2f}".format(quote["fiftyTwoWeekHigh"])
        + "\n"
    )
    info_text += "    Volume : " + "{:,d}".format(quote["regularMarketVolume"]) + "\n"
    info_text += "    Average Volume : " + "{:,d}".format(quote["averageVolume"]) + "\n"
    return info_text
