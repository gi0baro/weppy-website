# -*- coding: utf-8 -*-

from weppy import response
from .. import app, cache, redis
from ..helpers.code_blocks import blocks


@app.on_error(404)
def error_404():
    return app.render_template("404.haml")


@app.on_error(500)
def error_500():
    return app.render_template("500.haml")


@app.route("/")
@cache.response(query_params=False, language=False, duration=600)
def index():
    version = redis.get("weppy:last_version") or "0.1 Altair"
    response.meta.description = (
        "weppy is a full-stack python web framework designed with simplicity "
        "in mind")
    return {'version': version, 'code_blocks': blocks}
