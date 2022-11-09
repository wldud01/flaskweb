from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import re

video = []
def video_id(res):
    for i in range(0, 5):
        search_result = res.get("items", [])[i]
        print(search_result["id"]["videoId"])
        video.append(search_result["id"]["videoId"])
        print(video)
    return video
