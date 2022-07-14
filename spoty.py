import requests
import base64
import json

# Step 1 - Authorization : to make a request, send the parameters below
url = "https://accounts.spotify.com/api/token"  # url endpoint 
headers = {}                                    # to send access tokens 
data = {}                                       # part of the payload

with open(r"secret.txt") as f:
        secret_ls = f.readlines()
        cid = secret_ls[0][:-1]
        secret = secret_ls[1]
        f.close()

cid = cid.strip()
secret = secret.strip()

def getAccessToken(cid, secret):
    # Encode as Base64
    message = f"{cid}:{secret}"
    messageBytes = message.encode('ascii')       # Convert into bytes
    base64Bytes = base64.b64encode(messageBytes) # base64 encode it
    base64Message = base64Bytes.decode('ascii')  # convert bytes back to a string

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    res = requests.post(url, headers=headers, data=data) 
    responseObject = res.json()
    accessToken = responseObject['access_token']

    return accessToken

def getPlaylistTracks(token, playlistID):
    
    playlistUrl = f"https://api.spotify.com/v1/playlists/{playlistId}"

    getHeader = {
    "Authorization": "Bearer " + token
    }

    res = requests.get(url=playlistUrl, headers=getHeader)
    playlistObject = res.json()

    return playlistObject 

# API requests 
token = getAccessToken(cid, secret)
playlistId = "1ln3cEShWn4dcwBfjvluVT?si=b6db598ffc454925"

tracklist = getPlaylistTracks(token, playlistId)

with open('tracklist.json', 'w') as f:
    json.dump(tracklist, f)

#longsongs = []

for t in tracklist['tracks']['items']:
    songNames = t['track']['name']
    duration = t['track']['duration_ms']
    print(" " , songNames, " - ", duration)
    





