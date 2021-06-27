from youtube_scraping_api.constants import HEADERS
from youtube_scraping_api.utils import search_dict, reveal_redirect_url, get_initial_data
from youtube_scraping_api.decorators import custom_property
from youtube_scraping_api.urls import *

import requests
import re

class Channel:
    """Container of channel data"""
    def __init__(self, channel_id=None, username=None, builtin_called=False, **kwargs):
        self._session = requests.Session()
        self._session.headers = HEADERS
        self._has_generated = False

        self.id = channel_id
        self.username = username

        self._about_data = None
        self._metadata = None
        self._header_data = None
        self._is_builtin_called = builtin_called

        self._static_properties = kwargs

    def __repr__(self):
        return f'<Channel id="{self.id}" name="{self.name}">'

    def parse_data(self):
        """Fetch HTML source code and extract JSON data from it

        :return: Nothing, data have been set inside local variable
        :rtype: None
        """
        if not (self.id or self.username): return {}
        if self.id: url = (
            CHANNEL_ID_URL+self.id,
            CHANNEL_ID_URL+self.id+"/about"
        )
        elif self.username: url = (
            CHANNEL_USERNAME_URL+self.username,
            CHANNEL_USERNAME_URL+self.username+"/about"
        )
        response = [self._session.get(i).text for i in url]
        if "404 Not Found" in response[0]:
            self._debug("ERROR", "Channel not exist")
            return
        data, self._about_data = (get_initial_data(i) for i in response)
        self._metadata = data["metadata"]["channelMetadataRenderer"]
        self._header_data = data["header"]

        self._has_generated = True

    @custom_property
    def name(self):
        """Extract name of the channel

        :return: Channel name
        :rtype: str
        """
        return self._metadata["title"]

    @custom_property
    def description(self):
        """Extract description of the channel

        :return: Channel description
        :rtype: str
        """
        return self._metadata["description"]

    @custom_property
    def keywords(self):
        """Extract descriptive keywords which content creators can add to thier channel to help viewers find them

        :return: List of all keywords of the channel
        :rtype: list
        """
        if not 'keywords' in self._metadata: return None
        patterns = [
            r'(?:^|\"\s)([^\"].*?[^\"])(?:\s\"|$)',
            r'\".*?\"'
        ]
        raw_keywords = self._metadata["keywords"]
        keywords_list = sum([re.findall(pattern, raw_keywords) for pattern in patterns], [])
        final = [[eval(keyword)] if re.match(patterns[1], keyword) else keyword.split() for keyword in keywords_list]
        return sum(final, [])

    @custom_property
    def url(self):
        """Return url of the channel

        :return: Channel url
        :rtype: str
        """
        return self._metadata["channelUrl"]

    @custom_property
    def vanity_url(self):
        """Return a human readable custom url created by the channel owner if available

        :return: Custom channel url
        :rtype: str
        """
        return self._metadata["vanityChannelUrl"]

    @custom_property
    def facebook_profile_id(self):
        """Extract facebook profile id of channel owner if available

        :return: Facebook profile id of the channel owner
        :rtype: str or None
        """
        return self._metadata["facebookProfileId"] if "facebookProfileId" in self._metadata else None

    @custom_property
    def avatar(self):
        """Extract avatar thumbnail url of the channel

        :return: Avatar thumbnail url of the channel
        :rtype: str
        """
        return self._metadata["avatar"]["thumbnails"][0]

    @custom_property
    def subscriber_count(self):
        """Extract number of subscriber of the cannel

        :return: Number of subscriber of the channel
        :rtype: int or str or None
        """
        try: subscriber_count = next(search_dict(self._header_data, "subscriberCountText"))["simpleText"].split()[0]
        except: subscriber_count = "No"
        return int(subscriber_count) if subscriber_count.isdigit() else None if subscriber_count == "No" else subscriber_count

    @custom_property
    def banner(self):
        """Return a list of banner urls in different resolutions if available

        :return: A list of banner urls
        :rtype: list or None
        """
        try: return next(search_dict(self._header_data, "banner"))["thumbnails"]
        except: return None

    @custom_property
    def header_links(self):
        """Return a list of social media links that content creator put on their channel header if available

        :return: A list of social media links
        :rtype: list or None
        """
        try:
            raw_header_links = next(search_dict(self._header_data, "channelHeaderLinksRenderer")).values()
            header_links = [{
                "title": i["title"]["simpleText"],
                "icon": i["icon"]["thumbnails"][0]["url"],
                "url": reveal_redirect_url(i["navigationEndpoint"]["urlEndpoint"]["url"])
            } for i in sum(raw_header_links, [])]
            return header_links
        except:
            return None

    @custom_property
    def is_verified(self):
        """Check if the channel is verified by YouTube

        :return: A boolean that states whether the channel is verified
        :rtype: bool
        """
        try:
            if next(search_dict(self._header_data, "badges"))[0]["metadataBadgeRenderer"]["tooltip"] == "Verified":
                return True
            return False
        except: return False

    @custom_property
    def raw(self):
        """Returns all available channel metadata

        :return: A dictionary with metadata values
        :rtype: dict
        """
        return {
            'name': self.name,
            'description': self.description,
            'keywords': self.keywords,
            'url': self.url,
            'vanity_url': self.vanity_url,
            'facebook_profile_id': self.facebook_profile_id,
            'avatar': self.avatar,
            'subscriber_count': self.subscriber_count,
            'header_links': self.header_links,
            'is_verified': self.is_verified
        }
