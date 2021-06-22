#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import ENV
import os
import requests
import twitch
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import toml

_G = os.path.join(ENV["logs"], "global.toml")

if not os.path.exists(_G):
    with open(_G, "w") as io:
        toml.dump({
            "STREAM_STATUS": False
        }, io)

def webhooks_twitch():
    globalVars = toml.load(_G)

    user = "l_nafaryus"
    helix = twitch.Helix(ENV["TWITCH_CLIENT_ID"], ENV["TWITCH_CLIENT_SECRET"])
    u = helix.user(user)

    if u.is_live:
        if not globalVars["STREAM_STATUS"]:
            s = u.stream

            endpoint = "https://elnafo.net/webhooks/discord"
            headers = { "Content-Type": "application/json" }
            data = s.data
            data["profile_image_url"] = u.data["profile_image_url"]

            resp = requests.post(endpoint, headers = headers, data = json.dumps(data))
            #print(resp.content)

            globalVars["STREAM_STATUS"] = True
            #print(f"Twitch webhook: { user } is streaming now")

    else:
        globalVars["STREAM_STATUS"] = False

    with open(_G, "w") as io:
        toml.dump(globalVars, io)

def eventsRun():
    cron = BackgroundScheduler(daemon = True)
    cron.add_job(webhooks_twitch, "interval", seconds = 60)
    cron.start()
    atexit.register(lambda: cron.shutdown(wait=False))

