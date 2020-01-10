from flask import Flask
from pylol import *

app = Flask(__name__)


@app.route('/<gateway>/<summonerName>/live-game/stats')
def live_game_stats(gateway,summonerName):


if __name__ == '__main__':
    load_config()
    handle_api_setup()