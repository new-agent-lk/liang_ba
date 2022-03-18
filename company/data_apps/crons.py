# 静态化首页
import os
import requests
from datetime import datetime
import chinese_calendar

# from django.conf import settings
#
from data_apps.models import GenericStockMarketData

rq = requests.session()


def get_daily_stock_data():
    """
    生成静态的主页html文件
    """
    print('%s: get_daily_stock_data' % datetime.now())
    now = datetime.now()
    if chinese_calendar.is_workday(now):
        url = 'http://hq.sinajs.cn/?format=text&list=sz399001'
        try:
            r = rq.get(url, headers={"Referer": "https://finance.sina.com.cn"}, timeout=300, verify=False)
            meta_string = r.text
            stock_code, stock_string, *_ = r.text.split('=')
            # print(stock_string.split(','))
            stock_name, open_price, close_price, now_price, high_price, low_price, *_ = stock_string.split(',')
            turnover_of_shares = stock_string.split(',')[8]
            trading_volume = stock_string.split(',')[9]
            d = stock_string.split(',')[-3]
            t = stock_string.split(',')[-2]
            current_time = datetime.strptime(f'{d} {t}', "%Y-%m-%d %H:%M:%S")

            GenericStockMarketData.objects.get_or_create()
            print(current_time)
            print(turnover_of_shares, trading_volume, d, t)

        except requests.RequestException:
            pass


if __name__ == '__main__':
    get_daily_stock_data()
