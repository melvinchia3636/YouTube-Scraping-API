from youtube_scraping_api import YoutubeAPI
from youtube_scraping_api.filter import SearchFilter
api = YoutubeAPI()

#search test
print(api.search('mumbo jumbo'))
print(api.search('believer'))

#search filter test
filters = SearchFilter.get_all_filters()
print(filters.duration)
print(filters.features)
print(filters.sort_by)
print(filters.type)
print(filters.upload_date)

print(api.search("space", filter=SearchFilter(features=["360°"]))[0])