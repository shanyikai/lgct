import os
import json
import random
import webbrowser


def get_real_file_name(file_name):
    if file_name.count('.') >= 1:
        return file_name
    else:
        return f'{file_name}.json'


def get_from_rule(rule):
    problems = []
    if 'type' not in rule.keys() or rule['type'] == 'all':
        rule['type'] = ['P', 'B', 'CF', 'SP', 'AT', 'UVA']
    elif 'type' in rule.keys() and type(rule['type']) is str:
        rule['type'] = [rule['type']]
    for type_name in rule['type']:
        with open(f'lgct/data/{type_name}.json', 'r', encoding='utf-8') as f:
            for problem in json.load(f):
                problems.append(problem)

    if 'difficulty' in rule.keys() and type(rule['difficulty']) is int:
        rule['difficulty'] = [rule['difficulty']]

    if 'ignore' not in rule.keys():
        rule['ignore'] = 2

    with open('lgct/data/tags.json', 'r', encoding='utf-8') as f:
        tags = json.load(f)['id']

    result = []
    for problem in problems:
        if 'difficulty' in rule.keys() and rule['difficulty'] != 'all':
            if problem['difficulty'] not in rule['difficulty']:
                continue

        if 'translated' in rule.keys() and rule['translated'] != 'all':
            if problem['wantsTranslation'] == rule['translated']:
                continue

        if 'have' in rule.keys():
            if type(rule['have'][0]) is int:
                res = False
                for tag in problem['tags']:
                    if tag in rule['have']:
                        res = True
                if not res:
                    continue
            else:
                res = False
                for order in rule['have']:
                    tmp = True
                    for tag in order:
                        if tag not in problem['tags']:
                            tmp = False
                    res = res or tmp
                if not res:
                    continue

        if 'no' in rule.keys():
            if type(rule['no'][0]) is int:
                res = True
                for tag in rule['no']:
                    if tag in problem['tags']:
                        res = False
                if not res:
                    continue
            else:
                res = False
                for order in rule['no']:
                    tmp = True
                    for tag in problem['tags']:
                        if tag not in order:
                            tmp = False
                    res = res or tmp
                if res:
                    continue

        if 'in' in rule.keys():
            res = False
            for order in rule['in']:
                tmp = True
                tmp2 = True
                if rule['ignore'] == 1:
                    if len(problem['tags']) == 0:
                        continue
                if rule['ignore'] == 2:
                    tmp2 = False
                for tag in problem['tags']:
                    if tag in order:
                        tmp2 = True
                    if tags[str(tag)]['type'] in [1, 3, 4, 5, 6]:
                        if rule['ignore'] in [2, 3]:
                            continue
                    if tag not in order:
                        tmp = False
                res = res or (tmp and tmp2)
            if not res:
                continue

        result.append(problem['pid'])

    return result


def get_type(rules):
    if type(rules[0]) is str:
        return 'special'
    if len(rules) and 'text' in rules[0].keys():
        return 'weighted_special'
    for rule in rules:
        if 'weight' in rule.keys():
            return 'weighted'
    return 'standard'


def get_from_file(rules):
    if type(rules) is dict:
        rules = [rules]

    type_name = get_type(rules)
    if type_name == 'special':
        return rules

    elif type_name == 'weighted_special':
        result = []
        for rule in rules:
            if 'weight' in rule.keys():
                result += [rule['text']] * rule['weight']
            else:
                result.append(rule['text'])
        return result

    elif type_name == 'standard':
        result = []
        for rule in rules:
            result += get_from_rule(rule)
        return list(set(result))

    elif type_name == 'weighted':
        result = []
        for rule in rules:
            if 'weight' in rule.keys():
                result += get_from_rule(rule) * rule['weight']
            else:
                result += get_from_rule(rule)
        return result


def load(text):
    problems = get_from_file(text)
    real = list(set(problems))

    os.system('cls')
    if len(real):
        print(f'找到 {len(real)} 个符合条件的题目.')
    else:
        print('没有找到符合条件的题目! ')
        return

    while True:
        command = input('\n请输入命令: ')

        if command in ['q', 'quit', '-q', '-quit']:
            break

        if command in ['s', 'save', '-s', '-save']:
            file_name = input('请输入文件名: ')
            file_name = get_real_file_name(file_name)
            if os.path.exists(f'lgct/rule/{file_name}'):
                tmp = input(f'文件 lgct/rule/{file_name} 已经存在! 是否要替换? (y/n) ')
                if tmp in ['n', 'no', 'N', 'No', 'NO']:
                    continue
            with open(f'lgct/rule/{file_name}', 'w', encoding='utf-8') as f:
                json.dump(problems, f)
            print('完成!')
            continue

        sort = False
        if command and command[0] == '!':
            sort = True
            command = command[1:]

        if command in ['.', '']:
            command = '0'

        command = int(command)

        if command == 0:
            result = random.choice(problems)
            print(f'{result}')
            webbrowser.open(f'https://www.luogu.com.cn/problem/{result}')

        elif command < 0:
            command = -1 * command
            result = []
            for cnt in range(command):
                result.append(random.choice(problems))
            if sort:
                result.sort()
            print(result)

        else:
            if command > len(real):
                print('没有这么多题目! ')
                command = len(real)
            result = []
            random.shuffle(problems)
            for p in problems:
                if len(result) == command:
                    break
                if p not in result:
                    result.append(p)
            if sort:
                result.sort()
            print(result)
