import datetime

import akshare as ak

_now = datetime.datetime.now()
_now_date = _now.date()
_one_day_pre = _now_date - datetime.timedelta(days=1)
_one_day_pre_str = _one_day_pre.strftime("%Y%m%d")


def get_hsgt_north():
    """
    北上资金流入或流出市值
    """
    hgt_north_net_flow_in_em_df = ak.stock_hsgt_north_net_flow_in_em(symbol="沪股通")
    sgt_north_net_flow_in_em_df = ak.stock_hsgt_north_net_flow_in_em(symbol="深股通")
    north_net_flow_in_em_df = ak.stock_hsgt_north_net_flow_in_em(symbol="北上")
    north_flow_in = float(north_net_flow_in_em_df.values[-1][1]) / 10000
    hgt_flow_in = float(hgt_north_net_flow_in_em_df.values[-1][1]) / 10000
    sgt_flow_in = float(sgt_north_net_flow_in_em_df.values[-1][1]) / 10000
    str_nfi = f'净流入 {north_flow_in:.2f} 亿' if north_flow_in > 0 else f'净流出 {abs(north_flow_in):.2f} 亿'
    str_hfi = f'净流入 {hgt_flow_in:.2f} 亿' if hgt_flow_in > 0 else f'净流出 {abs(hgt_flow_in):.2f} 亿'
    str_sfi = f'净流入 {sgt_flow_in:.2f} 亿' if sgt_flow_in > 0 else f'净流出 {abs(sgt_flow_in):.2f} 亿'
    return str_nfi, str_hfi, str_sfi


def get_hsgt_south():
    """
    南下资金流入或流出市值
    """
    hgt_south_net_flow_in_em_df = ak.stock_hsgt_south_net_flow_in_em(symbol="沪股通")
    sgt_south_net_flow_in_em_df = ak.stock_hsgt_south_net_flow_in_em(symbol="深股通")
    south_net_flow_in_em_df = ak.stock_hsgt_south_net_flow_in_em(symbol="南下")
    south_flow_in = float(south_net_flow_in_em_df.values[-1][1]) / 10000
    hgt_south_flow_in = float(hgt_south_net_flow_in_em_df.values[-1][1]) / 10000
    sgt_south_flow_in = float(sgt_south_net_flow_in_em_df.values[-1][1]) / 10000
    str_nfi_s = f'净流入 {south_flow_in:.2f} 亿' if south_flow_in > 0 else f'净流出 {abs(south_flow_in):.2f} 亿'
    str_hfi_s = f'净流入 {hgt_south_flow_in:.2f} 亿' if hgt_south_flow_in > 0 else f'净流出 {abs(hgt_south_flow_in):.2f} 亿'
    str_sfi_s = f'净流入 {sgt_south_flow_in:.2f} 亿' if sgt_south_flow_in > 0 else f'净流出 {abs(sgt_south_flow_in):.2f} 亿'
    return str_nfi_s, str_hfi_s, str_sfi_s


def get_hsgt_total(start_date: str = _one_day_pre.strftime('%Y%m%d'),
                   end_date: str = _now_date.strftime('%Y%m%d')):
    """
    北向持股  总持股市值
    """
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


def get_sh_deal_total(_one_day_pre_str):
    """
        获取沪市交易总额
    """
    stock_sse_deal_daily_df = ak.stock_sse_deal_daily(_one_day_pre_str)
    return stock_sse_deal_daily_df.values[3][1]


def get_sz_deal_total(_one_day_pre_str):
    """
        获取深市交易总额
    """
    stock_szse_summary_df = ak.stock_szse_summary(_one_day_pre_str)
    return round(stock_szse_summary_df.values[0][2] / 100000000, 2)


def get_sh_deal():
    """
        获取沪港通买入 卖出总额
    """
    stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="沪股通")
    return round(stock_hsgt_hist_em_df.values[0][2], 2), round(stock_hsgt_hist_em_df.values[0][3], 2)


def get_sz_deal():
    """
        获取深港通买入 卖出总额
    """
    stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="深股通")
    return round(stock_hsgt_hist_em_df.values[0][2], 2), round(stock_hsgt_hist_em_df.values[0][3], 2)


def get_summary_deal():
    """
        获取北向资金 总成交额
    """
    sh_deal_flow, sh_deal_sell = get_sh_deal()
    sz_deal_flow, sz_deal_sell = get_sz_deal()
    _total = sh_deal_flow + sh_deal_sell + sz_deal_flow + sz_deal_sell
    return sh_deal_flow, sh_deal_sell, sz_deal_flow, sz_deal_sell, _total

