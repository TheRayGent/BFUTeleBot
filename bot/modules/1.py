from configparser import ConfigParser, MissingSectionHeaderError, DuplicateSectionError, DuplicateOptionError
from os import path
from sys import argv
cfg = ConfigParser()
import datetime
tz = datetime.timezone(datetime.timedelta(hours=2))
filename = f'{datetime.datetime.today().astimezone(tz=tz).day}.{datetime.datetime.today().astimezone(tz=tz).month}'

with open(path.join(path.dirname(argv[0]), f'attendance/{filename}.txt'), mode='r', encoding='utf-8') as config_file:
    a = config_file.readlines()
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
    config_file = open(path.join(path.dirname(argv[0]), f'attendance/{filename}.txt'), mode='w', encoding='utf-8')
    config_file.write(b)
    config_file.close
    config_file = open(path.join(path.dirname(argv[0]), f'attendance/{filename}.txt'), mode='r', encoding='utf-8')
    a = config_file.read()



try:
    cfg.read_string(a)
except MissingSectionHeaderError:
    with open(path.join(path.dirname(argv[0]), f'attendance/{filename}.txt'), mode='r', encoding='utf-8') as config_file:
        a = '[Default]\n'+config_file.read()
        config_file = open(path.join(path.dirname(argv[0]), f'attendance/{filename}.txt'), mode='w', encoding='utf-8')
        config_file.write(a)
    cfg.read_string(a)



print([i[0] for i in cfg.items('Default')])
