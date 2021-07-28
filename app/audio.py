#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, send_file, request
from app import app, ENV
import os
import magic
import mutagen
import datetime
from app.models import database, Items
import logging
from urllib.parse import quote, unquote
from app.files import convertSize, base64

# TODO: slash in names
@app.route("/audio")
@app.route("/audio/<artist>")
@app.route("/audio/<artist>/<album>")
@app.route("/audio/<artist>/<album>/<track>")
def audio(artist = None, album = None, track = None):
    audiopath = os.path.join(ENV["public"], "audio")
    root = "Artists"

    artist = request.args.get("artist")
    album = request.args.get("album")
    track = request.args.get("track")
    
    tracks = []
    albums = []
    artists = []

    db = database.init(os.path.join(ENV["public"], "databases", "audio.db"))

    if track and album and artist:
        query = (Items
            .select(Items.path)
            .distinct(True)
            .where(
                Items.albumartist == artist,
                Items.album == album,
                Items.title == track
            )
        )

        if query.exists():
            for item in query.dicts():
                splitted = str(item["path"], "utf-8").split("/")
                url = os.path.join(audiopath, *splitted[splitted.index("audio") + 1: ]) 
                mimetype = magic.from_file(url, mime = True)

                size = os.stat(url).st_size
                param = {
                    "name": track,
                    "mime": mimetype,
                    "minor": mimetype.split("/")[0],
                    "size": convertSize(size),
                    "url": url 
                }
                 
                if size > 100 * 1024 * 1024:
                    param["content"] = "Too large file"

                else:
                    with open(url, "rb") as io:
                        encoded = base64.b64encode(io.read())
                        raw = str(encoded)[2:-1]
                        param["content"] = f"data:{ mimetype };base64,{ raw }"


                return render_template(
                    "viewer.html", 
                    title = ENV["sitename"], 
                    subtitle = "Audio", 
                    param = param
                )

        return send_file(url, mimetype = mimetype)

    elif album and artist:
        query = (Items
            .select(Items.album, Items.track, Items.title, Items.length, Items.path)
            .distinct(True)
            .where(
                Items.albumartist == artist,
                Items.album == album
            )
            .order_by(Items.track)
        )
 
        if query.exists():
            for item in query.dicts():
                tracks.append(dict(
                    index = item["track"] - 1,
                    url = f"/audio?artist={ artist }&album={ item['album'] }&track={ item['title'] }",
                    name = item["title"],
                    duration = str(datetime.timedelta(seconds = item["length"])).split(".")[0],
                    format = ""
                ))

    elif artist:
        query = (Items
            .select(Items.album, Items.year)
            .distinct(True)
            .where(
                Items.albumartist == artist
            )
            .order_by(Items.year)
        )

        if query.exists():
            for item in query.dicts():
                albums.append(dict(
                    url = f"/audio?artist={ artist }&album={ item['album'] }",
                    name = item["album"],
                    year = item["year"]
                ))

    else:
        query = (Items
            .select(Items.albumartist)
            .distinct(True)
            .order_by(Items.albumartist)
        )
        

        if query.exists():
            for item in query.dicts():
                
                artists.append(dict(
                    url = f"/audio?artist={ item['albumartist'] }",
                    name = item["albumartist"]
                ))


    return render_template("audio.html",
        title = ENV["sitename"], subtitle = "Audio", 
        root = root, artists = artists, albums = albums, tracks = tracks)


