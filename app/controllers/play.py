import requests
import urllib

def play_play(term):
	url = "https://muzi.sdslabs.co.in/ajax/search/?search=" + str(term)
	res = requests.get(url)
	res = res.json()
	muzi_id = res['tracks'][0]['id']
	print muzi_id
	# Id found
	music_root = "https://music.sdslabs.co.in/ajax/track/"
	res = requests.get("https://sdslabs.co.in/muzi/ajax/track/?id=" + str(muzi_id))
	res = res.json()
	file_name = res['file']
	file_url = "https://music.sdslabs.co.in/" + str(urllib.quote(file_name))
	params = {'url': file_url, 'id': muzi_id}
	res = requests.post("https://play.sdslabs.co.in/play", data = params)