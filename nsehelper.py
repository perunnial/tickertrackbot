import yfinance as yf

CRORE = 100 * 100 * 1000
PD_MAX_ROWS = 10


def get_ticker(ticker):
    ticker += ".NS"
    return yf.Ticker(ticker)


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
    info_text = get_output([ticker])
    info_text += "    " + quote["longName"] + "\n"
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
        "    Day's Range : "
        + "{0:,.2f}".format(quote["regularMarketDayLow"])
        + " - "
        + "{0:,.2f}".format(quote["regularMarketDayHigh"])
        + "\n"
    )
    info_text += (
        "    52 Week Range : "
        + "{0:,.2f}".format(quote["fiftyTwoWeekLow"])
        + " - "
        + "{0:,.2f}".format(quote["fiftyTwoWeekHigh"])
        + "\n"
    )
    info_text += "    Volume : " + "{:,d}".format(quote["regularMarketVolume"]) + "\n"
    return info_text


def get_description(ticker):
    quote = {}
    quote = get_quote(ticker)
    return quote["longBusinessSummary"]


def get_logo_url(ticker):
    quote = {}
    quote = get_quote(ticker)
    return quote["logo_url"]


def get_history(ticker):
    ticker_object = get_ticker(ticker)
    hist = ticker_object.history(period="5d", actions=False)
    hist = hist.reset_index()
    response = f"-----{ticker}-----\n"
    for index, row in hist.iterrows():
        price = "{0:,.2f}".format(row["Close"])
        format_date = row["Date"].strftime("%Y/%m/%d")
        response += f"{format_date}: {price}\n"
    return response


def get_dividends(ticker):
    ticker_object = get_ticker(ticker)
    dividends = ticker_object.dividends
    return dividends.to_string(header=False, max_rows=PD_MAX_ROWS)


def get_splits(ticker):
    ticker_object = get_ticker(ticker)
    splits = ticker_object.splits
    return splits.to_string(header=False, max_rows=PD_MAX_ROWS)


def get_sustainability(ticker):
    ticker_object = get_ticker(ticker)
    sustainability = ticker_object.sustainability
    # TODO catch NoneType exceptions
    sustainability = sustainability.reset_index()
    e = 0
    s = 0
    g = 0
    t = 0
    p = 0
    c = 0
    for index, row in sustainability.iterrows():
        if row[0] == "environmentScore":
            e = row[1]
        elif row[0] == "socialScore":
            s = row[1]
        elif row[0] == "governanceScore":
            g = row[1]
        elif row[0] == "totalEsg":
            t = row[1]
        elif row[0] == "percentile":
            p = row[1]
        elif row[0] == "highestControversy":
            c = row[1]
    response = f"-----{ticker}-----\n"
    response += (
        "    Total ESG Risk score : "
        + str(round(t))
        + " ("
        + str(round(p))
        + "th percentile)\n"
    )
    response += "    Environment Risk Score : " + str(round(e, 1)) + "\n"
    response += "    Social Risk Score : " + str(round(s, 1)) + "\n"
    response += "    Governance Risk Score : " + str(round(g, 1)) + "\n"
    response += "    Controversy Level : " + str(round(c, 1)) + "\n"
    return response
