
import re
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

def extract_yt_term(command):
        
	# Regex para pegar frases como "tocar X no youtube" ou "toque X no youtube"
	pattern = r'(?:tocar|toque|reproduzir|play)\s+(.*?)\s+no\s+youtube'
	match = re.search(pattern, command, re.IGNORECASE)
	return match.group(1) if match else ""
    


def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)
    return result_string 


    # autenticação do spotify




## Exemplo: dar play em uma música
# sp.start_playback(uris=["spotify:track:6rqhFgbbKwnb9MLmUQDhG6"])  # Substitua pelo URI da música desejada

