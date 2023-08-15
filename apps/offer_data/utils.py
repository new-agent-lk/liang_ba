from dataclasses import dataclass
from tracemalloc import start
import requests
from decimal import Decimal
from datetime import datetime

from django.core.cache import cache


requests.packages.urllib3.disable_warnings()
rq = requests.session()


def get_two_float(f_str, n):
    f_str = str(f_str)     
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]
    return ".".join([a, c])


def merge_tensc_data(stock_portfolio, length=0):
    pass


def count_rate(stock_portfolio, couple_key=None):
    _stock_dict = {}
    for stock_code, weight in stock_portfolio.items():
        url = f'https://img1.money.126.net/data/hs/kline/day/history/{datetime.now().year}/{stock_code}.json'
        try:
            # key = f'{stock_code}_hs_{datetime.now().year-1}'
            # data = cache.get(key)
            # if not data:
            #     resp = rq.get(f'https://img1.money.126.net/data/hs/kline/day/history/{datetime.now().year-1}/{stock_code}.json')
            #     data = resp.json().get('data')
            #     cache.set(key, data)

            r = rq.get(url, timeout=300, verify=False)
            resp_data = r.json()
        except Exception as e:
            print(e)
            data = {}
            resp_data = {}  
        if resp_data:
            _datas = resp_data.get('data')
            # _datas = data + _datas
            for time_str, open, close, high, low, *_ in _datas:
                if time_str in _stock_dict:
                    _stock_dict[time_str]['open'] += Decimal(get_two_float(Decimal(open) * Decimal(weight), 2))
                    _stock_dict[time_str]['close'] += Decimal(get_two_float(Decimal(close) * Decimal(weight), 2))
                    _stock_dict[time_str]['high'] += Decimal(get_two_float(Decimal(high) * Decimal(weight), 2))
                    _stock_dict[time_str]['low'] += Decimal(get_two_float(Decimal(low) * Decimal(weight), 2))
                    _stock_dict[time_str]['count'] += 1
                else:
                    _stock_dict[time_str] = {
                        'open': Decimal(get_two_float(Decimal(open) * Decimal(weight), 2)),
                        'close': Decimal(get_two_float(Decimal(close) * Decimal(weight), 2)),
                        'high': Decimal(get_two_float(Decimal(high) * Decimal(weight), 2)),
                        'low': Decimal(get_two_float(Decimal(low) * Decimal(weight), 2)),
                        'count': 1
                    }
    data_set = []
    for key, value in _stock_dict.items():
        if value.get('count') != len(stock_portfolio.keys()):
            continue
        data_set.append([key, float(value.get('open')), float(value.get('close')), float(value.get('high')), float(value.get('low'))])
    print(data_set)
    price_list = [d[1] for d in data_set]
    # print(price_list)
    low_price = 0
    if price_list:
        low_price = min(price_list)
    start_date, start_price, *_ = data_set[0]
    last_date, last_price, *_ = data_set[-1]

    difference = start_price - low_price
    if difference > 0:
        retreat_rate = difference / start_price
    elif difference < 0:
        retreat_rate = -difference / start_price
    else:
        retreat_rate = 0
    
    annual_yield = (last_price - start_price) / start_price

    return annual_yield, retreat_rate


