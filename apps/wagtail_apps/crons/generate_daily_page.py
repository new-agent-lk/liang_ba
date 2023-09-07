import json
import os
import sys
import django
import akshare as ak
import chinese_calendar
import datetime

from django.template.loader import render_to_string
from wagtail.rich_text import RichText

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# 将项目路径加入到系统path中，这样在导入模型等模块时就不会报模块找不到了
sys.path.append(base_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'local_settings'  # 注意：base_django_api 是我的模块名，你在使用时需要跟换为你的模块
django.setup()

from wagtail_apps.models import CompanyDailyPage, CompanyDailyContentPage
from wagtail_apps.charts.pie_nest import create_pie_nest
from wagtail_apps.stock import get_hsgt_north, get_hsgt_south, get_hsgt_total, get_summary_deal
from django.conf import settings

_now = datetime.datetime.now()
_now_date = _now.date()
_one_day_pre = _now_date - datetime.timedelta(days=1)
_one_day_pre_str = _one_day_pre.strftime("%Y%m%d")


def get_template():
    str_nfi_north, str_hfi_north, str_sfi_north = get_hsgt_north()
    str_nfi_south, str_hfi_south, str_sfi_south = get_hsgt_south()
    total = get_hsgt_total()
    sh_deal_flow, sh_deal_sell, sz_deal_flow, sz_deal_sell, summary_deal = get_summary_deal()

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
    print(get_template())

    # create_page()
