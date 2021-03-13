#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from app import app

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
        }
    ]
    return render_template("index.html", title = title, links = links)
