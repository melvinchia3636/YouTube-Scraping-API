from youtube_scraping_api import YoutubeAPI
api = YoutubeAPI()
print(api.search('mumbo jumbo')[0].raw)