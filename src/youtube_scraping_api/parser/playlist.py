from youtube_scraping_api.utils import search_dict, get_thumbnail
from youtube_scraping_api.parser.video import Video
from youtube_scraping_api.decorators import custom_property

def cleanupData(data, nextCT=None):
    result = []
    for i in data:
        try: typeOfRenderer = list(i.keys())[0]
        except: raise
        if typeOfRenderer == "continuationItemRenderer":
            continue
        each = i[typeOfRenderer]
        eachFinal = RENDERER_PARSER[typeOfRenderer](each)
        result.append(eachFinal)
    if len(result) == 1: return result[0]
    return result

class Playlist(list):
    """A container of playlist metadata and  its videos"""
    def __init__(self, response, builtin_called=False):
        self.first_data = response["metadata"]["playlistMetadataRenderer"]
        self.second_data = next(search_dict(response, "videoOwnerRenderer"))
        self._is_builtin_called = builtin_called
        self._static_properties = []
        self._has_generated = False

        data = cleanupData(next(search_dict(response,"itemSectionRenderer"))["contents"])
        super(Playlist, self).__init__(data)

    def parse_data(self):
        pass

    @custom_property
    def title(self):
        """Exrtract name of the playlist
        
        :return: Playlist name
        :rtype: str
        """
        return self.first_data["title"]

    @custom_property
    def description(self):
        """Extract description of the playlist if available
    
        :return: Playlist description
        :rtype: str of None
        """
        return self.first_data["description"] if "description" in self.first_data else None
    
    @custom_property
    def owner(self):
        """Return the name of playlist creator
    
        :return: Playlist creator name
        :rtype: str
        """
        return self.second_data["title"]["runs"][0]["text"]
    
    @custom_property
    def video_count(self):
        """Count how many videos are in the playlist

        :return: Number of videos in the playlist
        :rtype: int
        """
        video_count, *_ = next(search_dict(self.response, "stats"))
        return int(video_count["runs"][0]["text"].replace(",", ""))
    
    @custom_property
    def view_count(self):
        """Count the total views of all videos in the playlist

        :return: Total views of videos in the playlist
        :rtype: int
        """
        _, total_views, _ = next(search_dict(self.response, "stats"))
        return int(total_views["simpleText"].split()[0].replace(",", ""))
    
    @custom_property
    def last_updated(self):
        """Return the time when the playlist is last updated

        :return: Playlist last updated time
        :rtype: str
        """
        *_, last_updated = next(search_dict(self.response, "stats"))
        last_updated = "".join(i["text"] for i in last_updated["runs"])
        if "Last updated on" in last_updated: last_updated = " ".join(last_updated.split()[3:])
        if "Updated" in last_updated: last_updated = " ".join(last_updated.split()[1:])
        return last_updated

    def __repr__(self):
        return f'<Playlist title="{self.title}" video_count={len(self)}>'

class PlaylistVideo(Video):
    """A container of playlist with the video index in playlist video that function exactly the same as Video Object"""
    def __init__(self, data):
        self.index = int(data["index"]["simpleText"])
        """Index of the video in playlist

        :return: Video index in playlist
        :rtype: int
        """
        super().__init__(
            data["videoId"],
            length = data["lengthText"]["simpleText"] if "lengthText" in data else None,
            thumbnails = get_thumbnail(data["videoId"]),
            builtin_called = True
        )
    
    def __repr__(self):
        return f'<PlaylistVideo index={self.index} id={self.id}>'

    @property
    def raw(self):
        """Return a dictionary containing all data of the playlist video

        :return: Raw data of video
        :rtype: dict
        """
        return {"index": self.index, **super().raw}

RENDERER_PARSER = {
    "playlistVideoListRenderer": lambda data: cleanupData(data["contents"]),
    "playlistVideoRenderer": PlaylistVideo
}