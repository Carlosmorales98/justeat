import requests

def fetch_comic(comic_num=None):
    if comic_num:
        url = f"https://xkcd.com/{comic_num}/info.0.json"
    else:
        url = "https://xkcd.com/info.0.json"

    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Error HTTP: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Error in the request: {err}")
    return None