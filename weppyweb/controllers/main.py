from weppyweb import app, redis


@app.expose("/")
def index():
    version = redis.get("weppy:last_version") or "0.1 Altair"
    return dict(version=version)
