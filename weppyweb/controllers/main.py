from weppyweb import app, redis


@app.on_error(404)
def error_404():
    return app.render_template("404.haml")


@app.on_error(500)
def error_500():
    return app.render_template("500.haml")


@app.expose("/")
def index():
    version = redis.get("weppy:last_version") or "0.1 Altair"
    return dict(version=version)
