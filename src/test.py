from youtube_scraping_api import YoutubeAPI
api = YoutubeAPI()
video = api.video('WzxSiEWK3cg')
print(video.download_data)