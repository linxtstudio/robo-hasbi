import json
import requests
import os
import time
import re
from threading import Thread

# USAGE:
# Set Environment Variables:
# Set IG_USERNAME to username account you want to monitor. Example - ladygaga
# Set WEBHOOK_URL to Discord account webhook url. To know how, just Google: "how to create webhook discord".
# Set TIME_INTERVAL to the time in seconds in between each check for a new post. Example - 1.5, 600 (default=600)
# Help: https://www.serverlab.ca/tutorials/linux/administration-linux/how-to-set-environment-variables-in-linux/

INSTAGRAM_USERNAME = ['itkarir', 'lowonganit.jkt', 'loker_it', 'lokeritindonesia', 'lokerprogrammerid', 'parttimeindonesia', 'indonesia_freelancer', 'magangbandung']

# ----------------------- Do not modify under this line ----------------------- #
def get_hashtag_json(ig_user):
    hashtag_json = json.loads(get_instagram_html(ig_user).text.split('<script')[4].split('window._sharedData = ')[1].split(';</script>')[0])['entry_data']['TagPage'][0]['graphql']['hashtag']
    return hashtag_json['edge_hashtag_to_media']['edges'][0]['node']

def get_hashtag_caption(_json):
    return _json['edge_media_to_caption']['edges'][0]['node']['text']

def get_hashtag_thumbnail_src(_json):
    return _json['thumbnail_src']

def get_hashtag_shortcode(_json):
    return _json['shortcode']

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
    raw_text = html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
    filtered_text = re.sub(r"#(\w+)", "", raw_text, flags=re.IGNORECASE)
    formatted_text = filtered_text.replace("  ?", "?").replace("  ,", ",")
    return formatted_text


def webhook(webhook_url, html, INSTAGRAM_USERNAME):
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data = {}
    data["embeds"] = []
    embed = {}
    embed["color"] = 15467852
    embed["author"] = {
        "name": "Halo guys, ada lowongan baru nih dari @"+INSTAGRAM_USERNAME+"",
        "url": "https://www.instagram.com/p/"+get_last_publication_url(html)+"/",
        "icon_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/1024px-Instagram_icon.png"
    }
    embed["description"] = get_description_photo(html)
    embed["image"] = {"url":get_last_thumb_url(html)}
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discord, code {}.".format(result.status_code))

def hashtag_webhook(webhook_url, html, INSTAGRAM_USERNAME):
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data = {}
    data["embeds"] = []
    embed = {}
    embed["color"] = 15467852
    embed["title"] = "Halo guys, ada lowongan baru nih dari @"+INSTAGRAM_USERNAME+""
    embed["url"] = "https://www.instagram.com/p/" + \
        get_hashtag_shortcode(html)+"/"
    embed["description"] = get_hashtag_caption(html)
    embed["image"] = {"url":get_hashtag_thumbnail_src(html)}
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
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
    html = requests.get("https://www.instagram.com/" + INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html


def main(ig_user, is_first_run):
    try:
        html = get_instagram_html(ig_user)
        if os.environ.get(f"LAST_IMAGE_ID_{ig_user}") != get_last_publication_url(html):
            os.environ[f"LAST_IMAGE_ID_{ig_user}"] = get_last_publication_url(html)
            print("New image to post in discord.")
            if not is_first_run:
              webhook('https://discord.com/api/webhooks/845531517857169419/iS1F5dkGBZtXNWvMW3FmgQjUoG7mwed0sdFAzS0JeMU1FvftVDrhK2JUYNI30sGSv91v', html, ig_user)
    except Exception as e:
        print(e)


def cari_loker():
    is_first_run = True
    if INSTAGRAM_USERNAME and 'https://discord.com/api/webhooks/845531517857169419/iS1F5dkGBZtXNWvMW3FmgQjUoG7mwed0sdFAzS0JeMU1FvftVDrhK2JUYNI30sGSv91v' != None:
        while True:
            for ig_user in INSTAGRAM_USERNAME:
                Thread(target=main, args=(ig_user, is_first_run)).start()
            is_first_run = False
            time.sleep(float(1200)) # 1200 = 20 minutes
    else:
        print('Please configure environment variables properly!')
