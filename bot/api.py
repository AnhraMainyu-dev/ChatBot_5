import requests
from pprint import pprint
from decouple import config

API_TOKEN = config('TG_API_KEY')
TG_API_TOKEN = config('TG_API_KEY')

def main():
    print('hi')
    url = f'http://localhost:1337/api/lososes'
    headers = {'Authorization': 'Bearer ' + API_TOKEN}
    print(url)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    pprint(response.json())


if __name__ == '__main__':
    main()