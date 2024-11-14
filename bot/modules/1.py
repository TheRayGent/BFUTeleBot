from configparser import ConfigParser, MissingSectionHeaderError
from os import path
from sys import argv
cfg = ConfigParser()

try:
    cfg.read('bot/modules/attendance/13.11.txt', encoding='utf-8')
except MissingSectionHeaderError:
    with open(path.join(path.dirname(argv[0]), 'attendance/13.11.txt'), mode='r', encoding='utf-8') as config_file:
        a = '[Default]'+config_file.read()
        config_file = open(path.join(path.dirname(argv[0]), 'attendance/13.11.txt'), mode='w', encoding='utf-8')
        config_file.write(a)
    cfg.read_string(a)


print([i[0] for i in cfg.items('Default')])