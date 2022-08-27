import json

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

def get_spotify_streams(title):
    