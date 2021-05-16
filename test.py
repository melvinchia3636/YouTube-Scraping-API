import requests
from youtube_scraping_api.utils import *
from youtube_scraping_api.constants import HEADERS, PAYLOAD
from youtube_scraping_api import YoutubeAPI
from datetime import datetime

api = YoutubeAPI()
#print(api.search(''))


s = requests.Session()
s.headers = HEADERS

raw = requests.get('https://www.youtube.com/watch?v=5qap5aO4i9A').text
API_TOKEN = findSnippet(raw, "innertubeApiKey", ",", (3, 1))
payload = PAYLOAD
payload['isInvalidationTimeoutRequest'] = True
data = getInitialData(raw)
continuation = next(searchDict(next(searchDict(data, "liveChatRenderer")), 'continuation'))
payload['continuation'] = continuation

finished = []

while True:
	data = next(searchDict(s.post('https://www.youtube.com/youtubei/v1/live_chat/get_live_chat?key='+API_TOKEN, json=payload).json(), "liveChatContinuation"))
	continuation = next(searchDict(data, 'continuation'))
	payload['continuation'] = continuation
	try: contents = data["actions"]
	except: continue
	for content in contents:
		try:
			cur_id = next(searchDict(content, "id"))
			if cur_id not in finished:
				message = ''.join(i['text'] for i in next(searchDict(content, "message"))['runs'] if 'text' in i)
				time = next(searchDict(content, "timestampUsec"))
				author = next(searchDict(content, "authorName"))['simpleText']
				print('{} <{}> {}'.format(datetime.utcfromtimestamp(int(time)/1000000).strftime('%H:%M:%S'), author, message))
				finished.append(cur_id)
		except Exception as e: 
			pass