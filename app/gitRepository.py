#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, abort
from app import app, ENV 
import os, time
from git import Repo
import subprocess
import json
import pypandoc
from app.utils import timeAgo, rst2html 

@app.route("/git")
def git():
    gitdir = os.path.join(ENV["public"], "git")
    projectsdirs = os.listdir(gitdir)
    projects = []

    for pd in projectsdirs:
        if not os.path.exists(os.path.join(gitdir, pd, ".git")):
            continue

        repo = Repo(os.path.join(gitdir, pd))
        name = pd
        description = repo.description
        lastchanged = timeAgo(repo.head.commit.committed_date)

        projects.append({
            "url": "git/{}".format(name),
            "name": name,
            "description": description,
            "lastchanged": lastchanged
        })

    return render_template("projects.html", title = ENV["sitename"], subtitle = "Git", projects = projects)

# TODO: branch changing
@app.route("/git/<repository>")
@app.route("/git/<repository>/<branch>/tree")
@app.route("/git/<repository>/<branch>/blob/<path:blob>")
@app.route("/git/<repository>/<branch>/tree/<path:tree>")
def git_repository(repository, branch = "master", blob = None, tree = None):
    repopath = os.path.join(ENV["public"], "git", repository)

    if not os.path.exists(repopath):
        abort(404)

    repo = Repo(repopath)
    curbranch = repo.heads[branch]
    firstcommit = list(repo.iter_commits(curbranch))[-1]
    lastcommit = list(repo.iter_commits(curbranch))[0]
    entries = list(lastcommit.tree.traverse())

    if repo.remotes:
        remotes = list(repo.remotes.origin.urls)
    else:
        remotes = []

    branches = [ branch.name for branch in repo.branches ]

    #cloc = subprocess.Popen("cloc --git --json {}/".format(repopath), shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #out, err = cloc.communicate()
    #print(err)
    #data = json.loads(str(out, "utf-8"))
    #langs = []

    #for key in data:
    #    if not (key == "header" or key == "SUM"):
    #        langs.append({
    #            "name": key,
    #            "code": data[key]["code"]
    #        })

    #langs = sorted(langs, key = lambda item: item["code"])
    #langs.reverse()
    #languages = []
    #sum = 0

    #for lang in langs:
    #    sum += lang["code"]

    #for lang in langs:
    #    lang["percent"] = round(lang["code"] / sum * 100, 1)

    #for lang in langs: 
    #        languages.append("{} {}%".format(lang["name"], lang["percent"]))
 
    for n, branch in enumerate(branches):
        if branch == "master":
            branch_url = os.path.join("/git", repository)
 
        else:
            branch_url = os.path.join("/git", repository, branch, "tree")

        branches[n] = f'<a href="{ branch_url }">{ branch }</a>'
  
    summary = {
        "desc": repo.description,
        "owner": firstcommit.author,
        "lastchanged": lastcommit.authored_datetime,
        "remotes": " \\ ".join(remotes),
        "branches": " \\ ".join(branches),
        "languages": "-" #"<br>".join(languages)
    }

    files = []
    readme = None
    blobcontent = None
    root = repository

    if blob:
        for entry in entries:
            if entry.type == "blob" and entry.path == blob:
                blobcontent = repo.git.show("{}:{}".format(lastcommit.hexsha, entry.path))
                root = f"{ repository }/{ entry.path }"

    elif tree:
        for entry in entries:
            if entry.path == os.path.join(tree, entry.name):
                if entry.type == "blob":
                    url = os.path.join("/git", repository, branch, "blob", entry.path)

                elif entry.type == "tree":
                    url = os.path.join("/git", repository, branch, "tree", entry.path)

                entrycommit = next(repo.iter_commits(paths = entry.path))
                message = entrycommit.summary
                date = timeAgo(entrycommit.committed_date)
                
                files.append({
                    "url": url,
                    "name": entry.name,
                    "type": entry.type,
                    "commit": message,
                    "lastchanged": date
                })
                root = f"{ repository }/{ tree }"

    else:
        for entry in entries:
            if entry.name == entry.path:
                if entry.type == "blob":
                    url = os.path.join("/git", repository, branch, "blob", entry.path)

                    if entry.name == "README.md":
                        readmemd = repo.git.show("{}:{}".format(lastcommit.hexsha, entry.path))
                        readme = pypandoc.convert(readmemd, to = "html", format = "md")

                    elif entry.name == "README.rst":
                        readmerst = repo.git.show("{}:{}".format(lastcommit.hexsha, entry.path))
                        readme = rst2html(readmerst)


                elif entry.type == "tree":
                    url = os.path.join("/git", repository, branch, "tree", entry.path)

                entrycommit = next(repo.iter_commits(paths = entry.path))
                message = entrycommit.summary
                date = timeAgo(entrycommit.committed_date)
                 
                files.append({
                    "url": url,
                    "name": entry.name,
                    "type": entry.type,
                    "commit": message,
                    "lastchanged": date
                })

    files = sorted(files, key = lambda item: item["type"], reverse = True)

    backroot = "/".join(root.split("/")[1:-1])
    url = os.path.join("/git", repository)

    if not branch == "master":
        url = os.path.join(url, branch, "tree")
      
    if backroot:
        url = os.path.join("/git", repository, branch, "tree", "/".join(root.split("/")[1:-1]))
     
    if not root == repository:
        files.insert(0, {
            "url": url,
            "name": "..",
            "type": "tree"
        })

    return render_template("repository.html",
        title = ENV["sitename"], subtitle = "Git", 
        root = root, summary = summary,
        blob = blobcontent, files = files, readme = readme)


