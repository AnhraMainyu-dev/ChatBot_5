import requests


def fetch_singular_item(content_type, document_id, api_token):
    url = f"http://localhost:1337/api/{content_type}/{document_id}"
    headers = {"Authorization": "Bearer " + api_token}
    response = requests.get(url, headers=headers, params={"populate": "*"})
    response.raise_for_status()
    return response.json()["data"]


def fetch_content_type(content_type, api_token):
    url = f"http://localhost:1337/api/{content_type}"
    headers = {"Authorization": "Bearer " + api_token}
    response = requests.get(url, headers=headers, params={"populate": "*"})
    response.raise_for_status()
    return response.json()["data"]


def fetch_picture(item):
    response = requests.get(f"http://localhost:1337{item['Picture']['url']}")
    response.raise_for_status()
    return response.content


def fetch_cart_id(tg_id, api_token):
    url = "http://localhost:1337/api/carts"
    headers = {"Authorization": "Bearer " + api_token}
    response = requests.get(
        url,
        headers=headers,
        params={
            "filters[tg_id][$eq]": tg_id,
            "filters[client][$null]": "true",
            "populate": "*",
        },
    )
    response.raise_for_status()
    carts = response.json()["data"]
    if not carts:
        return None
    return carts[0]["documentId"]


def create_cart(tg_id, api_token):
    url = "http://localhost:1337/api/carts"
    headers = {"Authorization": "Bearer " + api_token}
    payload = {
        "data": {
            "tg_id": tg_id,
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["data"]["documentId"]


def add_to_cart(tg_id, cart_id, item_id, api_token):
    url = "http://localhost:1337/api/fish-items"
    headers = {"Authorization": "Bearer " + api_token}
    payload = {
        "data": {
            "ryba": item_id,
            "cart": cart_id,
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()


def delete_from_cart(cart_item_id, api_token):
    url = f"http://localhost:1337/api/fish-items/{cart_item_id}"
    headers = {"Authorization": "Bearer " + api_token}
    response = requests.delete(url, headers=headers)
    response.raise_for_status()


def fetch_cart(cart_id, api_token):
    url = f"http://localhost:1337/api/carts/{cart_id}"
    headers = {"Authorization": "Bearer " + api_token}
    response = requests.get(
        url, headers=headers, params={"populate[fish_items][populate]": "*"}
    )
    response.raise_for_status()

    return response.json()["data"]["fish_items"]


def send_order(email, tg_name, cart_id, api_token):
    url = "http://localhost:1337/api/clients"
    headers = {
        "Authorization": "Bearer " + api_token,
        "Content-Type": "application/json",
    }
    payload = {
        "data": {
            "Email": email,
            "Name": tg_name,
            "cart": {
                "documentId": cart_id,
            },
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
