import requests
from config import *
from time import sleep
from random import choice

session = requests.Session()
session.cookies[".ROBLOSECURITY"] = roblosecurity


def rbx_request(method, url, **kwargs):
    request = session.request(method, url, **kwargs)
    method = method.lower()
    if method in ["post", "put", "patch", "delete"]:
        if "X-CSRF-TOKEN" in request.headers:
            session.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
            x_csrf_token = session.headers["X-CSRF-TOKEN"]
            if request.status_code == 403:
                request = session.request(method, url, **kwargs)
    return request

item_number = 0
items_max_number = len(itemIDs) - 1
while True:
    if mode == 'inorder':
        itemID = str(itemIDs[item_number])
    elif mode == 'random':
        itemID = str(choice(itemIDs))

    url = f"https://avatar.roblox.com/v1/avatar/assets/{itemID}/wear"

    req = rbx_request("POST", url)

    if req.status_code == 200:
        status = f"✅ set item {itemID} successfully"
    else:
        status = f"❌ error {str(req.status_code)}"

    print(status)
    print(f"⏳ cooldown {str(cooldown)} sec")

    if item_number < items_max_number:
        item_number += 1
    else:
        item_number = 0

    sleep(cooldown)