from bottle import Bottle, request, response, run, template, static_file
from app.controllers import google_images
import play
import pyxis
import requests
from subprocess import call
import urllib
import time

app = Bottle()

@app.hook('after_request')
def enable_cors():
	response.headers['Access-Control-Allow-Origin'] = '*'

@app.get('/')
def render_page():
	return template("app/views/pyxis")

# Static rendering
@app.get('<path:path>')
def server_public(path):
	return static_file(path, root = 'public/')

# Controls
@app.get('/images')
def google():
	term = pyxis.see("pixels")
	return google_images.search(term)

@app.get('/youtube')
def youtube():
	term = pyxis.see("pixels")
	# play_youtube(term)
	url = "http://gdata.youtube.com/feeds/api/videos?q=" + str(term) + "&format=5&max-results=1&v=2&alt=jsonc"
	res = requests.get(url)
	res = res.json()
	link = res['data']['items'][0]['player']['default']

	call(["google-chrome", str(link)])

@app.get('/play')
def play():
	term = pyxis.see("pixels")

	search_url = "https://muzi.sdslabs.co.in/ajax/search/?search=" + str(term)
	res = requests.get(url)
	res = res.json()

	# muzi_id = res['tracks'][0]['id']
	# print muzi_id
	# # Id found

	# res = requests.get("https://sdslabs.co.in/muzi/ajax/track/?id=" + str(muzi_id))
	# res = res.json()
	# file_name = res['file']
	# file_url = "https://music.sdslabs.co.in/" + str(urllib.quote(file_name))
	# params = {'url': file_url, 'id': muzi_id}
	# res = requests.post("https://play.sdslabs.co.in/play", data = params)
	artist_id = res['artists'][0]['id']
	track_url = "https://sdslabs.co.in/muzi/ajax/band/?id=" + str(artist_id)
	res = requests.get()
	res = res.json()
	for x in range(10):
		file_name = res[x]['file']
		track_id = res[x]['id']
		file_url = "https://music.sdslabs.co.in/" + str(urllib.quote(file_name))
		params = {'url': file_url, 'id': track_id}
		resp = requests.post("https://play.sdslabs.co.in/play", data = params)
		time.sleep(3)


@app.get('/news')
def news():
	term = pyxis.see("pixels")
	url = "https://news.google.com/news/search?q=" + str(term)
	call(["google-chrome", url])

app.run(host = "0.0.0.0", port = 1111)