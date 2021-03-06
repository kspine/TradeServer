# -*- coding: utf-8 -*-
# @Time    : 2017/12/2 20:40
# @Author  : Hochikong
# @Email   : hochikong@foxmail.com
# @File    : maintainctl.py
# @Software: PyCharm

from configparser import ConfigParser
from stockclib.omServ import modify_print, generate_and_write, helper_print, update_signal
import pymongo
import re

# --------------------------------------
# Load config.ini and read configuration
CONFIG_FILE = 'config.ini'
DB_SECTION = 'DB'
cfg = ConfigParser()
cfg.read(CONFIG_FILE)

# ----------------
# regular expression compile
generateuser = re.compile("gen -m \d{1,8}")
checkusers = re.compile("check -a")
exitctl = re.compile("exit")
helper = re.compile("help")
signal_run = re.compile("signal -r")
signal_halt = re.compile("signal -h")
# deleteuser = re.compile("delete -id")

if __name__ == "__main__":
    connection = pymongo.MongoClient(cfg.get(DB_SECTION, 'address'), int(cfg.get(DB_SECTION, 'port')))
    if connection.admin.authenticate(
            cfg.get(DB_SECTION, 'user'),
            cfg.get(DB_SECTION, 'passwd'),
            mechanism='SCRAM-SHA-1',
            source=cfg.get(DB_SECTION, 'database')):
        pass
    else:
        raise Exception('Error configure on user or password! ')
    sysdatabase = connection[cfg.get(DB_SECTION, 'database')]
    collect_traders = sysdatabase['traders']
    collect_oms = sysdatabase['ordermatch_service']

    while True:
        cmd = input('What to do? ')
        if generateuser.match(cmd):
            generate_and_write(cmd, collect_traders)
            print('\n')
        elif checkusers.match(cmd):
            rawdata = list(collect_traders.find())
            modify_print(rawdata)
            print('\n')
        elif exitctl.match(cmd):
            print('Exiting...', '\n')
            break
        elif helper.match(cmd):
            helper_print()
            print('\n')
        elif signal_run.match(cmd):
            update_signal(collect_oms, 'run')
            print('Order matching service running')
            print('\n')
        elif signal_halt.match(cmd):
            update_signal(collect_oms, 'halt')
            print('Order matching service stop')
            print('\n')
        else:
            print('Wrong command!')
            print('\n')


