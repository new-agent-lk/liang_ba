import akshare as ak


def get_sh_deal_total(_one_day_pre_str):
    stock_sse_deal_daily_df = ak.stock_sse_deal_daily(_one_day_pre_str)
    return stock_sse_deal_daily_df.values[3][1]


def get_sz_deal_total(_one_day_pre_str):
    stock_szse_summary_df = ak.stock_szse_summary(_one_day_pre_str)
    return round(stock_szse_summary_df.values[0][2] / 100000000, 2)


def get_sh_deal():
    stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="沪股通")
    return round(stock_hsgt_hist_em_df.values[0][2], 2), round(stock_hsgt_hist_em_df.values[0][3], 2)


def get_sz_deal():
    stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="深股通")
    return round(stock_hsgt_hist_em_df.values[0][2], 2), round(stock_hsgt_hist_em_df.values[0][3], 2)
