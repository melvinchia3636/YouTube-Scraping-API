from youtube_scraping_api import YoutubeAPI
api = YoutubeAPI()


api.search('hermitcraft')[0].download()