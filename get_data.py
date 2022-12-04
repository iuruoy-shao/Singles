import json
import os
import csv
import datetime
from datetime import date
from datetime import datetime
import requests
import urllib.parse

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                                                            client_secret=os.getenv('CLIENT_SECRET'),
                                                            redirect_uri=os.getenv('URI'),
                                                            scope="playlist-modify-private"))

DEVELOPER_KEY = os.getenv("API_KEY")

search_url = "https://youtube.googleapis.com/youtube/v3/search?"
list_url = "https://youtube.googleapis.com/youtube/v3/videos?"

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

        list.append([track_title,artist,int(year)])
    return(list)

def get_spotify_data(title,artist):
    query = title + " " + artist
    result = sp.search(q=query,limit=1,type='track')
    try:
        track_id = result['tracks']['items'][0]['id']
        popularity = int(result['tracks']['items'][0]['popularity'])

        artist_result = sp.search(q=artist,limit=1,type='artist')
        artist_popularity = int(artist_result['artists']['items'][0]['popularity'])
        artist_followers = int(artist_result['artists']['items'][0]['followers']['total'])
        artist_genres = artist_result['artists']['items'][0]['genres']
        return(popularity,artist_popularity,artist_followers,artist_genres)
    except:
        print(title,artist)

def get_track_ids():
    writer = csv.writer(open('track_id.csv','w'))
    for track in get_list():
        title = track[0]
        artist = track[1]
        query = title + " " + artist
        result = sp.search(q=query,limit=1,type='track')
        track_id = result['tracks']['items'][0]['id']
        writer.writerow([track_id])
    
def compile_data(start,end):
    list = get_list()
    f = open('data.csv','a')
    writer = csv.writer(f)

    for i in range(start,end):
        song = list[i]
        track = song[0]
        artist = song[1]
        # years_since_release = current_year - item[2]
        try:
            popularity,artist_popularity,artist_followers,artist_genres = get_spotify_data(track,artist)
            view_count,upload_date = youtube_data(track,artist)

            #'2011-05-30T13:12:47Z'
            days_elapsed = (datetime.now() - datetime.strptime(upload_date, "%Y-%m-%dT%H:%M:%SZ")).days
            for attribute in [popularity,artist_popularity,artist_followers,artist_genres,view_count,days_elapsed]:
                song.append(attribute)
            writer.writerow(song)
        except:
            break

def youtube_data(track_name,artist):
    search_params = [
        ('type', 'video'),
        ('part', 'snippet'), 
        ('part', 'id'),
        ('maxResults', '1'), 
        ('order', 'relevance'),
        ('q', track_name + " " + artist),
        ('key', DEVELOPER_KEY)
    ] 
    response = requests.get(search_url + urllib.parse.urlencode(search_params)).json()
    video_id = response["items"][0]["id"]["videoId"]
    publish_date = response["items"][0]["snippet"]["publishedAt"]

    views_params = [
        ('part', 'statistics'),
        ('id', video_id),
        ('key', DEVELOPER_KEY)
    ]
    response = requests.get(list_url + urllib.parse.urlencode(views_params)).json()
    views = response["items"][0]["statistics"]["viewCount"]

    return(views,publish_date)

if __name__ == "__main__":
    compile_data(198,200)

# playlist_id = os.getenv("PLAYLIST_ID")

# channel_id = {
#     "Taylor Swift"
# }

# def create_spotify_playlist():
    # track_csv = csv.reader(open("track_id.csv"))
    # track_ids = []
    # for row in track_csv:
    #     track_ids.append(row[0])
    # currently_reading = track_ids[200:250] #limit of 100 tracks at a time
    # sp.playlist_add_items(playlist_id,currently_reading)

# def youtube_data(video_id):
#     view_request = youtube.videos().list(
#         part="statistics",
#         id=video_id
#     )
#     view_response = view_request.execute()
#     statistics = view_response['items'][0]['statistics']
#     view_count = int(statistics['viewCount'])
#     return(view_count)