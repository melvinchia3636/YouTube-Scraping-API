import requests
from youtube_scraping_api.utils import *
from youtube_scraping_api.constants import HEADERS, PAYLOAD
import json

s = requests.Session()
s.headers = HEADERS

raw = requests.get('https://www.youtube.com/watch?v=6uddGul0oAc').text
API_TOKEN = findSnippet(raw, "innertubeApiKey", ",", (3, 1))
payload = PAYLOAD
payload['isInvalidationTimeoutRequest'] = True
data = getInitialData(raw)
continuation = next(searchDict(next(searchDict(data, "liveChatRenderer")), 'continuation'))
payload['continuation'] = continuation
data = s.post('https://www.youtube.com/youtubei/v1/live_chat/get_live_chat?key='+API_TOKEN, json=payload).json()
chats = next(searchDict(data, 'liveChatContinuation'))
continuation = next(searchDict(chats, 'continuation'))
contents = next(searchDict(data, "actions"))
print(next(searchDict(contents[-2], "message")))