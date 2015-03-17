import requests

while True:
	query = raw_input("Type 'n' for news, 'p' for play, 'y' for youtube : ")

	if (query == 'n'):
		requests.get("http://localhost:1111/news")
	elif (query == 'p'):
		requests.get("http://localhost:1111/play")
	elif (query == 'y'):
		requests.get("http://localhost:1111/youtube")