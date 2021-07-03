#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from app import app, ENV

@app.route("/srv")
def services():
    srvs = [
        {
            "name": "Transmission",
            "url": "/transmission"
        }
    ]

    return render_template(
        "services.html", 
        title = ENV["sitename"], 
        subtitle = "Services",
        services = srvs
    )
