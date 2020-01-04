import json
import os
import shlex
import itertools
import requests
from datetime import datetime

PY_DIR = os.path.abspath(os.path.join(__file__,'..'))
CONFIG = {}
RIOTREQUEST = None

def set_var_if_none(var,default):
    return var if var != None else default

class RiotRequest:
    def __init__(self, api_info):
        self.api_info = api_info
        self.api_key = self.api_info['KEY']
        self.request_url = self.api_info['URL']
        self.header = self.api_info['HEADER']
        self.header["X-Riot-Token"] = self.header["X-Riot-Token"].format(api_key = self.api_key)
        self.special_urls = self.api_info['SPECIAL-URLS']

        champions_data = requests.get(self.special_urls["CHAMPIONS"]["INFO"]).json()['data']
        self.champions_data = {}
        for champ_data in champions_data.values():
            self.champions_data[int(champ_data['key'])] = champ_data


    def get_request_url(self, gateway, request_type):
        return self.request_url.format(gateway=gateway.lower(),request_type=request_type)

    def summoner_by_name(self, summonerName, gateway):
        url = self.get_request_url(gateway,self.special_urls['SUMMONER']["BY-NAME"]).format(summonerName=summonerName)
        summoner = requests.get(url, headers = self.header)
        return summoner.json()

    def champion_masteries(self, summonerId, gateway):
        url = self.get_request_url(gateway,self.special_urls['CHAMPIONS']["BY-NAME"]).format(encryptedSummonerId=summonerId)
        champions = requests.get(url, headers = self.header)
        return champions.json()

class RiotUser:
    def __init__(self,RIOTREQUEST, summonerName, gateway):
        self.riotrequest = RIOTREQUEST
        self.gateway = gateway
        self.userObj = self.riotrequest.summoner_by_name(summonerName,gateway)
        self.champions = None

    def set_champion_masteries(self):
        champions = self.riotrequest.champion_masteries(self.userObj['id'],self.gateway)
        for champ in champions:
            champ['data'] = self.riotrequest.champions_data[champ['championId']]
        self.champions = champions

    def get_champions_ranked(self):
        #call set_champion_masteries before hand
        output = []
        for champ in self.champions:
            output.append((champ['data']['name'],champ['championLevel'],champ['championPoints'],datetime.fromtimestamp(champ['lastPlayTime']/1000)))
        return sorted(output, key=lambda champ:champ[1:3], reverse=True)

def load_config():
    global CONFIG
    with open(os.path.join(PY_DIR,'config.json'),'r') as file:
        CONFIG = json.load(file)

def save_config():
    with open(os.path.join(PY_DIR,'config.json'),'w') as file:
        json.dump(CONFIG,file)

def parse_command_datatype(cmd):
    return cmd

def list_of_user_champions(username = None, gateway = None, queue = 100):
    username = set_var_if_none(username,CONFIG['USER']['USER'])
    gateway = set_var_if_none(gateway,CONFIG['USER']['GATEWAY'])
    print(user)

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
        me = RiotUser(RIOTREQUEST,CONFIG['USER']['USER'],CONFIG['USER']['GATEWAY'])
        me.set_champion_masteries()
        print('\n'.join(map(lambda k:' '.join(map(str,k)),me.get_champions_ranked())))

def require_config(attr, none_type, message = None, message_if_required = ''):
    if CONFIG['USER'][attr] == none_type:
        CONFIG['USER'][attr] = input(message_if_required)
    if message != None:
        print(message.replace(f'%%{attr}%%',CONFIG['USER'][attr]))

if __name__ == '__main__':
    load_config()
    RIOTREQUEST = RiotRequest(CONFIG['API'])
    require_config('USER',"",message='Logged in as master user %%USER%%',message_if_required='Log in as master user: ')
    require_config('GATEWAY',"",message='Using gateway %%GATEWAY%%', message_if_required='Use gateway: ')
    while True:
        command(*map(parse_command_datatype,shlex.split(input(''))))