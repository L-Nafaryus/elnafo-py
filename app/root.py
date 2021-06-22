#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, send_file
from app import app, ENV 
import os

@app.route('/')
@app.route('/index')
def index():
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

    return render_template("index.html", title = ENV["sitename"], links = links)

@app.route("/favicon.ico")
def favicon():
    return send_file(
        os.path.join(ENV["static"], "favicon.ico"), 
        mimetype = "image/x-icon"
    )
