import json
import os
import shlex
import itertools
import requests
from bs4 import BeautifulSoup

PY_DIR = os.path.abspath(os.path.join(__file__,'..'))
CONFIG = {}

def load_config():
    global CONFIG
    with open(os.path.join(PY_DIR,'config.json'),'r') as file:
        CONFIG = json.load(file)

def save_config():
    with open(os.path.join(PY_DIR,'config.json'),'w') as file:
        json.dump(CONFIG,file)

def parse_command_datatype(cmd):
    return cmd

def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')

def set_var_if_none(var,default):
    return var if var != None else default

def list_of_user_champions(user = None, gateway = None, queue = 100):
    user = set_var_if_none(user,CONFIG['USER']['USER'])
    gateway = set_var_if_none(gateway,CONFIG['USER']['GATEWAY'])
    url_champs = f'https://lolprofile.net/summoner/{gateway.lower()}/{user.lower()}#Champions'
    soup = get_soup(url_champs)
    for i, champ_div in enumerate(soup.find('table').find_all('tr')):
        if i >= queue:
            return
        champ_name = champ_div.find('span', class_ = "champid").text
        champ_level = champ_div.find('span',class_ =  'cs').text
        champ_level = int(champ_level[champ_level.find('Level ')+len('Level '):])
        champ_winrate = champ_div.find('span',class_ = 'winrate').text
        yield f'Champion: {champ_name}, Level: {champ_level}, Winrate: {champ_winrate}'

def command(*args):
    if len(args) == 0:
        cmd = ''
    else:
        cmd = args[0].upper()
        args = list(args[1:])
    if cmd == 'HELP':
        print(CONFIG['HELP'])
    elif cmd == 'SET':
        CONFIG["USER"][args[0]] = args[1]
    elif cmd == 'RESET':
        CONFIG["USER"] = CONFIG["DEFAULTS"]
    elif cmd == 'SAVE':
        save_config()
    elif cmd == 'SHOW':
        print('\n'.join(map(lambda item , index: f'{index}\t{item[0]}\t{item[1]}',CONFIG['USER'].items(),itertools.count(1))))
    elif cmd == 'EXIT':
        save_config()
        exit()

    elif cmd == 'USER':
        sub_cmd = args[0].upper()
        args = list(args[1:])

        if sub_cmd == 'CHAMPIONS':
            print('\n'.join(list_of_user_champions(*args)))
    else:
        print("Dev AutoRun")

def require_config(attr, none_type, message = None, message_if_required = ''):
    if CONFIG['USER'][attr] == none_type:
        CONFIG['USER'][attr] = input(message_if_required)
    if message != None:
        print(message.replace(f'%%{attr}%%',CONFIG['USER'][attr]))

if __name__ == '__main__':
    load_config()
    require_config('USER',"",message='Logged in as master user %%USER%%',message_if_required='Log in as master user: ')
    require_config('GATEWAY',"",message='Using gateway %%GATEWAY%%', message_if_required='Use gateway: ')
    while True:
        command(*map(parse_command_datatype,shlex.split(input(''))))