import json, requests, logging, os
from collections import Counter

logPath=f'{os.getcwd()}/debug.log'
if(os.name=='nt'):
    logPath=f'{os.getcwd()}\debug.log'

if os.path.exists(logPath):
        with open('debug.log', 'w') as x:
            x.close()

logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)

API_KEY="YOUR_API_KEY"

USER="YOUR_USERNAME"

LIMIT=1000

payload = {
    'method': 'user.getrecenttracks',
    'user': USER,
    'api_key': API_KEY,
    'format': 'json',
    'from': '1640955600',
    'to': '1667181599',
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
    logging.warning("Error pulling data from Last.FM servers, ensure you have a connection and all data is correct.")

i=0
while i<pages:
    i=i+1
    payload['page']=i
    request=getFromApi(payload)
    if(i==pages):
        LIMIT=int(1000-((pages*1000)-int(request["recenttracks"]["@attr"]["total"])))
    j=0
    while j<LIMIT:
        dataTable["track_name"].append(request['recenttracks']['track'][j]["name"]) # from here get data and put it in table
        dataTable["artist_name"].append(request['recenttracks']['track'][j]["artist"]['#text'])
        dataTable["album_name"].append(request['recenttracks']['track'][j]["album"]['#text'])
        j=j+1

mostListenedSong = Counter(dataTable['track_name']).most_common(5)
logging.info(mostListenedSong)
mostListenedArtist = Counter(dataTable['artist_name']).most_common(5)
logging.info(mostListenedArtist)
mostListenedAlbum = Counter(dataTable['album_name']).most_common(5)
logging.info(mostListenedArtist)

print(f"Welcome to your 2022 Wrapped, {USER}!\n\n")

print(f"""Your top 5 most listened songs are...
1.{mostListenedSong[0][0]} with {mostListenedSong[0][1]} plays!
2.{mostListenedSong[1][0]} with {mostListenedSong[1][1]} plays!
3.{mostListenedSong[2][0]} with {mostListenedSong[2][1]} plays!
4.{mostListenedSong[3][0]} with {mostListenedSong[3][1]} plays!
5.{mostListenedSong[4][0]} with {mostListenedSong[4][1]} plays!\n""")
print(f"""Your top 5 most listened artists are...
1.{mostListenedArtist[0][0]} with {mostListenedArtist[0][1]} plays!
2.{mostListenedArtist[1][0]} with {mostListenedArtist[1][1]} plays!
3.{mostListenedArtist[2][0]} with {mostListenedArtist[2][1]} plays!
4.{mostListenedArtist[3][0]} with {mostListenedArtist[3][1]} plays!
5.{mostListenedArtist[4][0]} with {mostListenedArtist[4][1]} plays!\n""")
print(f"""Your top 5 most listened albums are...
1.{mostListenedAlbum[0][0]} with {mostListenedAlbum[0][1]} plays!
2.{mostListenedAlbum[1][0]} with {mostListenedAlbum[1][1]} plays!
3.{mostListenedAlbum[2][0]} with {mostListenedAlbum[2][1]} plays!
4.{mostListenedAlbum[3][0]} with {mostListenedAlbum[3][1]} plays!
5.{mostListenedAlbum[4][0]} with {mostListenedAlbum[4][1]} plays!""")
