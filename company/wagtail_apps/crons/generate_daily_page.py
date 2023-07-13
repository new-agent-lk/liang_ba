import json
import os
import sys
import django
import akshare as ak
import chinese_calendar
import datetime

from django.template.loader import render_to_string
from wagtail.rich_text import RichText

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 将项目路径加入到系统path中，这样在导入模型等模块时就不会报模块找不到了
sys.path.append(base_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'company.local_settings'  # 注意：base_django_api 是我的模块名，你在使用时需要跟换为你的模块
django.setup()

from wagtail_apps.models import CompanyDailyPage, CompanyDailyContentPage

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
    return str_nfi, str_hfi, str_sfi, hgt_flow_in, sgt_flow_in


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
    return str_nfi_s, str_hfi_s, str_sfi_s, hgt_south_flow_in, sgt_south_flow_in


def get_hsgt_total():
    """
    总持股市值
    """
    stock_hsgt_institution_statistics_em_df = (
        ak.stock_hsgt_institution_statistics_em(
            market="北向持股", start_date=_one_day_pre.strftime('%Y%m%d'), end_date=_now_date.strftime('%Y%m%d')
        )
    )
    _total = 0.0
    for i in stock_hsgt_institution_statistics_em_df['持股市值']:
        _total += i
    _total /= 10000000
    return f'{_total:.2f}'


def get_sh_deal_total():
    stock_sse_deal_daily_df = ak.stock_sse_deal_daily(_one_day_pre_str)
    return stock_sse_deal_daily_df.values[3][1]


def get_sz_deal_total():
    stock_szse_summary_df = ak.stock_szse_summary(_one_day_pre_str)
    return round(stock_szse_summary_df.values[0][2] / 100000000, 2)


def get_template():
    str_nfi_north, str_hfi_north, str_sfi_north, hgt_flow_in, sgt_flow_in = get_hsgt_north()
    str_nfi_south, str_hfi_south, str_sfi_south, hgt_south_flow_in, sgt_south_flow_in = get_hsgt_south()
    total = get_hsgt_total()
    inner_data = json.dumps([
        {
            'value': get_sh_deal_total(),
            'name': '沪市',
        },
        {
            'value': get_sz_deal_total(),
            'name': '深市',
        }
    ])
    outer_data = json.dumps([
        {
            'value': hgt_flow_in,
            'name': '沪股通买入',
        },
        {
            'value': sgt_flow_in,
            'name': '深股通买入',
        },
        {
            'value': hgt_south_flow_in,
            'name': '沪股通买入',
        },
        {
            'value': sgt_south_flow_in,
            'name': '',
        },
    ])
    return render_to_string('charts/daily.html', locals())


def get_stream_field():
    return [("source_code", RichText(get_template()))]


def make_title(_date):
    return f'{_date.strftime("%Y.%m.%d")}北上资金前日总结'


def make_slug(_date):
    return f'daily_{_date.strftime("%Y%m%d")}'


def create_page():
    print('%s: generate daily page' % _one_day_pre)
    daily_index = CompanyDailyPage.objects.live().first()
    daily_index.add_child(
        instance=CompanyDailyContentPage(
            title=make_title(_one_day_pre),
            slug=make_slug(_one_day_pre),
            body=get_stream_field()
        )
    )


if __name__ == '__main__':
    # print(get_template())

    create_page()
