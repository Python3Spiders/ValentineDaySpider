# -*- coding: utf-8 -*-
# author:           inspurer(月小水长)
# pc_type           lenovo
# create_time:      2019/8/3 15:40
# file_name:        data_scrapy.py
# github            https://github.com/inspurer
# qq邮箱            2391527690@qq.com
# 微信公众号         月小水长(ID: inspurer)

import requests

import re

from concurrent.futures import ThreadPoolExecutor,as_completed

headers = {
    'cookies': '''tgw_l7_route=73af20938a97f63d9b695ad561c4c10c; tst=; q_c1=2b96259977c74f3dabdb6c16fa585511|1564642693|1564642693; z_c0="2|1:0|10:1564642691|4:z_c0|92:Mi4xdFljQ0JBQUFBQUFBZ0tKMzBSSFREeVlBQUFCZ0FsVk5nOXN2WGdDZURJS0tOSi00bExkX05wOUZMcFlDNUh5NEd3|db8688dbdb903f9c01f92774275a654f18c7a97cae01683bf89aacdc789384c3"; capsion_ticket="2|1:0|10:1564642680|14:capsion_ticket|44:ODAzNWZkMGUwY2YyNDA2MjgwZmQxMjYwODU2NmFhMDE=|5471a1791e8130b82a2c5e57ab9ef6afd664e7771e3973c8b5057181a9e8628c"; d_c0="AICid9ER0w-PTp04VPewZBygtjG41AGcydw=|1564642679"; _xsrf=z1JSAVX9lV2PSGlgAFZ43o6Odd9KxfGL; _zap=4363ac70-ae8e-455c-bc64-0e4d61f6e5af; tst=r''',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
}

url = 'https://www.zhihu.com/api/v4/questions/285989317/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset={}&limit=5&sort_by=default&platform=desktop'

def worker(pageNum):
    try:
        res = requests.get(url=url.format(pageNum),headers=headers)
        data = res.json()['data']
        for item in data:
            author = item['author']['name']
            # 一条答案包括 content 和 excerpt 两部分
            content = item['content']
            excerpt = item['excerpt']
            answer = content + excerpt
            # 去掉富文本标签
            answer = re.sub("<.*?>","",answer)
            return [author,answer]

    except Exception as e:
        print(e)

executor = ThreadPoolExecutor(max_workers=4)
# 只获取质量高的前 100 个回答
all_tasks = [executor.submit(worker, (i)) for i in range(100)]

# as_completed()方法是一个生成器，在没有任务完成的时候，会阻塞，
# 在有某个任务完成的时候，会yield这个任务，就能执行for循环下面的语句，然后继续阻塞住，循环到所有的任务结束。
# 从结果也可以看出，先完成的任务会先通知主线程

import pandas as pd

answers = []
for future in as_completed(all_tasks):
    data = future.result()
    print(data)
    answers.append(data)

col = ['author','answer']
df = pd.DataFrame(data=answers,columns=col)

df.to_csv("answers.csv",encoding="utf-8")


