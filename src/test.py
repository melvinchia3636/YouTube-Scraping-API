from youtube_scraping_api import YoutubeAPI
from youtube_scraping_api.filter import SearchFilter
api = YoutubeAPI()


for i in api.playlist('PL7VmhWGNRxKgtwHFgDMCnutcmiafoP1c4'):
	print(i)