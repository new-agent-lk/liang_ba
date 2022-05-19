# 静态化首页
import os
import requests
import chinese_calendar

from datetime import datetime

from data_apps.models import GenericStockMarketData

rq = requests.session()


def get_on_work_time(now):
    # 范围时间
    a_time = datetime.strptime(str(datetime.now().date()) + '9:00', '%Y-%m-%d%H:%M')
    b_time = datetime.strptime(str(datetime.now().date()) + '11:30', '%Y-%m-%d%H:%M')
    c_time = datetime.strptime(str(datetime.now().date()) + '13:00', '%Y-%m-%d%H:%M')
    d_time = datetime.strptime(str(datetime.now().date()) + '15:00', '%Y-%m-%d%H:%M')
    # 判断当前时间是否在范围时间内
    if b_time > now > a_time or d_time > now > c_time:
        return True
    else:
        return False


def get_daily_stock_data():
    print('%s: get_daily_stock_data' % datetime.now())
    now = datetime.now()
    if chinese_calendar.is_workday(now):
        if get_on_work_time(now):
            print(f'现在是工作时间 {now}')
            url = 'http://hq.sinajs.cn/?format=text&list=sz399001'
            r = None
            try:
                r = rq.get(url, headers={"Referer": "https://finance.sina.com.cn"}, timeout=300, verify=False)
            except requests.RequestException:
                pass
            if r:
                meta_string = r.text
                stock_code, stock_string, *_ = r.text.split('=')
                stock_name, open_price, close_price, now_price, high_price, low_price, *_ = stock_string.split(',')
                turnover_of_shares = stock_string.split(',')[8]
                trading_volume = stock_string.split(',')[9]
                d = stock_string.split(',')[-3]
                t = stock_string.split(',')[-2]
                current_time = datetime.strptime(f'{d} {t}', "%Y-%m-%d %H:%M:%S")
                data = {
                    "stock_code": stock_code,
                    "stock_name": stock_name,
                    "now_price": now_price,
                    "open_price": open_price,
                    "close_price": close_price,
                    "high_price": high_price,
                    "low_price": low_price,
                    "turnover_of_shares": turnover_of_shares,
                    "trading_volume": trading_volume,
                    "current_time": current_time,
                    "source_data": meta_string,
                }
                print(f'获取到数据  {meta_string}')
                try:
                    gsmd, _ = GenericStockMarketData.objects.get_or_create(**data)
                    print(f'{now}  {gsmd.stock_code} now_price:{gsmd.now_price}')
                except Exception as e:
                    print(e)
        else:
            pass


def get_ten_stock_data():
    print('%s: get_ten_stock_data' % datetime.now())
    now = datetime.now()
    if chinese_calendar.is_workday(now):
        if get_on_work_time(now):
            codes = ['sh603185', 'sh603260', 'sh600196', 'sh600958', 'sh601878', 'sh600598', 'sz002594', 'sh688981', 'sz002371', 'sz002460']
            for code in codes:
                print(f'现在是工作时间 {now}, 股票代码为：{code}')
                url = 'http://hq.sinajs.cn/?format=text&list={}'.format(code)
                r = None
                try:
                    r = rq.get(url, headers={"Referer": "https://finance.sina.com.cn"}, timeout=300, verify=False)
                except requests.RequestException:
                    print(f'{code} 获取失败')
                    pass
                if r:
                    meta_string = r.text
                    stock_code, stock_string, *_ = r.text.split('=')
                    stock_name, open_price, close_price, now_price, high_price, low_price, *_ = stock_string.split(',')
                    turnover_of_shares = stock_string.split(',')[8]
                    trading_volume = stock_string.split(',')[9]
                    d = stock_string.split(',')[-3]
                    t = stock_string.split(',')[-2]
                    current_time = datetime.strptime(f'{d} {t}', "%Y-%m-%d %H:%M:%S")
                    data = {
                        "stock_code": stock_code,
                        "stock_name": stock_name,
                        "now_price": now_price,
                        "open_price": open_price,
                        "close_price": close_price,
                        "high_price": high_price,
                        "low_price": low_price,
                        "turnover_of_shares": turnover_of_shares,
                        "trading_volume": trading_volume,
                        "current_time": current_time,
                        "source_data": meta_string,
                    }
                    print(f'获取到数据  {meta_string}')
                    try:
                        gsmd, _ = GenericStockMarketData.objects.create(**data)
                        print(f'{now}  {gsmd.stock_code} now_price:{gsmd.now_price}')
                    except Exception as e:
                        print(e)
        else:
            pass