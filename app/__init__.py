#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from dotenv import dotenv_values
import os

app = Flask(__name__, static_folder = "static", template_folder = "templates")

ENV = dotenv_values(".env")
ENV["sitename"] = "ELNAFO"
ENV["root"] = os.path.join(os.getcwd(), "app")
ENV["static"] = os.path.join(ENV["root"], "static")
ENV["public"] = os.path.join(ENV["root"], "public")
ENV["logs"] = os.path.join(os.getcwd(), "logs")

from app import (
    errorHandlers,
    root,
    files,
    gitRepository,
    audio,
    webhooks,
    events,
    services
)

import logging

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)

else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    #events.eventsRun()
