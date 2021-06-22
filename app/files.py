#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, make_response, abort, send_file
from app import app, ENV 
import os, time
import magic

@app.route("/files/")
@app.route("/files/<path:filepath>")
def files(filepath = None):
    root = "/files"
    path = os.path.join(ENV["public"], "files")

    if filepath:
        path += f"/{ filepath }"

    if not os.path.exists(path):
        abort(404)

    if os.path.isfile(path):
        mimetype = magic.from_file(path)

        if mimetype == "text/plain":
            with open(path, "r") as io:
                content = io.read()
        
            return content

        else:
            return send_file(path, mimetype = mimetype, as_attachment = False)

    else:
        ls = os.listdir(path)
        files = []
        url = ""

        if filepath:
            root +=  f"/{ filepath }"
        
        for filename in ls:
            url = f"{ root }/{ filename }"
            name = filename
            
            if os.path.isdir(os.path.join(path, filename)):
                name += " /"
            
            stat = os.stat(os.path.join(path, filename))
            lastchanged = time.ctime(stat.st_mtime)

            files.append({
                "url": url,
                "name": name,
                "lastchanged": lastchanged
            })

        if filepath:
            files.insert(0, {
                "url": "/".join(root.split("/")[ :-1]),
                "name": ".. /",
                "lastchanged": "-"
            })

        return render_template("files.html", title = ENV["sitename"], subtitle = " > Files", files = files)


