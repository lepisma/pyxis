import requests
import json
import urllib

IMAGE_SEARCH = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&start=0"

MAX_IMAGES = 6

def search(query):
	query = urllib.quote(query)
	url = IMAGE_SEARCH + "&rsz=" + str(MAX_IMAGES) + "&q=" + query
	res = requests.get(url)
	if res.status_code == 200:
		data = res.json()
		result_urls = [query]
		for result in data['responseData']['results']:
			result_urls.append(result['url'])
		return json.dumps(result_urls)
	else:
		return "Error"