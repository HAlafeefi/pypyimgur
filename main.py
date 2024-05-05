import requests
from bs4 import BeautifulSoup
import re
import magic
import os




def check_status(_id, client_id):
    imgur_api = "https://api.imgur.com/media/v1/media/{_id}/status?client_id={client_id}".format(_id=_id, client_id=client_id)
    response = requests.get(imgur_api).json()
    state = response["state"]
    progress_percent = response["progress_percent"]
    print(response)

def check_type(file):
    # pip install python-magic-bin==0.4.14
    try:
        mime_type = magic.from_file(file, mime=True).split("/")
    except FileNotFoundError:
        raise
    try:
        # Won't check video length, should be 60 seconds.
        if mime_type[1] == "gif" or mime_type[0] == "video":
            if os.path.getsize(file) >= 201000000:
                raise Exception("Over-Size file; should be 200MB")
        elif mime_type[0] == "image" and mime_type[1] != "gif":
            if os.path.getsize(file) >= 21000000:
                raise Exception("Over-Size file; should be 20MB")
        else:
            raise Exception("Wrong File Type")
    except OSError:
        raise


    return mime_type[0]

def post_media(media, status_check=True):
    """
    maxFileSize:     20  MB\n
    maxAnimatedSize: 200 MB\n
    maxVideoDuration: 60 S\n
    There is an upload limit of 50 images per hour and 1250 in a day.\n
    """
    #TODO Add how many left in a day
    imgur_api = "https://api.imgur.com/3/upload"

    media_type = check_type(media)
    payload = [(media_type, open(media, 'rb'))]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Host': 'api.imgur.com',
        'Origin': 'https://imgur.com'
    }
    response = requests.post(imgur_api, headers=headers, files=payload)

    data = response.json()["data"]
    if response.status_code != 200:
        raise Exception(data["error"])

    req_id = data["id"]
    vid_link = data["link"]

    if 'processing' in data:
        print(data['processing']['status'])

    print(data)






post_media(r"C:\Users\soos\Downloads\HPw_-DA8ropUd1bQ.mp4", "546c25a59c58ad7")