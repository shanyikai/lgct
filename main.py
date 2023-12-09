import os
import json
import webbrowser

from template import template
from update import update
from search import search
from load import load

DEFAULT_SETTINGS = {"last_update": -1}
TYPE_NAMES = ['P', 'B', 'CF', 'SP', 'AT', 'UVA']
MAP1 = {'P': 'P', 'B': 'B', 'C': 'CF', 'S': 'SP', 'A': 'AT', 'U': 'UVA', 'N': TYPE_NAMES}
MAP2 = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 'N': list(range(0, 8))}


def check_files() -> bool:
    path = os.path.join(os.getcwd(), 'lgct')

    def get_path(p: str):
        return os.path.abspath(os.path.join(path, p))

    def create_dir_if_not_exist(p: str) -> bool:
        if not os.path.exists(p):
            os.mkdir(p)
            return True
        return False

    def create_file_if_not_exist(p: str, text):
        if not os.path.exists(p):
            with open(p, 'w', encoding='utf-8') as f:
                json.dump(text, f)

    create_dir_if_not_exist(path)
    create_dir_if_not_exist(get_path('rule'))
    create_file_if_not_exist(get_path('settings.json'), DEFAULT_SETTINGS)

    if create_dir_if_not_exist(get_path('data')):
        return True
    for name in ['P', 'B', 'CF', 'SP', 'AT', 'UVA', 'tags']:
        if not os.path.exists(get_path(f'data/{name}.json')):
            return True
    return False


def get_real_file_name(file_name):
    if file_name.count('.') >= 1:
        return file_name
    else:
        return f'{file_name}.json'


def main():
    while True:
        os.system('cls')
        print()
        print('欢迎使用洛谷抽题!')
        print('在下方输入 -help 以获得帮助.\n')

        if check_files():
            print('没有发现题目数据或题目数据不完整!')
            print('在下方输入 -update 以获取题目数据. 这可能需要一段时间.\n')
        else:
            with open('lgct/settings.json', 'r', encoding='utf-8') as f:
                print(f'上次更新题目数据在 {json.load(f)["last_update"]}!')
                print('在下方输入 -update 以更新题目数据. 这可能需要一段时间.\n')

        file_name = input('请输入文件名/命令: ')
        if len(file_name) and file_name[0] == '-':
            if file_name in ['-update', '-u']:
                update()
            elif file_name in ['-search', '-s']:
                search()
            elif len(file_name) >= 2 and file_name[:2] == '-t':
                tmp = file_name.split()
                template(get_real_file_name(tmp[1]), tmp[2], int(tmp[3]))
            elif len(file_name) >= 2 and file_name[:2] == '-r':
                load({'type': MAP1[file_name[3]], 'difficulty': MAP2[file_name[4]]})
            else:
                webbrowser.open(f'https://www.luogu.com.cn/problem/{file_name[1:]}')
        else:
            with open(f'lgct/rule/{get_real_file_name(file_name)}', 'r', encoding='utf-8') as f:
                tmp = json.load(f)
            load(tmp)
            input('按 Enter 键继续...')


if __name__ == '__main__':
    while True:
        main()
