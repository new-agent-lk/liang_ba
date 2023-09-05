import json
import os
import subprocess
import sys
import django
import datetime
from django.template.loader import render_to_string
from wagtail_apps.stock import get_sh_deal, get_sz_deal, get_sh_deal_total, get_sz_deal_total

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# 将项目路径加入到系统path中，这样在导入模型等模块时就不会报模块找不到了
sys.path.append(base_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'local_settings'  # 注意：base_django_api 是我的模块名，你在使用时需要跟换为你的模块
django.setup()

from django.conf import settings

_now = datetime.datetime.now()
_now_date = _now.date()
_one_day_pre = _now_date - datetime.timedelta(days=1)
_one_day_pre_str = _one_day_pre.strftime("%Y%m%d")


def create_pie_nest():
    sh_deal_flow, sh_deal_sell = get_sh_deal()
    sz_deal_flow, sz_deal_sell = get_sz_deal()
    inner_data = json.dumps([
        {
            'value': get_sh_deal_total(_one_day_pre_str),
            'name': '沪市',
        },
        {
            'value': get_sz_deal_total(_one_day_pre_str),
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
    with open(html_path, 'w') as f:
        f.write(create_pie_nest())

    if os.path.exists(html_path):
        if not os.path.exists(img_path):
            cmd_str = f"{settings.WKHTMLTOIMAGE} {html_path} {img_path}"
            print(cmd_str)
            subprocess.run(cmd_str, shell=True)
        else:
            print(img_path, ' @@exists.')


if __name__ == '__main__':
    print(create_pie_nest_img())

