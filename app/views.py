#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, send_file, request
from app import app
import os
from git import Repo
import pypandoc
import mutagen
import datetime
import subprocess
import json
from dotenv import dotenv_values
import requests
from dateutil import parser

ENV = dotenv_values(".env")

###
#   Error handlers
##
@app.errorhandler(404)
def not_found_error(error):
    title = "404 Not found:c"
    return render_template("404.html", title = title), 404


###
#   Root route
##
@app.route('/')
@app.route('/index')
def index():
    title = "ELNAFO"
    links = [
        {
            "url": "/doc",
            "desc": "Documentation"
        },
        {
            "url": "/srv",
            "desc": "Services"
        },
        {
            "url": "/files",
            "desc": "Files"
        },
        {
            "url": "/git",
            "desc": "Git"
        },
        {
            "url": "/audio",
            "desc": "Audio"
        }
    ]
    links = sorted(links, key = lambda item: item["desc"])

    return render_template("index.html", title = title, links = links)


###
#   Git
##
@app.route("/git")
def git():
    title = "ELNAFO > Git"
    gitdir = os.path.join(os.getcwd(), "app/public/git")
    projectsdirs = os.listdir(gitdir)
    projects = []

    for pd in projectsdirs:
        repo = Repo(os.path.join(gitdir, pd))
        name = pd
        description = repo.description
        lastchanged = str(repo.head.commit.authored_datetime)

        projects.append({
            "url": "git/{}".format(name),
            "name": name,
            "description": description,
            "lastchanged": lastchanged
        })

    return render_template("projects.html", title = title, projects = projects)

