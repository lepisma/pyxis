import requests
from subprocess import call

def play_youtube(term):
	url = "http://gdata.youtube.com/feeds/api/videos?q=" + str(term) + "&format=5&max-results=1&v=2&alt=jsonc"
	res = requests.get(url)
	res = res.json()
	link = res['data']['items'][0]['player']['default']

	call(["google-chrome", str(link)])