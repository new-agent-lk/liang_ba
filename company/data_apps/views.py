from dis import code_info
from ossaudiodev import control_labels
import chinese_calendar
import requests
from decimal import Decimal
from datetime import date, datetime
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import Http404
# Create your views here.

from data_apps.models import GenericStockMarketData
from data_apps.crons import get_on_work_time
from data_apps.serializers.generic_stock_market_data import GenericStockMarketDataSerializer

from .utils import get_two_float

requests.packages.urllib3.disable_warnings()
rq = requests.session()


class GenericStockMarketView(APIView):
    """
    返回 一串 股票数据
    """
    permission_classes = (AllowAny, )

    def get(self, request):
        stock_codes = request.query_params.get("stock_codes", "sz399001")
        stock_codes_list = stock_codes.split(',')
        result = {}
        for code in stock_codes_list:
            url = 'http://hq.sinajs.cn/list={}'.format(code)
            try:
                r = rq.get(url, headers={"Referer": "https://finance.sina.com.cn"}, timeout=300, verify=False)
                result[code] = r.json()
            except Exception as e:
                result[code] = ""
        return Response(result)


class GenericHistoryStockMarketView(APIView):
    """
    返回当前股票历史数据
    """
    permission_classes = (AllowAny, )

    def get(self, request):
        stock_codes = request.query_params.get("stock_codes", "sz399001")
        stock_codes_list = stock_codes.split(',')
        result = {}
        for code in stock_codes_list:
            url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={}&scale=5&ma=5&datalen=1023'.format(code)
            try:
                r = rq.get(url, timeout=300, verify=False)
                result[code] = r.json()
            except Exception as e:
                result[code] = ""
        return Response(result)


class CurrentStockCodeView(APIView):
    """
    返回当前股票数据
    """
    permission_classes = (AllowAny, )

    def get(self, request, stock_code):
        now = datetime.now()
        offset = timedelta(minutes=2)
        hgsmd = GenericStockMarketData.objects.filter(stock_code=stock_code, current_time__gte=datetime.now().date())
        if chinese_calendar.is_workday(now) and get_on_work_time(now):
            gsmd = GenericStockMarketData.objects.filter(stock_code=stock_code, current_time__range=(now-offset, now)).order_by('-id').first()
            if gsmd:
                data = {
                    'is_work_time': True,
                    'data': GenericStockMarketDataSerializer(gsmd).data,
                    'today_data': GenericStockMarketDataSerializer(hgsmd, many=True).data,
                    'info': 'ok'
                }
            else:
                data = {
                    'is_work_time': True,
                    'info': '没有找到这只股票的数据',

                    'data': ''
                }
            return Response(data)
        else:
            data = {
                'is_work_time': False,
                'info': '当前非工作时间',
                'today_data': GenericStockMarketDataSerializer(hgsmd, many=True).data,
                'data': ''
            }
            return Response(data)


