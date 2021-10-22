import json
import os

import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

DEV_PIC = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/No_picture_available.png/160px-No_picture_available.png'


def send_wh(listing, ap):
    webhook = DiscordWebhook(url=os.getenv('DISCORD_WH'), rate_limit_retry=True)
    embed = DiscordEmbed(description=ap.subtitle, color='03b2f8')

    embed.set_author(name=ap.title, url=ap.url)
    embed.add_embed_field(name='Description', value=ap.description, inline=False)
    embed.add_embed_field(name='Rent', value=ap.rent)
    embed.add_embed_field(name='Contact', value=ap.contact)
    embed.add_embed_field(name='Listing', value=listing.url)

    # add embed object to webhook
    webhook.add_embed(embed)

    photos = ap.photo_set.all()
    i = 1
    while i < 10 and i < len(photos):
        p = photos[i]
        thumb = DiscordEmbed(color='03b2f8')
        thumb.set_thumbnail(url=str(p.url))
        webhook.add_embed(thumb)
        i = i + 1

    response = webhook.execute()
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return False


def notify(listing, ap):
    headers = {'Content-Type': 'application/json'}
    data = {}
    data["content"] = get_message(listing, ap)
    #data["username"] = "Apartment Scraper bot"

    # leave this out if you dont want an embed
    data["embeds"] = []

    photos = ap.photo_set.all()
    for p in photos:
        embed = {
            "image": {
                "url": str(p.url)
            }
        }
        # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
        data["embeds"].append(embed)

    if "DISCORD_WH" in os.environ:
        result = requests.post(os.getenv('DISCORD_WH'), data=json.dumps(data), headers=headers)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            return False
    else:
        print('DISCORD_WH missing, skipping')
    return True