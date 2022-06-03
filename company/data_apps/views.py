import chinese_calendar
import requests
from datetime import datetime
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# Create your views here.

from data_apps.models import GenericStockMarketData
from data_apps.crons import get_on_work_time
from data_apps.serializers.generic_stock_market_data import GenericStockMarketDataSerializer

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
        codes = ['sh603185', 'sh603260', 'sh600196', 'sh600958', 'sh601878', 'sh600598', 'sz002594', 'sh688981', 'sh688363', 'sh600438']
        weight = ['sh603185', 'sh603260', 'sh600196', 'sh600958', 'sh601878', 'sh600598', 'sz002594', 'sh688981', 'sh688363', 'sh600438'],
        
        now = datetime.now()
        offset = timedelta(minutes=2)
        data = {
            'is_work_time': True,
            'avg_price': 0.0,
            'avg_weight_price': 0.0,
            'info': 'ok',
            'stock_codes': codes,
        }
        if chinese_calendar.is_workday(now) and get_on_work_time(now):
            sc_list = []
            _avg_price = 0.0
            _avg_w_price = 0.0
            for stock_code in codes:
                gsmd = GenericStockMarketData.objects.filter(stock_code=stock_code, current_time__range=(now-offset, now)).order_by('-id').first()
                sc_list.append(gsmd)
            
            if sc_list:
                for sc_obj in sc_list:
                    _avg_w_price += float(sc_obj.now_price) * 0.1
                    _avg_price += float(sc_obj.now_price)
                    
                data['avg_price'] = _avg_price / len(sc_list)
                data['avg_weight_price'] = _avg_w_price / _avg_price
                data['total_price'] = _avg_price
        else:
            data['is_work_time'] = False
            data['info'] = '当前非工作时间'
        
        return Response(data)


