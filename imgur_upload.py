import ast
import base64
import json
import os
import time

import requests

auth_url = "https://api.imgur.com/oauth2/token"
grant_type = "refresh_token"
album_id = "EuuadeF"


def get_imgur_access_token():
    if os.path.exists("imgur_auth_settings.json"):
        with open("imgur_auth_settings.json", "r") as auth_settings_loaded:
            auth_info_dict = ast.literal_eval(auth_settings_loaded.readlines()[0])
            client_id = auth_info_dict["client_id"]
            client_secret = auth_info_dict["client_secret"]
            refresh_token = auth_info_dict["refresh_token"]
    else:
        client_id = "310df355301676d"
        client_secret = "96386fa97b84e00648f988b15bb741dc2222170d"
        refresh_token = "441020c2dd8ff82b415e6d16eb0ad26cca020a24"
    r = requests.post(auth_url,
                      data={"client_id": client_id.replace("\n", ""), "client_secret": client_secret.replace("\n", ""),
                            "refresh_token": refresh_token.replace("\n", ""), "grant_type": grant_type})
    r_json = json.loads(r.text)
    with open("imgur_auth_settings.json", "w") as auth_settings:
        r_dict = {"client_id": client_id, "client_secret": client_secret,
                  "refresh_token": r_json["refresh_token"], "access_token": r_json["access_token"],
                  "account_username": r_json["account_username"], "account_id": r_json["account_id"]}
        access_token = r_json["access_token"]
        auth_settings.write(json.dumps(r_dict, sort_keys=True))
    return access_token


def imgur_upload(image_file_path):
    imgur_access_token = get_imgur_access_token()
    imgur_upload_url = "https://api.imgur.com/3/image"
    headers = {"Authorization": "Bearer {}".format(imgur_access_token)}
    timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(time.time()))
    with open(image_file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        r = requests.post(imgur_upload_url, data={"image": encoded_string, "album": album_id, "title": timestamp,
                                                  "description": timestamp}, headers=headers)
        image_link = json.loads(r.text).get("data").get("link")
        return image_link
