#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from app import app
import os
from git import Repo

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
    title = "elnafo > git"
    gitdir = os.path.join(os.getcwd(), "app/public/git")
    projectsdirs = os.listdir(gitdir)
    projects = []

    for pd in projectsdirs:
        repo = Repo(os.path.join(gitdir, pd))
        name = pd
        description = repo.description
        lastchanged = str(repo.head.commit.authored_datetime)

        projects.append({
            "name": name,
            "description": description,
            "lastchanged": lastchanged
        })

    return render_template("projects.html", projects = projects)

@app.route("git/<project>")
def index(project):
    p = os.path.join(os.getcwd(), "app/public/git", project)
    repo = Repo(p)

    return render_template("repository.html")
