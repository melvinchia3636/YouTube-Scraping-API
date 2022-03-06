from ..utils import get_thumbnail, search_dict
from collections import Counter
from .video import Video
from .channel import Channel
from ..urls import BASE_URL
import requests

def cleanupData(data, nextCT=None, to_object=False):
    result = []
    for i in data:
        try: typeOfRenderer = list(i.keys())[0]
        except: raise
        each = i[typeOfRenderer]
        try: typeOfRenderer = "liveStreamRenderer" if each["badges"][0]["metadataBadgeRenderer"]["label"] == "LIVE NOW" else typeOfRenderer
        except: pass
        try: typeOfRenderer = "premiereRenderer" if each["badges"][0]["metadataBadgeRenderer"]["label"] == "PREMIERING NOW" else typeOfRenderer
        except: pass
        if typeOfRenderer == "continuationItemRenderer":
            continue
        eachFinal = RENDERER_PARSER[typeOfRenderer](each)
        result.append(eachFinal)
    if to_object: return SearchResult(result, nextCT)
    else: return result

class SearchResult(list):
    def __init__(self, data, continuation=None):
        super(SearchResult, self).__init__(data)
        self.continuation_token = continuation
        self.url = None

    def __add__(self, other):
        return SearchResult(list(self)+other)

    def __repr__(self):
        return f'<SearchResult {self.statistic}>'

    @property
    def statistic(self):
            try:
                result = dict(Counter(list(map(lambda i: i.__class__.__name__, self))))
                return result
            except: 
                return None

    @property
    def raw(self):
        return [i.raw for i in self]

class Mix:
    def __init__(self, data):
        self.id = data["playlistId"]
        self.title = data["title"]["simpleText"]
        self.video_count = "".join(i["text"] for i in data["videoCountShortText"]["runs"])
        self.videos = [PlaylistVideo(i["childVideoRenderer"]) for i in data["videos"]]
        self.thumbnail = data["thumbnail"]["thumbnails"]

    def __repr__(self):
        return f'<Mix id="{self.id}" title="{self.title}">'

    @property
    def raw(self):
        return {
            "type": "mix",
            "playlist_id": self.id,
            "title": self.title,
            "videos": [i.raw for i in self.videos],
            "video_count": self.video_count,
            "thumbnails": self.thumbnail
        }

class Shelf:
    def __init__(self, data):
        try: self.title = data["title"]["simpleText"]
        except: self.title = None
        self.videos = cleanupData(next(search_dict(data, "items")))

    def __repr__(self):
        return f'<Shelf title="{self.title}">'

    @property
    def raw(self):
        return {
            "type": "shelf",
            "title": self.title,
            "videos": [i.raw for i in self.videos]
        }

class LiveStream:
    def __init__(self, data):
            self.id = data["videoId"]
            self.title = "".join(i["text"] for i in data["title"]["runs"])
            self.description = "".join(i["text"] for i in data["descriptionSnippet"]["runs"]) if "descriptionSnippet" in data else None
            self.watching_count = int(data["viewCountText"]["runs"][0]["text"].replace(",", "")) if "viewCountText" in data else None
            self.author = Channel(
                name = data["ownerText"]["runs"][0]["text"],
                url = data["ownerText"]["runs"][0]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"],
                channel_id = data["ownerText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"],
            builtin_called = True
            )
            self.thumbnail = get_thumbnail(data["videoId"])

    def __repr__(self):
        return f'<LiveStream id="{self.id}" title="{self.title}">'

    @property
    def raw(self):
        return {
            "type": "live_stream",
            "videoId": self.id,
            "title": self.title,
            "description": self.description,
            "watching_count": self.watching_count,
            "author": self.author.raw,
            "thumbnails": self.thumbnail
        }

class HorizontalCardList:
    def __init__(self, data):
        title = next(search_dict(data["header"], "title"))
        if "simpleText" in title: title = title["simpleText"]
        elif "runs" in title: title = "".join(i["text"] for i in title["runs"])
        else: title = None
        self.title = title
        self.cards = cleanupData(data["cards"])

    def __repr__(self):
        return f'<HorizontalCardList title="{self.title}">'

    @property
    def raw(self):
        return {
            'title': self.title,
            'cards': self.cards
        }

class SearchRefinementCard:
    def __init__(self, data):
        self.query = "".join(i["text"] for i in data["query"]["runs"])
        self.url = next(search_dict(data, "url"))
        self.thumbnail = data["thumbnail"]["thumbnails"]

    def __repr__(self):
        return f'<SearchRefinementCard query="{self.query}">'

    @property
    def raw(self):
        return {
            "type": "search_refinement_card",
            "query": self.query,
            "url": self.url,
            "thumbnails": self.thumbnail
        }

class RichItem:
    def __init__(self, raw):
        pass

class BackgroundPromo:
    def __init__(self, data):
        self.title = "".join(i["text"] for i in data["title"]["runs"])
        self.content = "".join(i["text"] for i in data["bodyText"]["runs"])
    
    def __repr__(self):
        return f'<BackgroundPromo title="{self.title}">'

    @property
    def raw(self):
        return {
            "type": 'background_promo',
            "title": self.title,
            "content": self.content
        }

class Message:
    def __init__(self, data):
        self.text = "".join(i["text"] for i in data["text"]["runs"])
    
    def __repr__(self):
        return f'<Message text="{self.text}">'

    @property
    def raw(self):
        return {
            "type": "message",
            "text": self.text
        }

