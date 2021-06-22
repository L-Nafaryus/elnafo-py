#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from app import app, ENV 
import os
from dateutil import parser
import requests

@app.route("/webhooks/discord", methods = ["POST"])
def webhooks_discord():
    data = request.get_json()#["data"][0]

    endpoint = ENV["DISCORD_WEBHOOK"]
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    date = parser.isoparse(data["started_at"])
    body = {
        "content": "New stream was detected!",
        "embeds": [{
            "title": "Stream",
            "url": "https://www.twitch.tv/{}".format(data["user_login"]),
            "description": data["title"],
            "thumbnail": {
                "url": data["profile_image_url"]
            },
            "fields": [
                {
                    "name": "\u200b",
                    "value": "\u200b",
                    "inline": "false"
                },
                {
                    "name": "Human (may be)",
                    "value": data["user_name"],
                    "inline": "true"
                },
                {
                    "name": "Playing",
                    "value": data["game_name"],
                    "inline": "true"
                }
            ],
            "image": {
                "url": data["thumbnail_url"].format(width = 1920, height = 1080)
            },
            "footer": {
                "text": "{} at {}".format(date.date(), date.time())
            }
        }]
    }
    
    resp = requests.post(endpoint, headers = headers, data = json.dumps(body))
    #print(resp.content)
    return str(resp.content)

