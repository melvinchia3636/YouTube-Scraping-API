from youtube_scraping_api.urls import *
from youtube_scraping_api.utils import *
from youtube_scraping_api.decorators import *
from youtube_scraping_api.cipher import Cipher
from youtube_scraping_api.constants import HEADERS
from youtube_scraping_api.parser.channel import Channel
from youtube_scraping_api.caption import CaptionQuery, Caption

import os
import time
import requests
from tqdm import tqdm
from urllib.parse import parse_qs
from typing import List, Dict, Any, Optional, Callable, Generator

class Video():
    """Container for video data"""
    def __init__(self, videoId: str, builtin_called: bool = False, **kwargs):
        self._session = requests.Session()
        self._session.headers = HEADERS
        self._has_generated = False

        self._raw = None
        self._player_data = None
        self._init_data = None
        self._primary_info = None
        self._secondary_info = None
        self._player_info = None
        self._is_builtin_called = builtin_called

        self.id = videoId
        self.thumbnails = get_thumbnail(self.id)

        self._static_properties = kwargs

    def __repr__(self):
        return f'<Video id="{self.id}" title="{self.title}" author="{self.author.name}">'

    def parse_data(self) -> None:
        """Fetch HTML source code and extract JSON data from it

        :return: Nothing, data have been set inside local variable
        :rtype: None
        """
        try:
            self._raw = self._session.get(VIDEO_PLAYER_URL+self.id).text
            self._player_data = get_initial_player_response(self._raw)
            self._init_data = get_initial_data(self._raw)
            self._primary_info = next(search_dict(self._init_data, "videoPrimaryInfoRenderer"))
            self._secondary_info = next(search_dict(self._init_data, "videoSecondaryInfoRenderer"))
            self._player_info = self._player_data["videoDetails"]

            self._has_generated = True

        except:
            self._session = requests.Session()
            self._session.headers = HEADERS
            time.sleep(3)
            self.parse_data()

    def get_signature_url(self, url: str) -> str:
        """Get decrypted download link for the video

        :param url: Encrypted download link of the video
        :type url: str
        :return: Usable download link of video
        :rtype: str
        :note: This function isn't developed by me since I have no enough time to dive so deep into Javascript. Credit to PyTube.
        """
        base_url = find_snippet(self._raw, "jsUrl", ",", (3, 1))
        js_url = BASE_URL+base_url
        js_content = self._session.get(js_url).text
        cipher = Cipher(js_content)
        s, sp, url = [i[0] for i in parse_qs(url).values()]
        return url + "&sig=" + cipher.get_signature(s)

    def get_comment_count(self) -> int:
        """Fetch the amount of comments of the video

        :return: Number of comments
        :rtype: int
        """
        continuation = next(search_dict(self._init_data, 'nextContinuationData'))['continuation'].replace('%3D', '=')
        xsrf_token = find_snippet(self._raw, 'XSRF_TOKEN', ",", (3, 1)).replace(r'\u003d', '\u003d')
        params = {
            'action_get_comments': 1,
            'pbj': 1,
            'ctoken': continuation,
            'continuation': continuation,
            'type': 'next'
        }
        data = self._session.post(COMMENT_AJAX_URL, data={'session_token': xsrf_token}, params=params).json()
        comment_count = int(next(search_dict(data, 'countText'))['runs'][0]['text'].replace(',', ''))
        return comment_count

    @custom_property
    def title(self) -> str:
        """Extract video title

        :return: Video title
        :rtype: str
        """
        return "".join(i["text"] for i in self._primary_info["title"]["runs"])

    @custom_property
    def type(self) -> str:
        """Determine type of video

        :return: Video type
        :rtype: str
        """
        return "livestream" if "isLive" in self._primary_info["viewCount"]["videoViewCountRenderer"] and self._primary_info["viewCount"]["videoViewCountRenderer"]["isLive"] else "video"

    @custom_property
    def supertitle(self) -> Optional[List[Dict[str, str]]]:
        """Extract supertitle(custom tags) from video

        :return: List of supertitles of video
        :rtype: list
        """
        if not "superTitleLink" in self._primary_info: return None
        supertitle = [{
            'text': i['text'].strip(),
            'url': next(search_dict(i, 'url'))
        } for i in self._primary_info["superTitleLink"]["runs"] if i['text'].strip()]
        return supertitle

    @custom_property
    def description(self) -> Optional[str]:
        """Extract full description of video

        :return: Description of video
        :rtype: str
        """
        return "".join(i["text"] for i in self._secondary_info["description"]["runs"]) if "description" in self._secondary_info else None

    @custom_property
    def tags(self) -> List[str]:
        """Extract descriptive keywords which content creators can add to thier video to help viewers find their content

        :return: List of all tags of video
        :rtype: list
        """
        return self._player_info["keywords"] if "keywords" in self._player_info else None

    @custom_property
    def publish_time(self) -> str:
        """Extract the time when the video is published

        :return: Time when video is published
        :rtype: str
        :todo: Convert output string to datetime object
        """
        return self._primary_info["dateText"]["simpleText"]

    @custom_property
    def author(self) -> Channel:
        """Extract the content creator who upload the video

        :return: Video author
        :rtype: Channel
        """
        return Channel(
            name = self._player_info["author"],
            url = self._secondary_info["owner"]["videoOwnerRenderer"]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"],
            channel_id = self._player_info["channelId"]
        )

    @custom_property
    def length(self) -> int:
        """Extract the length of the video in second

        :return: Length of video
        :rtype: int
        """
        return int(self._player_info["lengthSeconds"])

    @custom_property
    def view_count(self) -> Optional[int]:
        return self._player_info["viewCount"]

    @custom_property
    def raw(self) -> Dict[str, Any]:
        """Return a dictionary containing all data of video

        :return: Raw data of video
        :rtype: dict
        """
        primary_info = self._primary_info
        player_info = self._player_info
        cleaned_data = {
            "videoId": self.id,
            "type": self.type,
            "title": self.title,
            "supertitle": self.supertitle,
            "description": self.description,
            "tags": self.tags,
            "publish_time": self.publish_time,
            "author": self.author.name,
            "length": self.length,
            "thumbnails": self.thumbnails,
            "statistics": {
                "view_count": int(player_info["viewCount"]),
                **dict(zip(["like_count", "unlike_count"], map(lambda i: int(i.replace(",", "")), primary_info["sentimentBar"]["sentimentBarRenderer"]["tooltip"].split(" / ")))),
                "comment_count": self.get_comment_count()
            }
        }
        return cleaned_data

    @custom_property
    def download_data(self) -> Optional[Dict[int, Dict[str, Any]]]:
        """Parse download links and metadata of the video

        :return: List of dictionary containing download links and metadata
        :rtype: list
        """
        if not self._player_data: self.parse_data()
        try:
            return dict([(i["itag"], {
                "url": i["url"] if "url" in i else None,
                'signature_cipher': i["signatureCipher"] if "signatureCipher" in i else None,
                "mime_type": i["mimeType"],
                "bitrate": i["bitrate"],
                "width": i["width"] if "width" in i else None,
                "height": i["height"] if "height" in i else None,
                "size": i["contentLength"] if "contentLength" in i else None,
                "fps": i["fps"] if "fps" in i else None,
                "quality": i["quality"],
                "quality_label": i["qualityLabel"] if "qualityLabel" in i else None,
                "duration": i["approxDurationMs"] if "approxDurationMs" in i else None
            }) for i in self._player_data["streamingData"]["formats"]+self._player_data["streamingData"]["adaptiveFormats"]]) if self.type!="livestream" else None
        except:
            pass

    def get_file_size(self, url: str) -> int:
        """Get the size of video stream

        :param url: Download link of the video
        :type url: str
        :return: size of video stream in bytes
        :rtype: int
        """
        return int(self._session.get(url, stream=True).headers.get('content-length', 0))

    def stream(self, url, chunk_size: int = 8192, range_size: int = 10000000000) -> Generator:
        """Request and yield chunks of video stream

        :param url: Download link of video stream
        :type url: str
        :param chunk_size: Size of chunk per request
        :type chunk_size: int
        :param range_size: Default size to download, can be overridden
        :type range_size: int, optional
        :return: video stream chunk
        :rtype: bytes
        """
        file_size: int = self.get_file_size(url)

        downloaded = 0
        while downloaded < file_size:
            stop_pos = min(downloaded + range_size, file_size) - 1
            range_header = f"bytes={downloaded}-{stop_pos}"
            response = requests.get(url, headers={"Range": range_header}, stream=True)
            for chunk in response.iter_content(chunk_size):
                if not chunk: break
                downloaded += len(chunk)
                yield chunk
        return

    def download(self, itag: int = None, path: str = ".", log_progress: bool = True, chunk_size: int = 4096, callback_func: Optional[Callable[[Any], None]] = None, name: Optional[str] = None) -> None:
        """Download video from YouTube into local storage

        :param itag: Itag of the video to download, video with best quality will be downloaded if set to None, default set to None
        :type itag: int, optional
        :param path: Relative or absolute path to save the video
        :type path: str, optional
        :param log_progress: Wether to show progress bar of download or not. Default set to True
        :type log_progress: bool, optional
        :param chunk_size: Size of chunk per request. Default set to 4096
        :type chunk_size: int, optional
        :param callback_func: Callback function to be called downloading video. Default set to None
        :type callback_func: Callable, optional
        :param name: Filename of video. Use video title if not set
        :type name: str, optional
        :return: None, just download the video and save it
        :rtype: None
        """
        if not self.download_data:
            return None

        if itag:
            if itag in self.download_data.keys():
                target = self.download_data[itag]
            else:
                raise RuntimeError('Itag does not exist!')
        else:
            target = list(self.download_data.values())[0]

        if target['url'] != None:
            target_url = target['url']
        elif target["signature_cipher"]:
            target_url = self.get_signature_url(target["signature_cipher"])

        vid_name = name if name else convert_valid_filename(self.title)
        extension = target["mime_type"].split(";")[0].split("/")[-1]


        if log_progress:
            print(self.title)
            progress_bar = tqdm(total=self.get_file_size(target_url), unit='iB', unit_scale=True)

        with open(os.path.join(path, f"{vid_name}.{extension}"), "wb") as f:
            for chunk in self.stream(target_url, chunk_size=chunk_size):
                if log_progress: progress_bar.update(len(chunk))
                f.write(chunk)

    @custom_property
    def captions(self) -> CaptionQuery:
        """Give you a list of available captions for the video

        :return: List of available captions
        :rtype: CaptionQuery
        """
        if not self._player_data:
            self.parse_data()

        if not "captions" in self._player_data:
            return None
        raw = self._player_data["captions"]["playerCaptionsTracklistRenderer"]
        default_raw = raw["audioTracks"][0]
        default = default_raw["defaultCaptionTrackIndex"] if "defaultCaptionTrackIndex" in default_raw else 0
        caption_list = raw["captionTracks"]
        result = CaptionQuery((Caption(i["languageCode"], i["name"]["simpleText"], i["baseUrl"], i["isTranslatable"], raw["translationLanguages"]) for i in caption_list), default)

        return result
