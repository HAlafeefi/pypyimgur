
def post_img(image, client_id, status_check=False):
    imgur_api = "https://api.imgur.com/3/upload"
    payload = [('image', open(image, 'rb'))]
    headers = {
        'Authorization': f'Client-ID {client_id}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Host': 'api.imgur.com',
        'Origin': 'https://imgur.com'
    }
    response = requests.post(imgur_api, headers=headers, files=payload)
    return response.json()["data"]["link"]

def get_imgurjs():
    imgur_res = requests.get("https://imgur.com").text
    soup = BeautifulSoup(imgur_res, 'html.parser')
    script_tag_with_defer = soup.find('script', defer=True)

    if script_tag_with_defer:
        src_value = script_tag_with_defer.get('src')
        return src_value
    else:
        raise Exception("No script tag with 'defer' attribute found.")

imgurjs = "https://s.imgur.com/desktop-assets/js/main.824d64772ba6d6700b3f.js"


def get_clientid():
    kkk = open("kkk.txt", "r").read()
    pattern = r'apiClientId:"([^"]+)"'

    match = re.search(pattern, kkk)
    if match:
        api_client_id = match.group(1)
        return api_client_id
    else:
        raise Exception("apiClientId not found.")

client = "546c25a59c58ad7"

def post_media(media, client_id, status_check=True):
    """
    maxFileSize:     20  MB\n
    maxAnimatedSize: 200 MB\n
    maxVideoDuration: 60 S\n
    There is an upload limit of 50 images per hour and 1250 in a day.\n
    """
    #TODO Add how many left in a day
    imgur_api = "https://api.imgur.com/3/upload?client_id={client_id}".format(client_id=client_id)

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