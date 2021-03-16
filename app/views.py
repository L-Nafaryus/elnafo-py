#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, send_file
from app import app
import os
from git import Repo
import pypandoc

###############################################################################
#   Error handlers
#
@app.errorhandler(404)
def not_found_error(error):
    title = "404 Not found:c"
    return render_template("404.html", title = title), 404


###############################################################################
#   Root route
#
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


###############################################################################
#   Git
#
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
    remotes = list(repo.remotes.origin.urls)

    summary = {
        "desc": repo.description,
        "owner": firstcommit.author,
        "lastchange": str(lastcommit.authored_datetime),
        "remotes": "<br>".join(remotes)
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


###############################################################################
#   Audio
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
                tracks.append({
                    "url": os.path.join("/audio", artist, album, trackpath),
                    "name": trackpath
                })

        tracks = sorted(tracks, key = lambda item: item["name"])

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
