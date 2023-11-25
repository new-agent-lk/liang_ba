import json
import os
import subprocess
import sys
import django
import datetime
import chinese_calendar as cal
from django.template.loader import render_to_string

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# 将项目路径加入到系统path中，这样在导入模型等模块时就不会报模块找不到了
sys.path.append(base_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'local_settings'  # 注意：base_django_api 是我的模块名，你在使用时需要跟换为你的模块
django.setup()

from django.conf import settings
from wagtail_apps.stock import Stock

stock = Stock()


def get_previous_workday(date):
    while True:
        date -= datetime.timedelta(days=1)
        if cal.is_workday(date):
            return date


_now = datetime.datetime.now()
_now_date = _now.date()
_one_day_pre = get_previous_workday(_now_date)
_one_day_pre_str = _one_day_pre.strftime("%Y%m%d")


def create_pie_nest(**kwargs):
    sh_deal_flow, sh_deal_sell = stock.get_sh_deal()
    sz_deal_flow, sz_deal_sell = stock.get_sz_deal()
    inner_data = json.dumps([
        {
            'value': stock.get_sh_deal_total(_one_day_pre_str),
            'name': '沪市',
        },
        {
            'value': stock.get_sz_deal_total(_one_day_pre_str),
            'name': '深市',
        }
    ])
    outer_data = json.dumps([
        {
            'value': sh_deal_sell,
            'name': '沪股通卖出',
        },
        {
            'value': sz_deal_sell,
            'name': '深股通卖出',
        },
        {
            'value': sh_deal_flow,
            'name': '沪股通买入',
        },
        {
            'value': sz_deal_flow,
            'name': '深股通买入',
        },
    ])
    return render_to_string('charts/pie-nest.html', locals())


def create_pie_nest_img():
    img_dir_path = os.path.join(settings.TMP_DIR, 'img')
    html_dir_path = os.path.join(settings.TMP_DIR, 'html')
    if not os.path.exists(img_dir_path): os.mkdir(img_dir_path)
    if not os.path.exists(html_dir_path): os.mkdir(html_dir_path)

    html_path = os.path.join(html_dir_path, f'{_now.strftime("%Y%m%d")}.html')
    img_path = os.path.join(img_dir_path, f'{_now.strftime("%Y%m%d")}.png')
    if not os.path.exists(html_path):
        with open(html_path, 'w') as f:
            f.write(create_pie_nest())
    else:
        print(html_path, ' @@exists.')

    if not os.path.exists(img_path):
        cmd_str = f'node web_screenshot.js {html_path} {img_path}'

        result = subprocess.run(cmd_str, shell=True, cwd=settings.SCREENSHOT_WORK_PATH,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if result.returncode == 0:
            print("命令执行成功:")
            print(result.stdout)
        else:
            print("命令执行失败:")
            print(result.stderr)
    else:
        print(img_path, ' @@exists.')


if __name__ == '__main__':
    print(create_pie_nest())

