import requests
import ast

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# Create your views here.

rq = requests.session()


class GenericStockMarketView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        stock_code_list = request.query_params.get("stock_code", "['sz399001']")
        code_iter_list = ast.literal_eval(stock_code_list)
        result = {}
        for code in code_iter_list:
            url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={}&scale=60&ma=5&datalen=1023'.format(code)
            try:
                r = rq.get(url, timeout=300, verify=False)
                result[code] = r.json()
            except Exception as e:
                result[code] = ""
        return Response(result)


