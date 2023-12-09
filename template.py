import os
import json

STANDARD = {
    "type": [],
    "difficulty": [],
    "translated": "all",
    "have": [],
    "no": [],
    "in": [],
    "ignore": 2
}
WEIGHTED = {
    "type": [],
    "difficulty": [],
    "translated": "all",
    "have": [],
    "no": [],
    "in": [],
    "ignore": 2,
    "weight": 1
}
WEIGHTED_SPECIAL = {
    "text": "",
    "weight": 1
}


def template(file_name, t, count):
    if os.path.exists(f'lgct/rule/{file_name}'):
        tmp = input(f'文件 lgct/rule/{file_name} 已经存在! 是否要替换? (y/n) ')
        if tmp in ['n', 'no', 'N', 'No', 'NO']:
            return
    with open(f'lgct/rule/{file_name}', 'w', encoding='utf-8') as f:
        res = []
        if t in ['standard', 'std', 's']:
            for i in range(count):
                res.append(STANDARD)
        elif t in ['weighted', 'w']:
            for i in range(count):
                res.append(WEIGHTED)
        elif t in ['special', 'sp']:
            for i in range(count):
                res.append('')
        elif t in ['weighted_special', 'ws']:
            for i in range(count):
                res.append(WEIGHTED_SPECIAL)
        json.dump(res, f, indent=4)
    print('完成! ')
