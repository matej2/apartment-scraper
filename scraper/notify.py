import json
import os

import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

from config.models import Webhook


def send_discord_wh(listing, ap):
    wh_list = Webhook.objects.all()

    for wh in wh_list:
        webhook = DiscordWebhook(url=wh.url, rate_limit_retry=True)
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