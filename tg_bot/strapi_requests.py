import requests
from pprint import pprint
from decouple import config

API_TOKEN = config('STRAPI_API')
TG_API_TOKEN = config('TG_API_KEY')

def fetch_singular_item(content_type, item_id, api_token):
    url = f'http://localhost:1337/api/{content_type}'
    headers = {'Authorization': 'Bearer ' + api_token}
    response = requests.get(url, headers=headers, params={'filters[id][$eq]': item_id})
    response.raise_for_status()
    pprint(response.json()['data'])
    return response.json()['data']

def fetch_content_type(content_type, api_token):
    url = f'http://localhost:1337/api/{content_type}'
    headers = {'Authorization': 'Bearer ' + api_token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']

def add_to_cart(item_id, api_token):
    print('Adding to cart')

def delete_from_cart(item_id, api_token):
    print('Deleting from cart')

def fetch_cart(user_id, api_token):
    url = f'http://localhost:1337/api/{user_id}'

def main():
    pprint(fetch_content_type('lososes', API_TOKEN))


if __name__ == '__main__':
    main()