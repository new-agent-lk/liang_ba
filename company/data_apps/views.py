import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# Create your views here.

rq = requests.session()


class GenericStockMarketView(APIView):
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
    permission_classes = (AllowAny, )

    def get(self, request):
        stock_codes = request.query_params.get("stock_codes", "sz399001")
        stock_codes_list = stock_codes.split(',')
        result = {}
        for code in stock_codes_list:
            url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={}&scale=60&ma=5&datalen=100'.format(code)
            try:
                r = rq.get(url, timeout=300, verify=False)
                result[code] = r.json()
            except Exception as e:
                result[code] = ""
        return Response(result)


