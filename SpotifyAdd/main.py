import spotipy
import os
import sys
import json
import webbrowser
import spotipy.util as util
from pynput import keyboard
from json.decoder import JSONDecodeError
global spotifyObj, username

ATTEMPS = 500

def get_token():
    global username
    ClientID = 'bad8b6de67694ab78583db6f05d00d60'
    ClientSecret = '15030ee2233444719cba7dc7cb8ee951'
    #Get the username from therminal
    username = 'm2i3mws9tiaybw7o2zqhuqxua'
    scope = 'user-read-currently-playing playlist-modify-public'
    try:
        token = util.prompt_for_user_token(username,scope,client_id=ClientID,client_secret=ClientSecret,redirect_uri='https://www.google.com/')
    except:
        try:
            os.remove(f'.cachce-{username}')
            token = util.prompt_for_user_token(username,scope,client_id=ClientID,client_secret=ClientSecret,redirect_uri='https://www.google.com/')
        except:
            print("Error Auth")
            exit()
    global spotifyObj
    spotifyObj = spotipy.Spotify(auth=token)

    print("Auth")

def get_playlist_tracks(username,playlist_id):
    results = spotifyObj.user_playlist_tracks(username,playlist_id=playlist_id)
    tracks = results['items']
    while results['next']:
        results = spotifyObj.next(results)
        tracks.extend(results['items'])
    return tracks

def add_current_to_playlist():
    global username
    currentSong = spotifyObj.currently_playing()
    Ctrack = currentSong['item']['uri']
    playlistID = 'spotify:playlist:7coTTWaAyDXsSjCsOmWyDp'
    playlist = get_playlist_tracks(username,playlistID)
    tracks = set()
    for i,item in enumerate(playlist):
            tracks.add(item['track']['id'])
    if currentSong['item']['id'] not in tracks:
        spotifyObj.user_playlist_add_tracks(username,playlist_id=playlistID,tracks=[Ctrack])
        print(f"Added '{currentSong['item']['name']}'")
    else:
        print(f"Already added '{currentSong['item']['name']}'")


def on_release(key):
    if key == keyboard.Key.f9:
        i = 0
        while i < ATTEMPS:
            try:
                add_current_to_playlist()
                break
            except:
                get_token()
            i+=1
        if i == ATTEMPS:
            print(f"Error Adding song after {ATTEMPS} attempts")

get_token()

with keyboard.Listener(on_release=on_release) as keyboard_listener:
    keyboard_listener.join()