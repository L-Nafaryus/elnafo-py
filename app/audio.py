#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, send_file
from app import app, ENV 
import os
import magic
import mutagen
import datetime

@app.route("/audio")
@app.route("/audio/<artist>")
@app.route("/audio/<artist>/<album>")
@app.route("/audio/<artist>/<album>/<track>")
def audio(artist = None, album = None, track = None):
    audiopath = os.path.join(ENV["public"], "audio")
    root = "Artists"

    tracks = []
    albums = []
    artists = []

    if track:
        url = os.path.join(audiopath, artist, album, track)
        mimetype = magic.from_file(url)

        return send_file(url, mimetype = mimetype)

    elif album:
        tracks_ = os.listdir(os.path.join(audiopath, artist, album))
        root = " - ".join([artist, album])

        for trackpath in tracks_:
            filename, extension = os.path.splitext(trackpath)

            if extension == ".flac":
                audiofile = mutagen.File(os.path.join(audiopath, artist, album, trackpath))
                duration = str(datetime.timedelta(seconds = audiofile.info.length)).split(".")[0]
                fmt = audiofile.mime[0].split("/")[1]
                name = ".".join(" ".join(trackpath.split(" ")[1: ]).split(".")[ :-1])
                
                tracks.append({
                    "index": 0,
                    "url": os.path.join("/audio", artist, album, trackpath),
                    "name": name,
                    "duration": duration,
                    "format": fmt  
                })

        tracks = sorted(tracks, key = lambda item: item["name"])
        index = 0

        for track in tracks:
            track["index"] = index
            index += 1

    elif artist:
        albums_ = os.listdir(os.path.join(audiopath, artist))
        root = artist

        for albumpath in albums_:
            splited = albumpath.split(" ")
            albums.append({
                "url": os.path.join("/audio", artist, albumpath),
                "name": " ".join(splited[1: ]),
                "year": splited[0]
            })

    else:
        artists_ = os.listdir(audiopath)
        root = "Artists"

        for artistpath in artists_:
            artists.append({
                "url": os.path.join("/audio", artistpath),
                "name": artistpath
            })

    return render_template("audio.html",
        title = ENV["sitename"], subtitle = "Audio", 
        root = root, artists = artists, albums = albums, tracks = tracks)


