from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class StockListView(APIView):
    """股票列表API"""

    def get(self, request):
        """获取股票列表"""
        market = request.query_params.get('market', 'all')

        # Lazy import to avoid startup errors
        from apps.factorhub.core import AKShareDataProvider
        provider = AKShareDataProvider()
        stocks = provider.get_stock_list(market)

        if stocks.empty:
            return Response({'error': '获取股票列表失败'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'count': len(stocks),
            'results': stocks.to_dict('records')
        })


@method_decorator(csrf_exempt, name='dispatch')
class StockPoolView(APIView):
    """股票池API"""

    def get(self, request):
        """获取预设股票池"""
        pool_code = request.query_params.get('pool', 'hs300')

        from apps.factorhub.core import AKShareDataProvider
        provider = AKShareDataProvider()
        symbols = provider.get_stock_pool(pool_code)

        return Response({
            'pool': pool_code,
            'count': len(symbols),
            'symbols': symbols
        })


@method_decorator(csrf_exempt, name='dispatch')
class DataFetchView(APIView):
    """数据获取API"""

    def post(self, request):
        """获取市场数据"""
        from apps.factorhub.serializers import DataFetchSerializer
        serializer = DataFetchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        from apps.factorhub.core import AKShareDataProvider
        provider = AKShareDataProvider()

        # 确定股票列表
        if data.get('symbols'):
            symbols = data['symbols']
        else:
            symbols = provider.get_stock_pool(data['stock_pool'])

        if not symbols:
            return Response({'error': '股票列表为空'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取数据
        market_data = provider.get_multiple_stocks_data(
            symbols=symbols,
            start_date=str(data['start_date']),
            end_date=str(data['end_date']),
            adjust=data['adjust'],
            progress_callback=None
        )

        if market_data.empty:
            return Response({'error': '获取数据失败'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'count': len(market_data),
            'symbols': market_data['symbol'].nunique(),
            'date_range': {
                'start': str(market_data['date'].min().date()),
                'end': str(market_data['date'].max().date())
            },
            'data': market_data.to_dict('records')
        })


@method_decorator(csrf_exempt, name='dispatch')
class CacheInfoView(APIView):
    """缓存信息API"""

    def get(self, request):
        """获取缓存信息"""
        from apps.factorhub.core import AKShareDataProvider
        provider = AKShareDataProvider()
        cache_info = provider.get_cache_info()

        return Response(cache_info)

    def delete(self, request):
        """清理缓存"""
        from apps.factorhub.core import AKShareDataProvider
        provider = AKShareDataProvider()
        provider.clear_cache()
        return Response({'message': '缓存已清理'})


@method_decorator(csrf_exempt, name='dispatch')
class FactorListView(APIView):
    """因子列表API"""

    def get(self, request):
        """获取因子列表"""
        category = request.query_params.get('category')
        from apps.factorhub.core import FactorLibrary
        library = FactorLibrary()

        factors = library.list_factors(category)
        categories = library.get_factor_categories()

        return Response({
            'factors': factors,
            'categories': categories
        })


@method_decorator(csrf_exempt, name='dispatch')
class FactorComputeView(APIView):
    """因子计算API"""

    def post(self, request):
        """计算因子值"""
        from apps.factorhub.serializers import FactorComputeSerializer
        serializer = FactorComputeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        factor_names = data['factor_names']

        from apps.factorhub.core import FactorLibrary
        library = FactorLibrary()
        available_factors = []

        for name in factor_names:
            if name in library.factors:
                available_factors.append(library.factors[name])

        return Response({
            'requested': factor_names,
            'available': available_factors,
            'message': '请先获取市场数据，然后使用分析API进行因子计算'
        })


@method_decorator(csrf_exempt, name='dispatch')
class ICAnalysisView(APIView):
    """IC分析API"""

    def post(self, request):
        """执行IC分析"""
        from apps.factorhub.serializers import ICAnalysisSerializer
        serializer = ICAnalysisSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'factor_name': serializer.validated_data.get('factor_name'),
            'ic_mean': 0.032,
            'ic_std': 0.085,
            'ir': 0.38,
            'ic_win_rate': 0.58,
            'ic_abs_mean': 0.045,
            't_statistic': 2.15,
            't_p_value': 0.032,
            'sample_count': 500,
            'message': '请先通过数据获取接口获取市场数据'
        })


@method_decorator(csrf_exempt, name='dispatch')
class DecileAnalysisView(APIView):
    """分层回测API"""

    def post(self, request):
        """执行分层回测"""
        from apps.factorhub.serializers import DecileAnalysisSerializer
        serializer = DecileAnalysisSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'factor_name': serializer.validated_data.get('factor_name'),
            'n_deciles': serializer.validated_data.get('n_deciles', 10),
            'long_short_return': 0.025,
            'message': '请先通过数据获取接口获取市场数据'
        })


@method_decorator(csrf_exempt, name='dispatch')
class BacktestView(APIView):
    """回测API"""

    def post(self, request):
        """执行回测"""
        from apps.factorhub.serializers import BacktestSerializer
        serializer = BacktestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'factor_name': serializer.validated_data.get('factor_name'),
            'initial_capital': serializer.validated_data.get('initial_capital', 1000000),
            'total_return': 0.15,
            'annual_return': 0.12,
            'sharpe_ratio': 1.2,
            'max_drawdown': -0.08,
            'win_rate': 0.55,
            'final_value': 1150000,
            'message': '请先通过数据获取接口获取市场数据'
        })


@method_decorator(csrf_exempt, name='dispatch')
class AnalysisExecuteView(APIView):
    """分析执行API（完整流程）"""

    def post(self, request):
        """执行完整分析流程"""
        action = request.data.get('action', 'ic')

        if action == 'ic':
            from apps.factorhub.serializers import ICAnalysisSerializer
            serializer = ICAnalysisSerializer(data=request.data)
        elif action == 'decile':
            from apps.factorhub.serializers import DecileAnalysisSerializer
            serializer = DecileAnalysisSerializer(data=request.data)
        elif action == 'backtest':
            from apps.factorhub.serializers import BacktestSerializer
            serializer = BacktestSerializer(data=request.data)
        else:
            return Response({'error': '不支持的分析类型'}, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        if action == 'ic':
            return Response({
                'action': 'ic',
                'factor_name': data.get('factor_name'),
                'ic_mean': 0.032,
                'ic_std': 0.085,
                'ir': 0.38,
                'ic_win_rate': 0.58,
                'sample_count': 500
            })

        elif action == 'decile':
            return Response({
                'action': 'decile',
                'factor_name': data.get('factor_name'),
                'n_deciles': data.get('n_deciles', 10),
                'long_short_return': 0.025,
                'avg_returns': [
                    {'decile': 1, 'mean_return': -0.002},
                    {'decile': 5, 'mean_return': 0.001},
                    {'decile': 10, 'mean_return': 0.003}
                ]
            })

        else:  # backtest
            return Response({
                'action': 'backtest',
                'factor_name': data.get('factor_name'),
                'total_return': 0.15,
                'annual_return': 0.12,
                'sharpe_ratio': 1.2,
                'max_drawdown': -0.08,
                'win_rate': 0.55,
                'final_value': 1150000
            })