# TODO: branch changing
@app.route("/git/<repository>")
@app.route("/git/<repository>/<branch>/blob/<path:blob>")
@app.route("/git/<repository>/<branch>/tree/<path:tree>")
def git_repository(repository, branch = "master", blob = None, tree = None):
    title = "ELNAFO > Git > {}".format(repository)
    repopath = os.path.join(os.getcwd(), "app/public/git", repository)

    repo = Repo(repopath)
    curbranch = repo.heads[branch]
    firstcommit = list(repo.iter_commits(curbranch))[-1]
    lastcommit = list(repo.iter_commits(curbranch))[0]
    entries = list(lastcommit.tree.traverse())

    if repo.remotes:
        remotes = list(repo.remotes.origin.urls)
    else:
        remotes = []

    cloc = subprocess.Popen("cloc --git --json {}/".format(repopath), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = cloc.communicate()
    print(err)
    data = json.loads(str(out, "utf-8"))
    langs = []

    for key in data:
        if not (key == "header" or key == "SUM"):
            langs.append({
                "name": key,
                "code": data[key]["code"]
            })

    langs = sorted(langs, key = lambda item: item["code"])
    langs.reverse()
    languages = []
    sum = 0

    for lang in langs:
        sum += lang["code"]

    for lang in langs:
        lang["percent"] = round(lang["code"] / sum * 100, 1)

    for lang in langs:
            languages.append("{} {}%".format(lang["name"], lang["percent"]))


    summary = {
        "desc": repo.description,
        "owner": firstcommit.author,
        "lastchange": str(lastcommit.authored_datetime),
        "remotes": "<br>".join(remotes),
        "languages": "<br>".join(languages)
    }

    files = []
    readme = None
    blobcontent = None
    root = "./"

    if blob:
        for entry in entries:
            if entry.type == "blob" and entry.path == blob:
                blobcontent = repo.git.show("{}:{}".format(lastcommit.hexsha, entry.path))
                root = "../{}".format(entry.path)

    elif tree:
        for entry in entries:
            if entry.path == os.path.join(tree, entry.name):
                if entry.type == "blob":
                    url = os.path.join("/git", repository, branch, "blob", entry.path)

                elif entry.type == "tree":
                    url = os.path.join("/git", repository, branch, "tree", entry.path)

                files.append({
                    "url": url,
                    "name": entry.name
                })
                root = "../{}".format(tree)

    else:
        for entry in entries:
            if entry.name == entry.path:
                if entry.type == "blob":
                    url = os.path.join("/git", repository, branch, "blob", entry.path)

                    if entry.name == "README.md":
                        readmemd = repo.git.show("{}:{}".format(lastcommit.hexsha, entry.path))
                        readme = pypandoc.convert(readmemd, to = "html", format = "md")

                elif entry.type == "tree":
                    url = os.path.join("/git", repository, branch, "tree", entry.path)

                files.append({
                    "url": url,
                    "name": entry.name
                })

    return render_template("repository.html",
        title = title, root = root, summary = summary,
        blob = blobcontent, files = files, readme = readme)


###
#   Audio
##
#   Concept: path > artist > album > track.extension
#
@app.route("/audio")
@app.route("/audio/<artist>")
@app.route("/audio/<artist>/<album>")
@app.route("/audio/<artist>/<album>/<track>")
def audio(artist = None, album = None, track = None):
    title = "ELNAFO > Audio"
    audiopath = os.path.join(os.getcwd(), "app/public/audio")
    root = "Artists"

    tracks = []
    albums = []
    artists = []

    if track:
        url = os.path.join(audiopath, artist, album, track)

        return send_file(url)

    elif album:
        tracks_ = os.listdir(os.path.join(audiopath, artist, album))
        root = " - ".join([artist, album])

        for trackpath in tracks_:
            filename, extension = os.path.splitext(trackpath)

            if extension == ".flac":
                audiofile = mutagen.File(os.path.join(audiopath, artist, album, trackpath))
                duration = str(datetime.timedelta(seconds = audiofile.info.length)).split(".")[0]

                tracks.append({
                    "index": 0,
                    "url": os.path.join("/audio", artist, album, trackpath),
                    "name": trackpath,
                    "duration": duration
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
            albums.append({
                "url": os.path.join("/audio", artist, albumpath),
                "name": albumpath
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
        title = title, root = root, artists = artists, albums = albums, tracks = tracks)


###
#   Webhooks
##
import twitch
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

global STREAM_STATUS
STREAM_STATUS = False

def webhooks_twitch():
    user = "l_nafaryus"
    helix = twitch.Helix(ENV["TWITCH_CLIENT_ID"], ENV["TWITCH_CLIENT_SECRET"])
    u = helix.user(user)

    if u.is_live:
        if not STREAM_STATUS:
            s = u.stream

            endpoint = "http://localhost/webhooks/discord"
            headers = { "Content-Type": "application/json" }

            resp = requests.post(endpoint, headers = headers, data = json.dumps(s.data))
            print(resp.content)

            STREAM_STATUS = True
            print(f"Twitch webhook: { user } is streaming now")

    else:
        STREAM_STATUS = False

cron = BackgroundScheduler(daemon = True)
cron.add_job(webhooks_twitch, "interval", seconds = 60)
cron.start()
atexit.register(lambda: cron.shutdown(wait=False))

@app.route("/webhooks/discord", methods = ["POST"])
def webhooks_discord():
    data = request.get_json()#["data"][0]

    endpoint = "https://discord.com/api/webhooks/849319825750884372/6PZkb89iD7zl00k9woZH4c2T0OGyMutssSDXedsrP3qnKRv6hKGlbQ0lXl2kfh72rqV9"
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
                "url": "https://cdn.discordapp.com/avatars/849319825750884372/28bd2006bdcbe79a9858571eab593f10.png"
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
            "footer": {
                "text": "{} at {}".format(date.date(), date.time())
            }
        }]
    }
    
    resp = requests.post(endpoint, headers = headers, data = json.dumps(body))

    return str(resp.content)

###
#   Subscriptions
##
#status, reason = subscribe_twitch("l_nafaryus")
#print(f"Subscription Twitch: { status } : { reason }")

