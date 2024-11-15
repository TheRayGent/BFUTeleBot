from configparser import ConfigParser, MissingSectionHeaderError
from os import path
from sys import argv
cfg = ConfigParser()
import datetime
tz = datetime.timezone(datetime.timedelta(hours=2))
filename = f'{datetime.datetime.today().astimezone(tz=tz).day}.{datetime.datetime.today().astimezone(tz=tz).month}'

try:
    cfg.read(f'bot/modules/attendance/{filename}.txt', encoding='utf-8')
except MissingSectionHeaderError:
    with open(path.join(path.dirname(argv[0]), f'attendance/{filename}.txt'), mode='r', encoding='utf-8') as config_file:
        a = '[Default]\n'+config_file.read()
        config_file = open(path.join(path.dirname(argv[0]), f'attendance/{filename}.txt'), mode='w', encoding='utf-8')
        config_file.write(a)
    cfg.read_string(a)



print([i[0] for i in cfg.items('Default')])
