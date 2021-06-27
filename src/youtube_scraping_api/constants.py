PAYLOAD = {
    "context": {
        "client": {
            "clientName": "WEB",
            "clientVersion": "2.20201220.08.00",
        },
        "user": {
            "lockedSafetyMode": False,
        }
    },
    "webClientInfo": {
        "isDocumentHidden": True
    }
}

HEADERS = {
    "x-youtube-client-name": "1",
    "x-youtube-client-version": "2.20210407.08.00",
    "accept-language": "en-US"
}

THUMBNAIL_TEMPLATE = {
    "default": "https://i.ytimg.com/vi/{}/default.jpg",
    "medium": "https://i.ytimg.com/vi/{}/mqdefault.jpg",
    "high": "https://i.ytimg.com/vi/{}/hqdefault.jpg",
    "standard": "https://i.ytimg.com/vi/{}/sddefault.jpg",
    "maxres": "https://i.ytimg.com/vi/{}/maxresdefault.jpg"
}
