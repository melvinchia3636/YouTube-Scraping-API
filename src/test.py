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
print(api.search("hermitcraft", filter=SearchFilter(upload_date="Today"))[0])

#playlist test
print([i.thumbnail for i in api.playlist("PLU2851hDb3SE6S9YJFY6n1B4t_Qv26f1m")])