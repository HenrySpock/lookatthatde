# flickr_service.py

# Import necessary libraries:
# - requests for making HTTP calls 
import requests

# The base endpoint URL for Flickr's REST API.
FLICKR_ENDPOINT = "https://api.flickr.com/services/rest/"

def parse_flickr_response(response):
    """
    Parses the response from Flickr's API to extract image URLs and titles.

    :param response: Dictionary containing the response data from Flickr's API.
    :return: List of dictionaries with 'url' and 'title' as keys.
    """
    
    parsed_images = []  # List to store parsed image data
    
    # Loop through each photo in the response
    for photo in response['photos']['photo']:
        # Construct the image URL based on the Flickr's URL pattern
        url = f"https://farm{photo['farm']}.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg"
        title = photo['title']
        parsed_images.append({"url": url, "title": title})
    
    return parsed_images

def fetch_images(api_key, search_query, num_images=10):
    """
    Fetches images from Flickr's API based on a search query.

    :param api_key: Your Flickr API key.
    :param search_query: Text to search for in Flickr's image database.
    :param num_images: Number of images to fetch (default is 10).
    :return: List of dictionaries with 'url' and 'title' as keys.
    """
    
    # Payload (or parameters) for the API request
    payload = {
        'method': 'flickr.photos.search',  # API method for searching photos
        'api_key': api_key,
        'text': search_query,  # Search query
        'format': 'json',  # The response should be in JSON format
        'nojsoncallback': 1,  # Ensure the returned data is pure JSON and not wrapped in a function call
        'per_page': num_images,  # Limit the number of results
    }

    # Make the API request
    response = requests.get(FLICKR_ENDPOINT, params=payload)
    
    # Parse the response and return the list of images
    return parse_flickr_response(response.json())
