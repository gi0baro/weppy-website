from weppyweb import app


@app.expose("/")
def index():
    return dict()
