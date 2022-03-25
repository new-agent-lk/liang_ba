import requests
from datetime import datetime

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
        if get_on_work_time(now):
            gsmd = GenericStockMarketData.objects.filter(stock_code=stock_code,).first()
            if gsmd:
                data = {
                    'is_work_time': True,
                    'data': GenericStockMarketDataSerializer(gsmd).data,
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
                'data': ''
            }
            return Response(data)



