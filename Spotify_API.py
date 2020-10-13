# Verschillende imports
import requests
import base64
import json
from urllib.parse import urlencode
from columnar import columnar

# Variabele
main_api = "https://accounts.spotify.com/api/token"
url = "https://api.spotify.com/v1/search?"
authHeader = {}
authData = {}
searchItem = ""
res = ""
clientID = "INSERT YOUR CLIENTID HERE"
clientSecrets = "INSERT YOUR CLIENTSECRET HERE"

# Base64 Encode Client ID and Client Secret + authorization token
def getAccesToken(clientID, clientSecrets):
    message = f"{clientID}:{clientSecrets}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    # print(base64_message)

    authHeader['Authorization'] = "Basic " + base64_message
    authData['grant_type'] = "client_credentials"
    res = requests.post(main_api, headers=authHeader, data=authData)

    responseObject = res.json()
    # print(json.dumps(responseObject, indent=2))
    jsonToken = json.loads(res.text)

    token = jsonToken["access_token"]
    # print(token)
    return token

# Nodig voor constructie van url
token = getAccesToken(clientID, clientSecrets)
headers = {'Authorization' : "Bearer " + token}

# Zoeken van artiest 
artist = input("Search by artist: ")
print('\n')
if artist == 'q' or artist == 'quit':
    exit()
while not artist:
    print("You need to typ in an artist. If you want to quit, typ: q or quit")
    artist = input("Search by artist: ")
    if artist == 'q' or artist == 'quit':
        exit()

# query opmaken
query = {
    "q": artist,
    "type": "artist",
}

# url opmaken
response = requests.get(f"{url}{urlencode(query)}", headers=headers).json()


# Loop voor alle artiesten met bijhorende genre en populariteit printen + opschonen lay-out van output
sum = 0
print("You've searched for '" + artist + "'. You can find the result below.")
for artists in response["artists"]["items"]:
    sum +=1
    data = [["Name", f"{artists['name']}"], ["ID", f"{artists['id']}"], ["Genre", f"{artists['genres']}"], ["Followers", f"{artists['followers']['total']}"], ["Popularity", f"{artists['popularity']}"]]
    table = columnar(data)
    print(table)

print(str(sum) + " results are found with the name: '" + str(artist) + "' in it.")