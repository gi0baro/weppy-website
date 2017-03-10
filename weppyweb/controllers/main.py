# -*- coding: utf-8 -*-

from weppyweb import app, redis


@app.on_error(404)
def error_404():
    return app.render_template("404.haml")


@app.on_error(500)
def error_500():
    return app.render_template("500.haml")


@app.route("/")
def index():
    version = redis.get("weppy:last_version") or "0.1 Altair"
    return dict(version=version, tcode=template_example)


template_example = """
{{extend 'layout.html'}}

<div class="post-list">
{{for post in posts:}}
    <div class="post">
        <h2>{{=post.title}}</h2>
    </div>
{{pass}}
{{if not posts:}}
    <div>
        <em>No posts here so far.</em>
    </div>
{{pass}}
</div>"""
