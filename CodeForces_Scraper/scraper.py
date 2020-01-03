from bs4 import BeautifulSoup
import json
import sys
import requests
import os
import shlex

CONFIG = {}

def get_config():
    global CONFIG
    with open('config.json','r') as file:
        CONFIG = json.load(file)

def set_config():
    print(CONFIG['CONFIG_MSG'])
    while True:
        args = shlex.split(input(''))
        config_command(*args)

def config_set_variable(var):
    if var.lower() == 'true':
        return True
    elif var.lower() == 'false':
        return False
    else:
        return var

def config_command(cmd, *args):
    global CONFIG
    cmd = cmd.upper()
    if cmd == 'FIND':
        print('\n'.join(filter(lambda key : args[0].upper() in key, CONFIG['USER'].keys())))
    elif cmd == 'SHOW':
        print('\n'.join(CONFIG['USER'].keys()))
    elif cmd == 'SET':
        CONFIG['USER'][args[0].upper()] = config_set_variable(args[1])
    elif cmd == 'GET':
        print(CONFIG['USER'][args[0].upper()])
    elif cmd == 'EXIT':
        with open('config.json','w') as file:
            json.dump(CONFIG,file)
        exit()
    elif cmd == 'RESET':
        CONFIG['USER'].update(CONFIG['DEFAULT'])

def help():
    print(CONFIG["HELP_MSG"])

def template_replace(template, **kwargs):
    for key, value in kwargs.items():
        template = template.replace(f'%%{key.upper()}%%', value)
    return template

def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')

def get_problem_ids():
    soup = get_soup(CONFIG['USER']['CODEFORCES_CONTEST_PAGE_VAL'])
    problems_obj = soup.find('table',class_ = 'problems')
    problem_temp = template_replace(CONFIG['USER']['CODEFORCES_PROBLEM_TEMP'], contest_id = CONFIG['USER']['CONTEST_ID'])
    problems = set()
    for pot_problem in problems_obj.find_all('a'):
        if problem_temp in pot_problem['href']:
            problems.add(pot_problem['href'].replace(problem_temp,''))
    return sorted(list(problems))

def get_file_name_problem(problem_id,problem_name):
    problem_name = problem_name.lower().replace(' ','-')
    if CONFIG['USER']['ORDER']:
        problem_name = f'{problem_id.lower()}-{problem_name}'
    return problem_name

def write_file(filename, contents):
    dir = os.path.join(os.getcwd(),filename)
    with open(dir, 'w') as file:
        file.writelines(contents)

def parse_io_data_probelm(data):
    if data[0] == '\n':
        data = data[1:]
    if data[-1] == '\n':
        data = data[:-1]
    return data

def write_problem(problem_id):
    problem_url = template_replace(CONFIG['USER']['CODEFORCES_PROBLEM_PAGE_TEMP'], contest_id = CONFIG['USER']['CONTEST_ID'],problem_id=problem_id)
    soup = get_soup(problem_url)
    problem_name = soup.find('div', class_ = 'title').text.replace(f'{problem_id}. ','')
    for i, input_source in enumerate(soup.find_all('div', class_ = 'input')):
        input_data = parse_io_data_probelm(input_source.find('pre').text)
        write_file(f'{get_file_name_problem(problem_id,problem_name)}.in.{i+1}',input_data)
    for i, output_source in enumerate(soup.find_all('div', class_ = 'output')):
        output_data = parse_io_data_probelm(output_source.find('pre').text)
        write_file(f'{get_file_name_problem(problem_id,problem_name)}.out.{i+1}',output_data)
    if CONFIG['USER']['CPP_FILE_CREATE']:
        os.system(f'cd "{os.getcwd()}";{CONFIG["USER"]["CPP_FILE_CREATE_COMMAND"]} {get_file_name_problem(problem_id,problem_name)}.cpp')

def main(contest_id):
    global soup
    config_command('SET','CONTEST_ID',contest_id)
    config_command('SET','CODEFORCES_CONTEST_PAGE_VAL',template_replace(CONFIG['USER']['CODEFORCES_CONTEST_PAGE_TEMP'],contest_id = contest_id))
    for problem_id in get_problem_ids():
        write_problem(problem_id)
    config_command('EXIT')

def handle_io():
    arg = sys.argv[1]
    if 'c' in arg:
        set_config()
    elif 'h' in arg:
        help()
    else:
        main(arg)

if __name__ == '__main__':
    get_config()
    handle_io()
