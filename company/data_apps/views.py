import chinese_calendar
import requests
from decimal import Decimal
from datetime import datetime
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
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
    返回当前十只股票历史数据
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        _codes = {
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
        }
        
        now = datetime.now()
        offset = timedelta(minutes=2)
        data = {
            'is_work_time': True,
            'avg_price': 0.0,
            'avg_weight_price': 0.0,
            'info': 'ok',
            'stock_codes': list(_codes.keys()),
        }
       

        _stock_dict = {}
        for stock_code, weight in _codes.items():
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
            if value.get('count') != len(_codes.keys()):
                continue
            data['last_work_data'].append([key, float(value.get('price'))])
            #     gsmd = GenericStockMarketData.objects.filter(stock_code=stock_code, current_time__range=(now-offset, now)).order_by('-id').first()
            #     sc_list.append(gsmd)
            
            # if sc_list:
            #     for sc_obj in sc_list:
            #         _avg_w_price += float(sc_obj.now_price) * 0.1
            #         _avg_price += float(sc_obj.now_price)
                    
            #     data['avg_price'] = _avg_price / len(sc_list)
            #     data['avg_weight_price'] = _avg_w_price / _avg_price
            #     data['total_price'] = _avg_price
        if not (chinese_calendar.is_workday(now) and get_on_work_time(now)):
            data['is_work_time'] = False
            data['info'] = '当前非工作时间'

        return Response(data)