class SiteLinks:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __repr__(self):
        return f'<SiteLinks title="{self.title}">'

    @property
    def redirected_url(self):
        return (requests.get(self.url).url)

class Advertisement:
    def __init__(self, data):
        self.title = data["title"]["simpleText"]
        self.description = data["descriptionText"]["simpleText"]
        self.website = "".join(i["text"] for i in data["websiteText"]["runs"])
        self.sitelinks = [SiteLinks("".join(i["text"] for i in i["title"]["runs"]), next(search_dict(i, 'url'))) for i in data["sitelinks"]] if 'sitelinks' in data else None

    def __repr__(self):
        return f'<Admertisement title="{self.title}">'

    @property
    def raw(self):
        return {
            "type": 'advertisement',
            "title": self.title,
            "description": self.description,
            "website": self.website
        }

class Playlist:
    def __init__(self, data):
        self.id = data["playlistId"]
        self.title = data["title"]["simpleText"]
        self.video_count = int(data["videoCount"])
        self.videos = [PlaylistVideo(i["childVideoRenderer"]) for i in data["videos"]]

    def __repr__(self):
        return f'<Playlist id="{self.id}" title="{self.title}">'

    @property
    def raw(self):
        return {
            "type": "playlist",
            "id": self.id,
            "title": self.title,
            "video_count": self.video_count,
            "videos": [i.raw for i in self.videos]
        }

class PlaylistVideo:
    def __init__(self, data):
        self.id = data["videoId"]
        self.title = data["title"]["simpleText"]
        self.length = data["lengthText"]["simpleText"]

    def __repr__(self):
        return f'<PlaylistVideo id="{self.id}" title="{self.title}">'

    @property
    def raw(self):
        return {
            "type": "playlist_video",
            "videoId": self.id,
            "title": self.title,
            "length": self.length
        }

class CarouselAd:
    def __init__(self, raw):
        pass

class DidYouMean:
    def __init__(self, data):
        self.query = data["correctedQuery"]["runs"][0]["text"]
        self.url = BASE_URL+next(search_dict(data, "url"))

    def __repr__(self):
        return f'<DidYouMean query="{self.query}">'

    @property
    def raw(self):
        return {
            'query': self.query,
            'url': self.url
        }

class ShowingResultsFor:
    def __init__(self, data):
        self.query = data["correctedQuery"]["runs"][0]["text"]
        self.url = BASE_URL+next(search_dict(data, "url"))
        self.original_query = BASE_URL+next(search_dict(data["originalQueryEndpoint"], "url"))

    def __repr__(self):
        return f'<ShowingResultsFor query="{self.query}">'

    @property
    def raw(self):
        return {
            'query': self.query,
            'url': self.url
        }

RENDERER_PARSER = {
    "videoRenderer": lambda x: Video(
        x["videoId"], 
        title="".join(i["text"] for i in x["title"]["runs"]),
        author=Channel(
            name = x["ownerText"]["runs"][0]["text"],
            url = x["ownerText"]["runs"][0]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"],
            channel_id = x["ownerText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"],
            builtin_called = True
        ),
        builtin_called=True
    ),
    "radioRenderer": Mix,
    "shelfRenderer": Shelf,
    "liveStreamRenderer": lambda x: Video(
        x["videoId"], 
        title="".join(i["text"] for i in x["title"]["runs"]),
        author=Channel(
            name = x["ownerText"]["runs"][0]["text"],
            url = x["ownerText"]["runs"][0]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"],
            channel_id = x["ownerText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"],
            builtin_called = True
        ),
        builtin_called=True
    ),
    "channelRenderer": lambda x: Channel(
        channel_id = x["channelId"],
        url = x["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"],
        name = x["title"]["simpleText"],
        video_count = int(x["videoCountText"]["runs"][0]["text"].split()[0].replace(",", "")) if "videoCountText" in x else None,
        subscriber_count = (int(d) if (d:=x["subscriberCountText"]["simpleText"].split()[0]).isdigit() else d) if "subscriberCountText" in x else None,
        avatar = x["thumbnail"]["thumbnails"],
        builtin_called = True
    ),
    "playlistRenderer": Playlist,
    "horizontalCardListRenderer": HorizontalCardList,
    "searchRefinementCardRenderer": SearchRefinementCard,
    "richItemRenderer": lambda x: cleanupData([x["content"]])[0],
    "backgroundPromoRenderer": BackgroundPromo,
    "messageRenderer": Message,
    "promotedSparklesTextSearchRenderer": lambda x: Advertisement(x['content']),
    "playlistVideoListRenderer": None,
    "playlistVideoRenderer": None,
    "carouselAdRenderer": None,
    "showingResultsForRenderer": lambda x: None,
    "previewCardRenderer": None,
    "searchPyvRenderer": lambda x: cleanupData(x['ads'])[0],
    "promotedVideoRenderer": lambda x: Video(
        x["videoId"], 
        title = x["title"]["simpleText"],
        author = Channel(
            name = x["longBylineText"]["runs"][0]["text"],
            url = x["longBylineText"]["runs"][0]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"],
            channel_id = x["longBylineText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"],
            builtin_called = True
        ),
        builtin_called=True
    ),
    'didYouMeanRenderer': DidYouMean,
    'showingResultsForRenderer': ShowingResultsFor,
    'premiereRenderer': lambda x: None
}