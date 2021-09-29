#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, make_response, abort, send_file
from app import app, ENV 
import os, time
import magic
import base64
from app.utils import timeAgo, convertSize
  
 
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
        mimetype = magic.from_file(path, mime = True)
        size = os.stat(path).st_size
        param = {
            "name": os.path.basename(path),
            "mime": mimetype,
            "minor": mimetype.split("/")[0],
            "size": convertSize(size),
            "url": os.path.join(root, filepath)
        }
        supported = [
            "image/png",

            "audio/flac",

            "video/webm"
        ]  
         
        if size > 100 * 1024 * 1024:
            param["content"] = "Too large file"

        else:
            if mimetype == "text/plain":
                with open(path, "r") as io:
                    param["content"] = io.read()
       
            elif mimetype in supported:
                with open(path, "rb") as io:
                    encoded = base64.b64encode(io.read())
                    raw = str(encoded)[2:-1]
                    param["content"] = f"data:{ mimetype };base64,{ raw }"

            else:
                param["content"] = "Not supported"

        return render_template(
            "viewer.html", 
            title = ENV["sitename"], 
            subtitle = "Files", 
            param = param
        )

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
                filetype = "directory"

            else:
                filetype = "file"
            
            stat = os.stat(os.path.join(path, filename))
            lastchanged = timeAgo(stat.st_mtime)

            files.append({
                "url": url,
                "name": name,
                "lastchanged": lastchanged,
                "type": filetype
            })

        files = sorted(files, key = lambda item: (item["type"], item["name"]), reverse = False)

        if filepath:
            files.insert(0, {
                "url": "/".join(root.split("/")[ :-1]),
                "name": "..",
                "lastchanged": "",
                "type": "directory"
            })

        return render_template("files.html", title = ENV["sitename"], subtitle = "Files", files = files)


