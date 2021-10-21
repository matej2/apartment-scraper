import json
import os

import requests

DEV_PIC = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/No_picture_available.png/160px-No_picture_available.png'

def get_message(listing, ap):
    return f"""
    New post: [{ap.title}]({ap.url}) in listing [{listing.url}]({listing.url})
    Rent: {ap.rent}
    Contact: {ap.contact}
    Description: 

    {ap.description}
    ---
    """

def notify(listing, ap):
    headers = {'Content-Type': 'application/json'}
    data = {}
    data["content"] = get_message(listing, ap)
    #data["username"] = "Apartment Scraper bot"

    # leave this out if you dont want an embed
    data["embeds"] = []
    embed = {
        "image": {
            "url": str(DEV_PIC)
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