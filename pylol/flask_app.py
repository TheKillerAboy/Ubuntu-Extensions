from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

@app.route("/live-game")
def live_game():
    return "Hello world"

def run_html():
    def __run__():
        app.run(debug=True)
    thread = Thread(target=__run__)
    thread.start()