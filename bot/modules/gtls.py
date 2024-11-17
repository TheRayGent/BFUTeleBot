from configparser import ConfigParser, MissingSectionHeaderError
from os import path
from sys import argv

import datetime
tz = datetime.timezone(datetime.timedelta(hours=2))
from aiogram import Bot

class ConfigParserCaseSensitive(ConfigParser):
    def optionxform(self, optionstr):
        return optionstr


async def get_list(bot: Bot, filename: str, good: bool = False) -> str:
    cfg = ConfigParserCaseSensitive()
    pathname = f'attendance/{filename}.txt' if __name__ == '__main__' else f'modules/attendance/{filename}.txt'
    with open(path.join(path.dirname(argv[0]), f'{pathname}'), mode='r', encoding='utf-8') as config_file:
        a = config_file.readlines()
        if a == []:
            return 'Такой файл не обнаружен!'
        b = []+a
        for i in range(len(b)):
            if b[i].count(' = ')>0:
                b[i] = b[i][:b[i].index(' = ')]
        for i in range(len(b)):
            c=b[i]
            while b.count(c)>1 and c!='':
                a[b.index(c)] = ''
                b[b.index(c)] = ''
        b = ''
        for i in a:
            b+=i
        config_file = open(path.join(path.dirname(argv[0]), f'{pathname}'), mode='w', encoding='utf-8')
        config_file.write(b)
        config_file.close
        config_file = open(path.join(path.dirname(argv[0]), f'{pathname}'), mode='r', encoding='utf-8')
        a = config_file.read()
    try:
        cfg.read_string(a)
    except MissingSectionHeaderError:
        with open(path.join(path.dirname(argv[0]), f'{pathname}'), mode='r', encoding='utf-8') as config_file:
            a = '[Default]\n'+config_file.read()
            config_file = open(path.join(path.dirname(argv[0]), f'{pathname}'), mode='w', encoding='utf-8')
            config_file.write(a)
        cfg.read_string(a)
    dict1 = [i[0] for i in cfg.items('Default')]
    dict2 = [i[1] for i in cfg.items('Default')]
    dict1 = [i.split('_') for i in dict1]
    for i in range(len(dict1)):
        dict1[i]+=[dict2[i]]
    dict3 = {}
    for i in dict1:
        dict3[i[0]] = {}
    for i in dict1:
        dict3[i[0]][i[1]] = {}    
    for i in dict1:
        dict3[i[0]][i[1]][i[2]] = i[3]

    dict1 = sorted([i for i in [j for j in dict3]], reverse=True)
    text = ''
    if good == False:
        for i in dict1:
            text+=f'<i>{i}</i>\n'
            for j in dict3[i]:
                text+=f'    <b>{j}</b>\n'
                for k in dict3[i][j]:
                    if dict3[i][j][k]=='2':
                        text+=f'        @{(await bot.get_chat(int(k))).username} - Не уваж.\n'
                    elif dict3[i][j][k]=='3':
                        text+=f'        @{(await bot.get_chat(int(k))).username} - Уваж.\n'
    else:
        for i in dict1:
            text+=f'<i>{i}</i>\n'
            for j in dict3[i]:
                text+=f'    <b>{j}</b>\n'
                for k in dict3[i][j]:
                    if dict3[i][j][k]=='1':
                        text+=f'        @{(await bot.get_chat(int(k))).username} - Был\n'
    #print(text)
    return text

#asyncio.run(get_list())