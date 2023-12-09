import os
import json
import datetime

from urllib.request import urlopen
from urllib.parse import unquote

from parse import parse

TYPE_NAMES = ['P', 'B', 'CF', 'SP', 'AT', 'UVA']


def update_type(type_name: str):
    base = f'https://www.luogu.com.cn/problem/list?type={type_name}&page='
    page = 1
    result = []
    while True:
        url = base + str(page)
        os.system('cls')
        print(f'正在获取 {url} 的数据...')
        html = bytes.decode(urlopen(url).read())
        res = parse('{before}JSON.parse(decodeURIComponent("{text}"));{after}', html)
        text = unquote(res['text'])
        problems = json.loads(text)['currentData']['problems']['result']
        if not problems:
            break
        for problem in problems:
            result.append(problem)
        page += 1
    with open(f'lgct/data/{type_name}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f)


def update_tags():
    tags = json.loads(bytes.decode(urlopen('https://www.luogu.com.cn/_lfe/tags').read()))
    _id = {}
    name = {}
    for tag in tags['tags']:
        name[tag['name']] = str(tag['id'])
        _id[str(tag['id'])] = {"name": tag['name'], "type": tag["type"]}
    with open('lgct/data/tags.json', 'w', encoding='utf-8') as f:
        json.dump({"name": name, "id": _id}, f)


def update():
    for type_name in TYPE_NAMES:
        update_type(type_name)
    update_tags()
    with open('lgct/settings.json', 'r', encoding='utf-8') as f:
        tmp = json.load(f)
    with open('lgct/settings.json', 'w', encoding='utf-8') as f:
        tmp['last_update'] = f'{datetime.datetime.today().year}-{datetime.datetime.today().month}-{datetime.datetime.today().day}'
        json.dump(tmp, f)
    print('完成!')