class TenStockDataView(APIView):
    """
    
    """
    permission_classes = (AllowAny,)

    def get(self, request, date_flag):
        code_flag = request.GET.get('code_flag')
        if str(code_flag) not in ['0', '1', '2']:
            return Http404
        if date_flag not in ['minsec', 'day', 'week', 'month']:
            return Http404
        _data = {
            '0': {
                'info': '量霸价投，对标中证100',
                'stock_portfolio': {
                    '0603185': 0.1,
                    '0603260': 0.1,
                    '0600196': 0.1,
                    '0600958': 0.1,
                    '0601878': 0.1,
                    '0600598': 0.1,
                    '1002594': 0.1,
                    '0688981': 0.1,
                    '0688363': 0.1,
                    '0600438': 0.1
                },
                'blast_stock_code': '0000903'
            },
            '1': {
                'info': '量霸超额，对标中证500',
                'stock_portfolio': {
                    '1300869': 0.1,
                    '0600298': 0.1,
                    '0600597': 0.1,
                    '1002511': 0.1,
                    '1300724': 0.1,
                    '1300024': 0.1,
                    '0601555': 0.1,
                    '1300474': 0.1,
                    '0688521': 0.1,
                    '1002156': 0.1
                },
                'blast_stock_code': '0000905'
            },
            '2': {
                'info': '量霸超额，对标中证500',
                'stock_portfolio': {
                    '0688396': 0.1,
                    '0601995': 0.1,
                    '0601012': 0.1,
                    '1002202': 0.1,
                    '0600893': 0.1,
                    '1300623': 0.1,
                    '1300613': 0.1,
                    '0688298': 0.1,
                    '0603529': 0.1,
                    '1300075': 0.1
                },
                'blast_stock_code': '0000300'
            }
        }
        data = {
            'is_work_time': True,
            'info': 'ok'
        }
        now = datetime.now()   
        
        if date_flag == 'minsec':
            _stock_dict = {}
            stock_datas = _data[code_flag]['stock_portfolio']
            blast_stock_code = _data[code_flag]['blast_stock_code']
            data['stock_codes']: list(stock_datas.keys())
            for stock_code, weight in stock_datas.items():
                url = f"https://img1.money.126.net/data/hs/time/today/{stock_code}.json"
                try:
                    r = rq.get(url, timeout=300, verify=False)
                    resp_data = r.json()
                except Exception as e:
                    resp_data = {}
                
                if resp_data:
                    _datas = resp_data.get('data')
                    for time_str, _price, avg_price, _ in _datas:
                        if time_str in _stock_dict:
                            _stock_dict[time_str]['price'] += Decimal(get_two_float(Decimal(_price) * Decimal(weight), 2))
                            _stock_dict[time_str]['count'] += 1
                        else:
                            _stock_dict[time_str] = {
                                'price': Decimal(get_two_float(Decimal(_price) * Decimal(weight), 2)),
                                'count': 1
                            }

            data['last_work_data'] = []
            for key, value in _stock_dict.items():
                if value.get('count') != len(stock_datas.keys()):
                    continue
                data['last_work_data'].append([key, float(value.get('price'))])
            url = f"https://img1.money.126.net/data/hs/time/today/{blast_stock_code}.json"
            try:
                r = rq.get(url, timeout=300, verify=False)
                data['control_data'] = r.json()
            except Exception as e:
                data['control_data'] = []
            
            data['flag_info'] = _data[code_flag]['info']
            if not (chinese_calendar.is_workday(now) and get_on_work_time(now)):
                data['is_work_time'] = False
                data['info'] = '当前非工作时间'

        else:
            _stock_dict = {}
            blast_stock_code = _data[code_flag]['blast_stock_code']
            stock_datas = _data[code_flag]['stock_portfolio']
            data['stock_codes']: list(stock_datas.keys())
            for stock_code, weight in stock_datas.items():
                url = f'https://img1.money.126.net/data/hs/kline/{date_flag}/history/2022/{stock_code}.json'
                try:
                    r = rq.get(url, timeout=300, verify=False)
                    resp_data = r.json()
                except Exception as e:
                    resp_data = {}  
                if resp_data:
                    _datas = resp_data.get('data')
                    if len(_datas) > 12:
                        _datas = _datas[-13:]
                    else:
                        url = f'https://img1.money.126.net/data/hs/kline/{date_flag}/history/2021/{stock_code}.json'
                        try:
                            r = rq.get(url, timeout=300, verify=False)
                            _resp_data = r.json()
                        except Exception as e:
                            _resp_data = {}
                        if _resp_data:
                            other_datas = _resp_data.get('data')
                            _datas = other_datas[12-len(_datas):] + _datas
                    
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

            data[f'{date_flag}k_data'] = []
            for key, value in _stock_dict.items():
                if value.get('count') != len(stock_datas.keys()):
                    continue
                data[f'{date_flag}k_data'].append([key, float(value.get('open')), float(value.get('close')), float(value.get('high')), float(value.get('low'))])
            
            url = f'https://img1.money.126.net/data/hs/kline/{date_flag}/history/2022/{blast_stock_code}.json'
            try:
                r = rq.get(url, timeout=300, verify=False)
                control_data = r.json()
                
            except Exception as e:
                control_data = {}
            
            if control_data:
                if len(control_data['data']) < 12:
                    url = f'https://img1.money.126.net/data/hs/kline/{date_flag}/history/2021/{blast_stock_code}.json'
                    try:
                        r = rq.get(url, timeout=300, verify=False)
                        _resp_data = r.json()
                    except Exception as e:
                        _resp_data = {}
                    if _resp_data:
                        other_datas = _resp_data.get('data')
                        control_data['data'] = other_datas[12-len(control_data['data']):] + control_data['data']
                
                data['control_data'] = control_data

            if not (chinese_calendar.is_workday(now) and get_on_work_time(now)):
                data['is_work_time'] = False
                data['info'] = '当前非工作时间'
            
            data['flag_info'] = _data[code_flag]['info']
        
        return Response(data)
        


