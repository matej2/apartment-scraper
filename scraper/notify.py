import requests
from discord_webhook import DiscordWebhook, DiscordEmbed



def process_messages(listing, ap):
    webhook_list = listing.webhook.all()
    for wh in webhook_list:
        send_discord_wh(listing.url, ap, wh.url)

def send_discord_wh(listing_url, ap, wh_url):

    webhook = DiscordWebhook(url=wh_url, rate_limit_retry=True)
    embed = DiscordEmbed(description=ap.subtitle, color='03b2f8')

    embed.set_author(name=ap.title, url=ap.url)
    embed.add_embed_field(name='Description', value=ap.description, inline=False)
    embed.add_embed_field(name='Rent', value=ap.rent)
    embed.add_embed_field(name='Contact', value=ap.contact)
    embed.add_embed_field(name='Listing', value=listing_url)

    # add embed object to webhook
    webhook.add_embed(embed)

    photos = ap.photo_set.all()
    i = 1
    while i < 10 and i < len(photos):
        p = photos[i]
        thumb = DiscordEmbed(color='03b2f8')
        thumb.set_image(url=str(p.url))
        webhook.add_embed(thumb)
        i = i + 1

    response = webhook.execute()
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)