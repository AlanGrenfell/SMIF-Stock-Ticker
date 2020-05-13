import PyRSS2Gen
from alpha_vantage.timeseries import TimeSeries
import time
from datetime import datetime
import config

api_key = config.api_key
symbols = ['ESYJY', 'IFNNY', 'LYG', 'PFE', 'RIO', 'TOT', 'DIS', 'BHE', 'DCMYY', 'NEE', 'CRM', 'BAX', 'BLK', 'COLD', 'EL']

ts = TimeSeries(key=api_key, output_format='pandas')

def ticker_func():
    stock_market = {}

    for sym in symbols:
        data, meta_data = ts.get_daily(symbol=sym, outputsize='compact')
        current_price = data.iloc[-1, 3]  # last available price
        day_prev_close = data.iloc[-2, 3]  # price at end of day previous
        daily_change_abs = (current_price-day_prev_close)
        daily_change_abs = (round(daily_change_abs, 2))
        if daily_change_abs > 0:
            stock_market[sym] = f"{current_price}(+{daily_change_abs})"
        else:
            stock_market[sym] = f"{current_price}({daily_change_abs})"
        time.sleep(12)
        # API allows 5 calls per minute, 60/5 = 12
    print('data updated at:', datetime.now().strftime('%c'))

    CHAR_EVEN = "="

    stock_list = []

    for sym in symbols:
        s = stock_market[sym]
        daily_change = s[s.find("(")+1:s.find(")")]
        if '+' in daily_change:
            direction = ''
        elif '-' in daily_change:
            direction = ''
        else:
            direction = CHAR_EVEN
        current_price = s.partition("(")[0]
        stock_list_str = " |  {} {} {} {} ".format(sym, current_price, direction, daily_change)
        stock_list.append(stock_list_str)

    string1 = ''.join(stock_list[0:len(stock_list)])
    print(string1)

    rss = PyRSS2Gen.RSS2(
        title="",
        link="",
        description="",

        lastBuildDate=datetime.now(),

        items=[PyRSS2Gen.RSSItem(
            title='',
            link="http://www.dalkescientific.com/news/030906-PyRSS2Gen.html",
            description=string1,
            guid=PyRSS2Gen.Guid("http://www.dalkescientific.com/news/"
                                "030906-PyRSS2Gen.html"),
            pubDate=datetime.now()),
        ])

    rss.write_xml(open("pyrss2gen.xml", "w", encoding="utf-8"))

while True:
    ticker_func()
    time.sleep(120) #wait 2 mins before re-running