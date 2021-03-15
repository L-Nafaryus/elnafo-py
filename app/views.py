#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from app import app
import os
from git import Repo
import pypandoc

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
        }
    ]

    return render_template("index.html", title = title, links = links)

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

@app.errorhandler(404)
def not_found_error(error):
    title = "404 Not found:c"
    return render_template("404.html", title = title), 404

# TODO: branch changing
@app.route("/git/<repository>")
@app.route("/git/<repository>/<branch>/blob/<path:blob>")
@app.route("/git/<repository>/<branch>/tree/<path:tree>")
def git_repository(repository, branch = "master", blob = None, tree = None):
    title = "ELNAFO > Git > {}".format(repository)
    repopath = os.path.join(os.getcwd(), "app/public/git", repository)
    
    repo = Repo(repopath)
    curbranch = repo.heads[branch]
    lastcommit = list(repo.iter_commits(curbranch))[0]
    entries = list(lastcommit.tree.traverse())
    
    files = []
    readme = None
    blobcontent = None
    # TODO: fix slahes in html
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

    return render_template("repository.html", title = title, root = root, blob = blobcontent, files = files, readme = readme)


#github = os.path.join(os.getcwd(), "app/public/git")
#for d in os.listdir():
#    isgit = True
#
#    try:
#        repo = Repo(d)
#
#    except:
#        isgit = false
#
#    if not isgit:
#        continue
#    
#    git_repo = []
#
#    def git_repo_f():
#        return """Hola"""
#    
#    git_repo.append({ "grf1": git_repo_f })
#    #
#    app.route(git_repo[0]["grf1"], "/git/{}".format(d))
    
