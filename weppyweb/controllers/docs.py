# -*- coding: utf-8 -*-

from weppy import response, abort, redirect, url, asis
from weppy.validators.process import Urlify
from weppyweb import app
from weppyweb.helpers.docs import (
    get_latest_version, get_versions, build_tree, get_sections, get_html,
    _get_chapter, is_page, get_navigation)


docs = app.module(__name__, "docs", url_prefix="docs", template_folder="docs")


@docs.route("/")
def index():
    redirect(url('.home', 'latest'))


@docs.route("/<str:version>")
def home(version):
    if version == 'latest':
        v = get_latest_version()
        redirect(url('.home', v))
    if version not in get_versions() + ["dev"]:
        redirect(url('.page', 'latest'))
    tree = build_tree(version)
    if not tree:
        abort(404)
    pages = []
    for v in tree:
        u = url('.page', [version, v[1]])
        sub_v = []
        if v[2]:
            for sv in v[2]:
                sub_v.append((sv[0], url('.page', [version, v[1], sv[1]])))
        else:
            for sv in v[3]:
                slug = Urlify(keep_underscores=True)(sv)[0]
                sub_v.append((sv, u + "#" + slug))
        pages.append((v[0], u, sub_v))
    #pages = [(v[0], url('.page', [version, v[1]]), v[2]) for v in tree]
    response.meta.title = "weppy - Docs"
    return dict(tree=pages, version=version, versions=["dev"] + get_versions())


@docs.route("/<str:version>/<str:p>(/<str:subp>)?")
def page(version, p, subp):
    if version == 'latest':
        v = get_latest_version()
        pargs = [v, p]
        if subp:
            pargs.append(subp)
        redirect(url('.page', pargs))
    if subp:
        requested_page = subp
        parent = p
    else:
        requested_page = p
        parent = None
    if not is_page(version, requested_page, parent):
        abort(404)
    _sections = get_sections(version, requested_page, parent)
    sections = []
    for s in _sections:
        sections.append((s, Urlify(keep_underscores=True)(s)[0]))
    body = asis(get_html(version, requested_page, parent))
    title = _get_chapter(version, requested_page, parent)
    response.meta.title = "weppy - Docs - " + title
    # for navigator
    prev, after = get_navigation(version, requested_page, parent)
    return dict(body=body, sections=sections, prev=prev, after=after)
