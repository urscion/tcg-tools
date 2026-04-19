#!/usr/bin/env python3

# Copyright 2026, Peter Clay (pwclay@gmail.com), All Rights Reserved

"""TCG Tools"""

from flask import Flask, render_template

from tools.swu import swu_bp

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


app.register_blueprint(swu_bp, url_prefix="/swu")
