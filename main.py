import json, requests, pandas as pd, logging, csv, os
from collections import Counter
import urllib.request
from datetime import datetime # to get year

year = datetime.date.today().year
beginEpoch = str(datetime(year, 1, 1, 0, 0).timestamp())
endEpoch = str(datetime(year, 10, 31, 0, 0).timestamp())

logPath=f'{os.getcwd()}/debug.log'
if(os.name=='nt'):
    logPath=f'{os.getcwd()}\debug.log'

if os.path.exists(logPath):
        with open('debug.log', 'w') as x:
            x.close()

logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)

def connect(host='http://google.com'): # check if user is connected to internet
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

logging.debug('Checking for internet connection.')
if connect() == False:
    logging.critical('Could not detect internet connection, quitting...')
    print("\033[91m[ERROR] You don't have a connection to the internet, please connect and try again")
logging.debug("Check successful.")

API_KEY="YOUR_API_KEY"

USER="YOUR_USERNAME"

LIMIT=1000

payload = {
    'method': 'user.getrecenttracks',
    'user': USER,
    'api_key': API_KEY,
    'format': 'json',
    'from': beginEpoch,
    'to': endEpoch,
    'limit': LIMIT,
    'page': '1'
}

dataTable = {'track_name': [], 'artist_name': [], 'album_name': []}

def getFromApi(params):
    r = requests.get('https://ws.audioscrobbler.com/2.0/', params=params) # NOTE: this returns a dict, not json!!!!
    return r.json()

try:
    pages=int(getFromApi(payload)["recenttracks"]["@attr"]["totalPages"])
except:
    logging.critical("Error pulling data from Last.FM servers, ensure all data is correct.")
    print("\033[91m[ERROR] Data could not be pulled from last.fm servers, ensure all data is correct.")
    exit()

i=0
while i<pages:
    i=i+1
    payload['page']=i
    request=getFromApi(payload)
    if(i==pages):
        LIMIT=int(LIMIT-((pages*LIMIT)-int(request["recenttracks"]["@attr"]["total"])))
    j=0
    while j<LIMIT:
        dataTable["track_name"].append(request['recenttracks']['track'][j]["name"]) # from here get data and put it in table
        dataTable["artist_name"].append(request['recenttracks']['track'][j]["artist"]['#text'])
        dataTable["album_name"].append(request['recenttracks']['track'][j]["album"]['#text'])
        j=j+1

noToCount=3 # number of songs, albums, artists to count

mostListenedSong = Counter(dataTable['track_name']).most_common(noToCount)
logging.info(mostListenedSong)
mostListenedArtist = Counter(dataTable['artist_name']).most_common(noToCount)
logging.info(mostListenedArtist)
mostListenedAlbum = Counter(dataTable['album_name']).most_common(noToCount)
logging.info(mostListenedArtist)

print(f"Welcome to your {year} Wrapped, {USER}!\n\n")

i=0
print(f"Your top {noToCount} most listened songs are...\n")
while i<noToCount:
    i=i+1
    print(f'{i}. {mostListenedSong[i-1][0]} with {mostListenedSong[i-1][1]} plays!')
print('\n')

i=0
print(f"Your top {noToCount} most listened artists are...\n")
while i<noToCount:
    i=i+1
    print(f'{i}. {mostListenedArtist[i-1][0]} with {mostListenedArtist[i-1][1]} plays!')
print('\n')

i=0
print(f"Your top {noToCount} most listened albums are...\n")
while i<noToCount:
    i=i+1
    print(f'{i}. {mostListenedAlbum[i-1][0]} with {mostListenedAlbum[i-1][1]} plays!')
