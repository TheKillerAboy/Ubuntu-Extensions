import json
import os
import shlex
from riotwatcher import RiotWatcher
from RiotUser import RiotUser
from flask import Flask, render_template
from threading import Thread
from urllib.parse import quote

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
        riotuser.live_match_method()

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
    elif cmd == 'RELOG':
        CONFIG['USER']['SUMMONER-NAME'] = ''
        CONFIG['USER']['SUMMONER-GATEWAY'] = ''
        handle_login()
    elif cmd == 'SHOW':
        for name, setting in CONFIG['USER'].items():
            print(f'{name}: {setting}')
    elif cmd == 'SET':
        CONFIG['USER'][args[0]] = args[1]
    elif cmd == 'ME':
        user_commands(MASTERUSER, *args)
    elif cmd == 'USER':
        user_commands(RiotUser(STATICDATA,CONFIG,WATCHER,args[0],CONFIG['SUMMONER-GATEWAY']), *args[1:])
    elif cmd == '':
        print('Global Dev AutoRun')

def handle_login():
    global MASTERUSER
    if CONFIG['USER']['SUMMONER-NAME'] == '':
        CONFIG['USER']['SUMMONER-NAME'] = input('Login as master summoner: ').lower()
    print(f"Logged in as master summoner: {CONFIG['USER']['SUMMONER-NAME']}")
    if CONFIG['USER']['SUMMONER-GATEWAY'] == '':
        print(f"Available Gateways:\n{' '.join(CONFIG['ALL-GATEWAYS'])}")
        while True:
            CONFIG['USER']['SUMMONER-GATEWAY'] = input('Login with gateway: ').lower()
            if CONFIG['USER']['SUMMONER-GATEWAY'].upper() not in CONFIG['ALL-GATEWAYS']:
                print("Unknown Gateway")
            else:
                break
    print(f"Logged in with gateway: {CONFIG['USER']['SUMMONER-GATEWAY']}")
    MASTERUSER = RiotUser(STATICDATA,CONFIG,WATCHER, CONFIG['USER']['SUMMONER-NAME'], CONFIG['USER']['SUMMONER-GATEWAY'])



def handle_api_setup():
    global WATCHER, STATICDATA
    WATCHER = RiotWatcher(CONFIG['API']['KEY'])
    STATICDATA['VERSION'] = WATCHER.data_dragon.versions_for_region(CONFIG['API']['DATA-DRAGON-GATEWAY'])
    STATICDATA = {
        "CHAMPIONS":WATCHER.data_dragon.champions(STATICDATA['VERSION']['v']),
        "ITEMS":WATCHER.data_dragon.items(STATICDATA['VERSION']['v']),
    }
    extra_data = {}
    for champName, champData in STATICDATA['CHAMPIONS']['data'].items():
        extra_data[int(champData['key'])] = champData
    STATICDATA['CHAMPIONS']['data'].update(extra_data)

app = Flask(__name__)

@app.route('/')
def live_game():
    def champ_spec_id(user):
        return f"{STATICDATA['CHAMPIONS']['data'][user['championId']]['name']} ({user['team']})({user['user'].userData['name']})"
    match = MASTERUSER.get_live_match()
    if match is None:
        return "No Live Match"
    members = []
    for parti in match['participants']:
        members.append({
            'user':RiotUser(STATICDATA,CONFIG,WATCHER, parti['summonerName'], CONFIG['USER']['SUMMONER-GATEWAY']),
            'team':"blue" if parti['teamId'] == 100 else "red",
            'championId':parti['championId'],
            'championName':STATICDATA['CHAMPIONS']['data'][parti['championId']]['name']
        })
        members[-1]['user'].set_matches_played(200)
        print(f"Got User {champ_spec_id(members[-1])}'s Data")
    matchup = {}
    for i in range(len(members)):
        for j in range(i+1,len(members)):
            matchup[(i,j)] = members[i]['user'].matches_in_common(members[j]['user'])
    teams__ = []
    for k in range(2):
        teams__.append([])
        team__ = [i for i in range(k*5,(k+1)*5)]
        while len(team__) > 0:
            i = team__[0]
            team_ = [i]
            team__.remove(i)
            for j in team__.copy():
                if len(matchup[(i,j)]) >= 5:
                    team_.append(j)
                    team__.remove(j)
            teams__[-1].append(team_)
    for member in members:
        lanes = {}
        roles = {}
        i = 0
        for matchId, match in member['user'].matches.items():
            if match['champion'] == member['championId']:
                if match['lane'] not in lanes:
                    lanes[match['lane']] = 1
                else:
                    lanes[match['lane']] += 1
                if match['role'] not in roles:
                    roles[match['role']] = 1
                else:
                    roles[match['role']] += 1
                i+=1
            if i >= 20:
                break
        try:
            member['role'] = f'{max(lanes.items(),key = lambda lane : lane[1])[0]} {max(roles.items(),key = lambda role : role[1])[0]}'
        except:
            member['role'] = "NONE"
    for member in members:
        try:
            res = WATCHER.champion_mastery.by_summoner_by_champion(member['user'].gateway,member['user'].userData['id'], member['championId'])
            member['lvl'] = res['championLevel']
            member['pts'] = res['championPoints']
        except:
            member['lvl'] = 0
            member['pts'] = 0
    teams = {'blue':[],'red':[]}
    for i, color in enumerate(['blue','red']):
        for team in teams__[i]:
            teams[color].append([])
            for mem in team:
                teams[color][-1].append({
                    'role' : members[mem]['role'],
                    'champion':{
                        'name': members[mem]['championName'],
                        'level':members[mem]['lvl'],
                        'pts':members[mem]['pts']
                    },
                    'username':members[mem]['user'].userData['name'],
                    'lolprofile':f'https://lolprofile.net/summoner/{members[mem]["user"].gateway[:-1]}/{quote(members[mem]["user"].userData["name"])}#update',
                    'pfp':CONFIG['API']['CHAMPION-PFP'].format(champ_pfp_id=f"{STATICDATA['CHAMPIONS']['data'][members[mem]['championId']]['id']}_0")
                })
    return render_template('index.html',teams = teams, username = MASTERUSER.userData['name'], colors = ['blue','red'])


def run_html():
    def __run__():
        app.run(debug=False)
    thread = Thread(target=__run__)
    thread.start()

if __name__ == '__main__':
    load_config()
    handle_api_setup()
    handle_login()
    run_html()
    while True:
        global_commands(*map(raw_input_handle,shlex.split(input(""))))