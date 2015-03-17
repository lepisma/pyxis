from subprocess import call

def show_news(term):
	url = "https://news.google.com/news/search?q=" + str(term)
	call(["google-chrome", url])