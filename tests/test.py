from youtube_scraping_api import YoutubeAPI
api = YoutubeAPI()
for i in api.search('python'):
	print(i)