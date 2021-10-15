import requests, json, sys, os, re


if os.path.exists('./key.txt'):
    with open('key.txt', 'r') as file:
        api_key = file.read()
        if not re.fullmatch(r'[A-Z0-9]{32}', api_key):
            print('Invalid key')
            sys.exit()
else:
    with open('key.txt', 'r') as file:
        file.write('PUT YOUR KEY XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')


dota_id = '570' # 205790


session = requests.Session()
session.header = {
    "Accept-Language" : "ru",
    "User-Agent" : "Mozilla/5.0"
}


def get_matches(start=0, matches_requested=500):
    response = session.get(f'http://api.steampowered.com/IDOTA2Match_{dota_id}/GetMatchHistory/v1?key={api_key}&game_mode=1&matches_requested={matches_requested}', timeout=5)
    if response.status_code == 200:
        print('Data loaded', end='')
    else:
        print('Loading failed\n', response)
        sys.exit()
    return response.json()


def dump(data, name):
    with open(f'./{name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, sort_keys=True, indent=2)


def id_transform(id, out=64):
    base = 76561197960265728
    if out == 64:
        return id + base
    elif out == 32:
        return id - base
    else:
        raise AttributeError('Wrong output format was asked')


def get_users_names(users_id):
    names = []
    users = session.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?steamids={users_id}&key={api_key}', timeout=5).json()
    for user in users['responce']['players']:
       names.append(user['personaname'])
    return names


"""
match = {
    'matches' : [
    {
        'id' : 0,
        'radiant' : [1, 2, 3, 4, 5],
        'dire' : [6, 7, 8, 9, 10],
        'winner' : 0
    },
    {
       'id' : 1,
        'radiant' : [1, 2, 3, 4, 5],
        'dire' : [6, 7, 8, 9, 10],
        'winner' : 0 
    }]
}
"""

# for i in range(0, 10001, 500):
#     dump(get_matches(start=i), i + 500)

dump(get_matches(matches_requested=10000), name='data')