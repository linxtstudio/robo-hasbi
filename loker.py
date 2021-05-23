# import requests
# import json

# url = "https://instagramdimashirokovv1.p.rapidapi.com/user/loker.programmer"

# headers = {
#     'x-rapidapi-key': "366f407af5msh652298aab9f275dp14efd1jsn963e160017d3",
#     'x-rapidapi-host': "InstagramdimashirokovV1.p.rapidapi.com"
#     }

# response = requests.request("GET", url, headers=headers)

# print(response.json())

import re
import json
import sys
import requests
import urllib.request
import os
import time

# USAGE:
# Set Environment Variables:
# Set IG_USERNAME to username account you want to monitor. Example - ladygaga
# Set WEBHOOK_URL to Discord account webhook url. To know how, just Google: "how to create webhook discord".
# Set TIME_INTERVAL to the time in seconds in between each check for a new post. Example - 1.5, 600 (default=600)
# Help: https://www.serverlab.ca/tutorials/linux/administration-linux/how-to-set-environment-variables-in-linux/

INSTAGRAM_USERNAME = ['loker.programmer', 'lokeritindonesia]

# ----------------------- Do not modify under this line ----------------------- #


def get_user_fullname(html):
    return html.json()["graphql"]["user"]["full_name"]


def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def get_last_publication_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]


def get_last_photo_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]


def get_last_thumb_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]


def get_description_photo(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]


def webhook(webhook_url, html):
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data = {}
    data["embeds"] = []
    embed = {}
    embed["color"] = 15467852
    embed["title"] = "New pic of @"+INSTAGRAM_USERNAME+""
    embed["url"] = "https://www.instagram.com/p/" + \
        get_last_publication_url(html)+"/"
    embed["description"] = get_description_photo(html)
    embed["image"] = {"url":get_last_thumb_url(html)} # unmark to post bigger image
    embed["thumbnail"] = {"url": get_last_thumb_url(html)}
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(
        data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discord, code {}.".format(
            result.status_code))


def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html = requests.get("https://www.instagram.com/" +
                        INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html


def main(ig_user):
    try:
        html = get_instagram_html(ig_user)
        if(os.environ.get(f"LAST_IMAGE_ID_{ig_user}") == get_last_publication_url(html)):
            print("Not new image to post in discord.")
        else:
            os.environ[f"LAST_IMAGE_ID_{ig_user}"] = get_last_publication_url(html)
            print("New image to post in discord.")
            webhook('https://discord.com/api/webhooks/845531517857169419/iS1F5dkGBZtXNWvMW3FmgQjUoG7mwed0sdFAzS0JeMU1FvftVDrhK2JUYNI30sGSv91v',
                    get_instagram_html(ig_user), ig_user)
    except Exception as e:
        print(e)


def cari_loker():
    if INSTAGRAM_USERNAME and 'https://discord.com/api/webhooks/845531517857169419/iS1F5dkGBZtXNWvMW3FmgQjUoG7mwed0sdFAzS0JeMU1FvftVDrhK2JUYNI30sGSv91v' != None:
        while True:
            for ig_user in INSTAGRAM_USERNAME:
                Thread(target=main, args=(ig_user,)).start()
            time.sleep(float(600)) # 600 = 10 minutes
    else:
        print('Please configure environment variables properly!')
