#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from app import app, ENV 
import os
from git import Repo
import subprocess
import json
import pypandoc

@app.route("/git")
def git():
    gitdir = os.path.join(ENV["public"], "git")
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

    return render_template("projects.html", title = ENV["sitename"], subtitle = " > Git", projects = projects)

# TODO: branch changing
@app.route("/git/<repository>")
@app.route("/git/<repository>/<branch>/blob/<path:blob>")
@app.route("/git/<repository>/<branch>/tree/<path:tree>")
def git_repository(repository, branch = "master", blob = None, tree = None):
    repopath = os.path.join(ENV["public"], "git", repository)

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
        title = ENV["sitename"], subtitle = " > Git > {}".format(repository), 
        root = root, summary = summary,
        blob = blobcontent, files = files, readme = readme)


