import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pprint
import csv
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv('CLIENT_ID'),
                                                               client_secret=os.getenv('CLIENT_SECRET')))

def get_list():
    reader = open("singles_list.json")
    data = json.load(reader)
    list = []

    for i in range(len(data)):
        title = data[i]["Title"]
        artist = data[i]["Artist"]
        try:
            track_title = title.split("\"")[1]
        except:
            print(title)
        year = data[i]["Year"]

        j = 0
        while year == "":
            j+=1
            year = data[i-j]["Year"]

        list.append([track_title,artist,year])
    return(list)

def get_spotify_data(title,artist):
    query = title + " " + artist
    result = sp.search(q=query,limit=1,type='track')
    try:
        track_id = result['tracks']['items'][0]['id']
        popularity = result['tracks']['items'][0]['popularity']

        artist_result = sp.search(q=artist,limit=1,type='artist')
        artist_popularity = artist_result['artists']['items'][0]['popularity']
        artist_followers = artist_result['artists']['items'][0]['followers']['total']
        print([title,popularity,artist_popularity,artist_followers])
        return(popularity,artist_popularity,artist_followers)
    except:
        print(title,artist)
    
def compile_data():
    list = get_list()
    f = open('data.csv','w')
    writer = csv.writer(f)

    for item in list:
        track = item[0]
        artist = item[1]
        popularity,artist_popularity,artist_followers = get_spotify_data(track,artist)
        item.append(popularity)
        item.append(artist_popularity)
        item.append(artist_followers)
        writer.writerow(item)

def youtube_data(title,artist):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("API_KEY")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q = title + " " + artist
    )
    
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    
    view_request = youtube.videos().list(
        part="statistics",
        id=video_id
    )
    view_response = view_request.execute()
    

compile_data()
youtube_data