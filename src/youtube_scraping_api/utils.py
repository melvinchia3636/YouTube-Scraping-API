import json
import string as strlib
import requests
from bs4 import BeautifulSoup as bs
from youtube_scraping_api.constants import HEADERS, THUMBNAIL_TEMPLATE

def search_dict(partial, key):
    """Recursive search in dictionary

    :param partial: Dictionary to search in
    :type partial: dict
    :param key: Key that you want to search in dictionary
    :type key: str
    :return: Value in dictionary of targeted key
    :rtype: Any
    """
    if isinstance(partial, dict):
        for k, v in partial.items():
            if k == key:
                yield v
            else:
                for o in search_dict(v, key):
                    yield o
    elif isinstance(partial, list):
        for i in partial:
            for o in search_dict(i, key):
                yield o

def find_snippet(text, start, end, skip=(0, 0)):
    """Find snippet in text

    :param text: Text to search in
    :type text: str
    :param start: Where to start grabbing text
    :type start: str
    :param end: Where to stop grabbing text and return
    :type end: str
    :param skip: Number of character to trim in front and behind gragbbed text
    :type skip: tuple
    :return: Snippet found in the text
    :rtype: str
    """
    start_index = text.find(start)
    if start_index == -1:
        return start_index
    end = text.find(end, start_index)
    return text[start_index + len(start) + skip[0]:end - skip[1]]

def parse_continuation_token(data):
    """Extract continuation from raw JSON data

    :param data: Raw JSON data
    :type data: dict
    :return: Continuation token
    :rtype: str
    """
    try: nextCT = next(search_dict(data, "token"))
    except: nextCT = None
    finally: return nextCT

def convert_valid_filename(string):
    """Remove invalid character for saving file from string

    :param string: String to be converted into valid filename
    :type string: str
    :return: String that has invalid character removed
    :rtype: str
    """
    valid_chars = "-_.() %s%s" % (strlib.ascii_letters, strlib.digits)
    return "".join(c for c in string if c in valid_chars)

def get_initial_data(html):
    """Extract primary JSON data from raw HTML source code

    :param html: Raw HTML source code
    :type html: str
    :return: JSON data in form of dictionary
    :rtype: dict
    """
    return json.loads(find_snippet(html, "var ytInitialData = ", "</script>", (0, 1)))

def get_initial_player_response(html):
    """Extract JSON data where video download links are located

    :param html: Raw HTML source code
    :type html: str
    :return: JSON data in form of dictionary
    :rtype: dict
    """
    return json.loads(find_snippet(html, "var ytInitialPlayerResponse = ", ";</script>", (0, 1))+"}", strict=False)

def reveal_redirect_url(url):
    """Get real url from redirect url

    :param url: Redirect url
    :type url: str
    :return: Real url
    :rtype: str
    """
    return bs(requests.get(url, headers=HEADERS).content, "lxml").find("div", {"id": "redirect-action-container"}).find("a")["href"]

def get_thumbnail(videoId):
    """Get url for thumbnails of video

    :param videoId: Youtube ID of the video
    :type videoId: str
    :return: A dictionary of thumbnail urls
    :rtype: dict
    :todo: Check thumbnail urls availability
    """
    return dict(map(lambda i: (i[0], i[1].format(videoId)), THUMBNAIL_TEMPLATE.items()))

def get_proxy():
    proxies = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=4550&country=all&ssl=all&anonymity=all&simplified=true').text.split('\r\n')
    for i in proxies:
        try:
            proxy = {
                'http': 'http://' + i,
                'https': 'http://' + i
            }
            requests.get('https://youtube.com', proxies=proxy, timeout=5)
            return proxy
        except:
            pass
