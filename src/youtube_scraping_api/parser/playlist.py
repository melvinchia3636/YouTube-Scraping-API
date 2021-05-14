from ..utils import searchDict, getThumbnail
from .video import Video

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

class Metadata:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Playlist(list):
    def __init__(self, response):
        first_data = response["metadata"]["playlistMetadataRenderer"]
        second_data = next(searchDict(response, "videoOwnerRenderer"))
        video_count, total_views, last_updated = next(searchDict(response, "stats"))
        last_updated = "".join(i["text"] for i in last_updated["runs"])
        if "Last updated on" in last_updated: last_updated = " ".join(last_updated.split()[3:])
        if "Updated" in last_updated: last_updated = " ".join(last_updated.split()[1:])

        data = cleanupData(next(searchDict(response,"itemSectionRenderer"))["contents"])
        super(Playlist, self).__init__(data)

        self.title = first_data["title"]
        self.description = first_data["description"] if "description" in first_data else None
        self.owner = second_data["title"]["runs"][0]["text"]
        self.video_count = int(video_count["runs"][0]["text"].replace(",", ""))
        self.view_count = int(total_views["simpleText"].split()[0].replace(",", ""))
        self.last_updated = last_updated

    def __repr__(self):
        return f'<Playlist title="{self.title}" video_count={len(self)}>'

def parsePlaylistContent(data):
    return cleanupData(data["contents"])

class PlaylistVideo(Video):
    def __init__(self, data):
        self.index = int(data["index"]["simpleText"])
        super().__init__(
            data["videoId"],
            length = data["lengthText"]["simpleText"] if "lengthText" in data else None,
            thumbnails = getThumbnail(data["videoId"]),
            builtin_called = True
        )
    
    def __repr__(self):
        return f'<PlaylistVideo index={self.index} id={self.id}>'

    @property
    def raw(self):
        return {
            "index": self.index
        } | super().raw

RENDERER_PARSER = {
    "playlistVideoListRenderer": parsePlaylistContent,
    "playlistVideoRenderer": PlaylistVideo
}