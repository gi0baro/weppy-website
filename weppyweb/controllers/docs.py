from weppy import AppModule, abort, redirect, url, asis
from weppy.validators import IS_SLUG
from weppyweb import app
from weppyweb.helpers.docs import get_latest_version, get_versions, \
    build_tree, get_sections, get_html


docs = AppModule(app, "docs", __name__, url_prefix="docs",
                 template_folder="docs")


@docs.expose("/")
def index():
    redirect(url('.home', 'latest'))


@docs.expose("/<str:version>")
def home(version):
    if version == 'latest':
        v = get_latest_version()
        redirect(url('.home', v))
    if version not in get_versions():
        redirect(url('.page', ['latest', version]))
    tree = build_tree(version)
    if not tree:
        abort(404)
    pages = []
    for v in tree:
        u = url('.page', [version, v[1]])
        sub_v = []
        for sv in v[2]:
            slug = IS_SLUG()(sv)[0]
            sub_v.append((sv, u+"#"+slug))
        pages.append((v[0], u, sub_v))
    #pages = [(v[0], url('.page', [version, v[1]]), v[2]) for v in tree]
    return dict(tree=pages, version=version, versions=get_versions())


@docs.expose("/<str:version>/<str:p>")
def page(version, p):
    if version == 'latest':
        v = get_latest_version()
        redirect(url('.page', [v, p]))
    _sections = get_sections(version, p)
    sections = []
    for s in _sections:
        sections.append((s, IS_SLUG()(s)[0]))
    body = asis(get_html(version, p))
    return dict(body=body, sections=sections)
