import requests

API_KEY = "fb1b53e3e43875e5dd81ffc2fb71b995"

def recommend_music(mood):
    url = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={mood}&api_key={API_KEY}&format=json"
    response = requests.get(url).json()

    if 'tracks' in response and 'track' in response['tracks']:
        tracks = response['tracks']['track'][:5]
        return [f"{t['name']} by {t['artist']['name']}" for t in tracks]
    
    return ["No tracks found."]
