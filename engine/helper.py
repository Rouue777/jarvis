import re

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