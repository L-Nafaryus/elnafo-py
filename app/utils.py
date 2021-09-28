# -*- coding: utf-8 -*-

import docutils.core
import time

def rst2html(rsText: str) -> str:
    html = None

    try:
        html = docutils.core.publish_string(rsText, writer_name = "html")
        html = html.decode("utf-8")
        html = html[html.find("<body>") + 6 : html.find("</body>")].strip()

    except:
        pass

    return html


def timeAgo(epoch):
    seconds = time.time() - epoch
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    months = days / 30
    years = months / 12

    if not years < 1:
        return f"{ int(years) } years ago"

    elif not months < 1:
        return f"{ int(months) } months ago"
    
    elif not days < 1:
        return f"{ int(days) } days ago"
    
    elif not hours < 1:
        return f"{ int(hours) } hours ago"
    
    elif not minutes < 1:
        return f"{ int(minutes) } minutes ago"
    
    else:
        return f"{ int(seconds) } seconds ago"


def convertSize(st_size):
    kb = st_size / 1024
    mb = kb / 1024
    gb = mb / 1024

    if not int(gb) < 1:
        return f"{ int(gb * 10) / 10 } GB"

    elif not int(mb) < 1:
        return f"{ int(mb * 10) / 10 } MB"

    elif not int(kb) < 1:
        return f"{ int(kb * 10) / 10 } KB"

    else:
        return f"{ st_size } B"
