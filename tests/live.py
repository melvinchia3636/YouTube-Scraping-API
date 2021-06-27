import requests
from youtube_scraping_api.utils import *
from youtube_scraping_api.constants import HEADERS, PAYLOAD
from youtube_scraping_api import YoutubeAPI
from datetime import datetime

api = YoutubeAPI()
#print(api.search('')

s = requests.Session()
s.headers = HEADERS

raw = requests.get('https://www.youtube.com/watch?v=qYNvJiJrNR4').text
API_TOKEN = find_snippet(raw, "innertubeApiKey", ",", (3, 1))
payload = PAYLOAD
payload['isInvalidationTimeoutRequest'] = True
data = get_initial_data(raw)
continuation = next(search_dict(next(search_dict(data, "liveChatRenderer")), 'continuation'))
payload['continuation'] = continuation

finished = []

while True:
	data = next(search_dict(s.post('https://www.youtube.com/youtubei/v1/live_chat/get_live_chat?key='+API_TOKEN, json=payload).json(), "liveChatContinuation"))
	continuation = next(search_dict(data, 'continuation'))
	payload['continuation'] = continuation
	try: contents = data["actions"]
	except: continue
	for content in contents:
		try:
			cur_id = next(search_dict(content, "id"))
			if cur_id not in finished:
				message = ''.join(i['text'] for i in next(search_dict(content, "message"))['runs'] if 'text' in i)
				time = next(search_dict(content, "timestampUsec"))
				author = next(search_dict(content, "authorName"))['simpleText']
				print('{:<10} {:<30} {}'.format(datetime.utcfromtimestamp(int(time)/1000000).strftime('%H:%M:%S'), f'<{author}>', message))
				finished.append(cur_id)
		except Exception as e:
			pass
