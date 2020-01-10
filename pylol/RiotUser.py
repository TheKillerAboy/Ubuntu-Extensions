import math
from urllib.parse import quote

class RiotUser:
    def __init__(self, static_data, config, watcher, summonerName, summonerGateway, extra = {}):
        self.STATICDATA = static_data
        self.CONFIG = config
        self.WATCHER = watcher
        self.userData = self.WATCHER.summoner.by_name(summonerGateway, summonerName)
        self.gateway = summonerGateway
        self.matches = {}
        self.EXTRA = extra

    def set_matches_played(self, query = 20):
        startIndex = 0
        totalMatches = math.inf
        while startIndex < query and startIndex < totalMatches:
            endIndex = min(query, startIndex + self.CONFIG['API']['MAX-QUERY'], totalMatches)
            matches = self.WATCHER.match.matchlist_by_account(self.gateway,self.userData['accountId'], begin_index=startIndex,end_index= endIndex)

            for match in matches['matches']:
                self.matches[match['gameId']] = match

            totalMatches = matches['totalGames']
            startIndex = endIndex

    def matches_in_common(self, riotuser):
        #make sure both have ran set_matches_played
        selfMatches = set(self.matches.keys())
        otherMatches = set(riotuser.matches.keys())
        return [k for k in selfMatches if k in otherMatches]

    def get_live_match(self):
        try:
            return self.WATCHER.spectator.by_summoner(self.gateway,self.userData['id'])
        except:
            return None

    def live_match_method(self, query = 300):
        def user_abv(riotuser):
            return f'{self.STATICDATA["CHAMPIONS"]["data"][riotuser.EXTRA["parti"]["championId"]]["name"]} ({"blue" if riotuser.EXTRA["parti"]["teamId"] == 100 else "red"})({riotuser.userData["name"]})'
        match = self.get_live_match()
        if match is None:
            print("No live match found")
            return
        users = []
        for parti in match['participants']:
            users.append(RiotUser(self.STATICDATA,self.CONFIG,self.WATCHER,parti['summonerName'],self.gateway, {'parti':parti}))
        for user in users:
            print(f'https://lolprofile.net/summoner/{user.gateway[:-1]}/{quote(user.userData["name"])}#update')
        for user in users:
            user.set_matches_played(query)
            print(f'Got {user_abv(user)} Data')
        matches_common = {}
        for i in range(len(users)):
            for j in range(i+1,len(users)):
                matches_common[(i,j)] = users[i].matches_in_common(users[j])
                if len(matches_common[(i,j)]) > 0:
                    print(f'{user_abv(users[i])} - {user_abv(users[j])} has played {len(matches_common[(i,j)])} matches before')