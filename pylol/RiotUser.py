import math

class RiotUser:
    def __init__(self, config, watcher, summonerName, summonerGateway):
        self.CONFIG = config
        self.WATCHER = watcher
        self.userData = self.WATCHER.summoner.by_name(summonerGateway, summonerName)
        self.gateway = summonerGateway
        self.matches = {}

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
        return selfMatches.union(otherMatches)