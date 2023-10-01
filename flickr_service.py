# flickr_service.py

import requests
import json

FLICKR_ENDPOINT = "https://api.flickr.com/services/rest/"  # replace with the actual endpoint

def parse_flickr_response(response):
    parsed_images = []
    for photo in response['photos']['photo']:
        url = f"https://farm{photo['farm']}.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg"
        title = photo['title']
        parsed_images.append({"url": url, "title": title})
    return parsed_images

def fetch_images(api_key, search_query, num_images=10):
    payload = {
        'method': 'flickr.photos.search',
        'api_key': api_key,
        'text': search_query,
        'format': 'json',
        'nojsoncallback': 1,
        'per_page': num_images,
    }

    response = requests.get(FLICKR_ENDPOINT, params=payload)
    return parse_flickr_response(response.json())
 