import json
import os
import shlex
from riotwatcher import RiotWatcher, ApiError
from RiotUser import RiotUser
import math

PYLOL_DIR = os.path.abspath(os.path.join(__file__,'..'))
CONFIG = None
WATCHER = None
MASTERUSER = None
STATICDATA = {}

def load_config():
    global CONFIG
    with open(os.path.join(PYLOL_DIR,'config.json'),'r') as f:
        CONFIG = json.load(f)

def save_config():
    with open(os.path.join(PYLOL_DIR, 'config.json'), 'w') as f:
        json.dump(CONFIG,f)

def raw_input_handle(raw):
    return raw

def parse_dev_input(args):
    cmd = ''
    if len(args) > 0:
        cmd = args[0].upper()
        args = args[1:]
    return cmd, args

def user_commands(riotuser, *args):
    cmd, args = parse_dev_input(args)
    print(cmd)
    if cmd == '':
        print('User Dev AutoRun')
        riotuser.set_matches_played(math.inf)

def global_commands(*args):
    cmd, args = parse_dev_input(args)
    if cmd == 'HELP':
        print(CONFIG['HELP'])
    elif cmd == 'RESET':
        CONFIG['USER'] = CONFIG['USER-DEFAULT']
    elif cmd == 'EXIT':
        global_commands('SAVE')
        exit()
    elif cmd == 'SAVE':
        save_config()
    elif cmd == 'SHOW':
        for name, setting in CONFIG['USER'].items():
            print(f'{name}: {setting}')
    elif cmd == 'SET':
        CONFIG['USER'][args[0]] = args[1]
    elif cmd == 'ME':
        user_commands(MASTERUSER, *args)
    elif cmd == 'USER':
        user_commands(RiotUser(CONFIG,WATCHER,args[0],CONFIG['SUMMONER-GATEWAY']), *args[1:])
    elif cmd == '':
        print('Global Dev AutoRun')

def handle_login():
    global MASTERUSER
    if CONFIG['USER']['SUMMONER-NAME'] == '':
        CONFIG['USER']['SUMMONER-NAME'] = input('Login as master summoner: ').lower()
    if CONFIG['USER']['SUMMONER-GATEWAY'] == '':
        print(f"Available Gateways:\n{' '.join(CONFIG['ALL-GATEWAYS'])}")
        while True:
            CONFIG['USER']['SUMMONER-GATEWAY'] = input('Login with gateway: ').lower()
            if CONFIG['USER']['SUMMONER-GATEWAY'].upper() not in CONFIG['ALL-GATEWAYS']:
                print("Unknown Gateway")
            else:
                break
    MASTERUSER = RiotUser(CONFIG,WATCHER, CONFIG['USER']['SUMMONER-NAME'], CONFIG['USER']['SUMMONER-GATEWAY'])

def handle_api_setup():
    global WATCHER, STATICDATA
    WATCHER = RiotWatcher(CONFIG['API']['KEY'])
    print(WATCHER.data_dragon.versions_for_region(CONFIG['API']['DATA-DRAGON-GATEWAY']))
    STATICDATA = {
        "CHAMPIONS":WATCHER.data_dragon.champions(CONFIG['API']['DATA-DRAGON-GATEWAY']),
        "ITEMS":WATCHER.data_dragon.items(CONFIG['API']['DATA-DRAGON-GATEWAY']),
    }

if __name__ == '__main__':
    load_config()
    handle_api_setup()
    handle_login()
    while True:
        global_commands(*map(raw_input_handle,shlex.split(input(""))))