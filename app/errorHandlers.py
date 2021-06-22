#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import make_response, render_template
from app import app, ENV

@app.errorhandler(404)
def not_found(error):
    error = "404 Not found"
    return make_response(
        render_template("error.html", title = ENV["sitename"], error = error), 
        404
    )

@app.errorhandler(400)
def bad_request(error):
    error = "400 Bad Request"
    return make_response(
        render_template("error.html", title = ENV["sitename"], error = error), 
        400
    )


@app.errorhandler(500)
def server_error(error):
    error = "500 Internal server error"
    return make_response(
        render_template("error.html", title = ENV["sitename"], error = error), 
        500
    )



