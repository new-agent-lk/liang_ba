import datetime
import akshare as ak
import chinese_calendar as cal
from .utils import retry

from wagtail_apps.utils import get_time_str


class Stock:

    def __init__(self):
        self._now = datetime.datetime.now()
        self.previous_workday = None
        self.get_previous_workday()
        self.previous_workday_str = ''

    def get_previous_workday(self):
        self.previous_workday = self._now.date()
        while True:
            self.previous_workday -= datetime.timedelta(days=1)
            if cal.is_workday(self.previous_workday):
                self.previous_workday_str = self.previous_workday.strftime("%Y%m%d")
                break

    def get_pre_workday_index(self, data_frame, reverse=False):
        _index = -1 if reverse else 0
        while True:
            _time = data_frame.values[_index][0]
            time_str = get_time_str(_time)
            data = data_frame.values[_index][1]
            if not time_str:
                raise Exception('没找到合适的类型')

            if time_str != self.previous_workday_str:
                if reverse:
                    _index -= 1
                else:
                    _index += 1
                self.previous_workday_str = get_time_str(data_frame.values[_index][0])
            else:
                if abs(float(data)) > 0.0:
                    return _index
                else:
                    print(f'离最近的一个工作日没有数据，将发生改变 往{"上" if reverse else "下"}寻一天')
                    if reverse:
                        _index -= 1
                    else:
                        _index += 1
                    self.previous_workday_str = get_time_str(data_frame.values[_index][0])

    @retry(times=3, delay=10, timeout=60)
    def get_hsgt_north(self):
        """
        北上资金流入或流出市值
        """
        hgt_north_net_flow_in_em_df = ak.stock_hsgt_north_net_flow_in_em(symbol="沪股通")
        sgt_north_net_flow_in_em_df = ak.stock_hsgt_north_net_flow_in_em(symbol="深股通")
        north_net_flow_in_em_df = ak.stock_hsgt_north_net_flow_in_em(symbol="北上")

        index = self.get_pre_workday_index(north_net_flow_in_em_df, reverse=True)

        north_flow_in = float(north_net_flow_in_em_df.values[index][1]) / 10000
        hgt_flow_in = float(hgt_north_net_flow_in_em_df.values[index][1]) / 10000
        sgt_flow_in = float(sgt_north_net_flow_in_em_df.values[index][1]) / 10000
        str_nfi = f'净流入 {north_flow_in:.2f} 亿' if north_flow_in > 0 else f'净流出 {abs(north_flow_in):.2f} 亿'
        str_hfi = f'净流入 {hgt_flow_in:.2f} 亿' if hgt_flow_in > 0 else f'净流出 {abs(hgt_flow_in):.2f} 亿'
        str_sfi = f'净流入 {sgt_flow_in:.2f} 亿' if sgt_flow_in > 0 else f'净流出 {abs(sgt_flow_in):.2f} 亿'
        return str_nfi, str_hfi, str_sfi

    @retry(times=3, delay=10, timeout=60)
    def get_hsgt_south(self):
        """
        南下资金流入或流出市值
        """
        hgt_south_net_flow_in_em_df = ak.stock_hsgt_south_net_flow_in_em(symbol="沪股通")
        sgt_south_net_flow_in_em_df = ak.stock_hsgt_south_net_flow_in_em(symbol="深股通")
        south_net_flow_in_em_df = ak.stock_hsgt_south_net_flow_in_em(symbol="南下")

        index = self.get_pre_workday_index(south_net_flow_in_em_df, reverse=True)

        south_flow_in = float(south_net_flow_in_em_df.values[index][1]) / 10000
        hgt_south_flow_in = float(hgt_south_net_flow_in_em_df.values[index][1]) / 10000
        sgt_south_flow_in = float(sgt_south_net_flow_in_em_df.values[index][1]) / 10000
        str_nfi_s = f'净流入 {south_flow_in:.2f} 亿' if south_flow_in > 0 else f'净流出 {abs(south_flow_in):.2f} 亿'
        str_hfi_s = f'净流入 {hgt_south_flow_in:.2f} 亿' if hgt_south_flow_in > 0 else f'净流出 {abs(hgt_south_flow_in):.2f} 亿'
        str_sfi_s = f'净流入 {sgt_south_flow_in:.2f} 亿' if sgt_south_flow_in > 0 else f'净流出 {abs(sgt_south_flow_in):.2f} 亿'
        return str_nfi_s, str_hfi_s, str_sfi_s

    @retry(times=3, delay=10, timeout=60)
    def get_hsgt_total(self, start_date: str = '', end_date: str = ''):
        """
        北向持股  总持股市值
        """
        if not start_date: start_date = self.previous_workday_str
        if not end_date: end_date = self.previous_workday_str

        stock_hsgt_institution_statistics_em_df = (
            ak.stock_hsgt_institution_statistics_em(
                market="北向持股", start_date=start_date, end_date=end_date
            )
        )
        _total = 0.0
        for i in stock_hsgt_institution_statistics_em_df['持股市值']:
            _total += i
        _total /= 10000000
        return f'{_total:.2f}'

    @retry(times=3, delay=10, timeout=60)
    def get_sh_deal_total(self, _day_str=''):
        """
            获取沪市交易总额
        """
        if not _day_str: _day_str = self.previous_workday_str
        stock_sse_deal_daily_df = ak.stock_sse_deal_daily(_day_str)
        return stock_sse_deal_daily_df.values[3][1]

    @retry(times=3, delay=10, timeout=60)
    def get_sz_deal_total(self, _day_str):
        """
            获取深市交易总额
        """
        if not _day_str: _day_str = self.previous_workday_str
        stock_szse_summary_df = ak.stock_szse_summary(_day_str)
        return round(stock_szse_summary_df.values[0][2] / 100000000, 2)

    @retry(times=3, delay=10, timeout=60)
    def get_sh_deal(self):
        """
            获取沪港通买入 卖出总额
        """
        stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="沪股通")
        index = self.get_pre_workday_index(stock_hsgt_hist_em_df)
        return round(stock_hsgt_hist_em_df.values[index][2], 2), round(stock_hsgt_hist_em_df.values[index][3], 2)

    @retry(times=3, delay=10, timeout=60)
    def get_sz_deal(self):
        """
            获取深港通买入 卖出总额
        """
        stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="深股通")
        index = self.get_pre_workday_index(stock_hsgt_hist_em_df)
        return round(stock_hsgt_hist_em_df.values[index][2], 2), round(stock_hsgt_hist_em_df.values[index][3], 2)

    @retry(times=3, delay=10, timeout=60)
    def get_summary_deal(self):
        """
            获取北向资金 总成交额
        """
        sh_deal_flow, sh_deal_sell = self.get_sh_deal()
        sz_deal_flow, sz_deal_sell = self.get_sz_deal()
        _total = sh_deal_flow + sh_deal_sell + sz_deal_flow + sz_deal_sell
        return sh_deal_flow, sh_deal_sell, sz_deal_flow, sz_deal_sell, _total


def get_template_data():
    stock = Stock()
    str_nfi_north, str_hfi_north, str_sfi_north = stock.get_hsgt_north()
    str_nfi_south, str_hfi_south, str_sfi_south = stock.get_hsgt_south()
    total = stock.get_hsgt_total()
    sh_deal_flow, sh_deal_sell, sz_deal_flow, sz_deal_sell, summary_deal = stock.get_summary_deal()
    return locals()


if __name__ == '__main__':
    print(get_template_data())
