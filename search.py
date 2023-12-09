import os
import json

from fuzzywuzzy import process
from fuzzywuzzy import fuzz

TAG_TYPE = {1: '地区', 2: '算法', 3: '来源', 4: '时间', 5: '特殊', 6: '其它'}


def search():
    with open('lgct/data/tags.json', 'r', encoding='utf-8') as f:
        tags = json.load(f)
    while True:
        os.system('cls')
        print('输入 -quit 或 -q 以退出!\n')
        name = input('请输入要查询的标签名: ')
        if name in ['-quit', '-q']:
            break
        if name in tags['id'].keys():
            print(f'{name}\t|{TAG_TYPE[tags["id"][name]["type"]]}\t|{tags["id"][name]["name"]}')
            input('\n按 Enter 键继续...')
            continue
        res = process.extract(name, tags['name'].keys(), limit=10, scorer=fuzz.QRatio)
        if res[0][1] == 0:
            print('没有找到对应的标签!')
        else:
            print('标签 ID\t|类型\t|标签名称\n')
            for tag in res:
                if tag[1] > 0:
                    print(f'{tags["name"][tag[0]]}\t|{TAG_TYPE[tags["id"][tags["name"][tag[0]]]["type"]]}\t|{tag[0]}')
        input('\n按 Enter 键继续...')
