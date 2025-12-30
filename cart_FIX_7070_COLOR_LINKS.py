#!/usr/bin/env python3
# FIX: Color-coded, clickable token events for 7070 Repo Walker

import json, time

COLOR_MAP = {
    "engineer": "blue",
    "fix": "green",
    "decide": "orange",
    "assimilate": "purple",
}

def emit_event(events, msg, mode="engineer", link=None):
    evt = {
        "ts": time.strftime("%H:%M:%S"),
        "msg": msg,
        "color": COLOR_MAP.get(mode, "blue"),
        "link": link,
        "mode": mode,
    }
    events.append(evt)
    if len(events) > 500:
        events.pop(0)
    return evt
