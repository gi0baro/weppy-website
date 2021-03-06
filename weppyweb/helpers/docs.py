# -*- coding: utf-8 -*-

import os
from yaml import load as ymlload
from markdown2 import markdown
from .. import app, cache

_docs_path = os.path.join(app.root_path, 'docs')


def _build_filepath(version, name, parent=None):
    args = [_docs_path, version, name + ".md"]
    if parent:
        args.insert(2, parent)
    return os.path.join(*args)


@cache('docs_versions', duration=600)
def get_versions():
    versions = []
    for name in os.listdir(_docs_path):
        if name != "dev" and os.path.isdir(os.path.join(_docs_path, name)):
            versions.append(name)
    return sorted(versions, reverse=True)


def get_latest_version():
    latest_version = max([float(v) for v in get_versions()])
    return str(latest_version)


def is_page(version, name, parent=None):
    path = _build_filepath(version, name, parent)
    return os.path.exists(path)


def _get_lines(version, name, parent=None):
    with open(_build_filepath(version, name, parent)) as f:
        lines = f.readlines()
    return lines


def get_chapter(version, name, parent=None):
    lines = _get_lines(version, name, parent)
    chapter = name
    for i in range(0, len(lines)):
        if lines[i].startswith("==="):
            chapter = lines[i - 1]
            break
    return chapter


def get_sections(version, name, parent=None):
    lines = _get_lines(version, name, parent)
    sections = []
    for i in range(0, len(lines)):
        if lines[i].startswith("---"):
            sections.append(lines[i - 1].replace("\\", ""))
    return sections


def _get_subpages(version, parent, pages):
    rv = []
    for page in pages:
        title = get_chapter(version, page, parent)
        sections = get_sections(version, page, parent)
        rv.append((title, page, [], sections))
    return rv


def build_tree(version):
    folder = os.path.join(_docs_path, version)
    if not os.path.exists(folder):
        return None
    with open(os.path.join(folder, 'tree.yml')) as f:
        tree = ymlload(f)
    complete_tree = []
    subpaged = []
    for name in tree:
        if isinstance(name, dict):
            rname = list(name)[0]
            subpaged.append(rname)
            ch_name = get_chapter(version, rname)
            sub_tree = _get_subpages(version, rname, name[rname])
            complete_tree.append((ch_name, rname, sub_tree, []))
        else:
            if name in subpaged:
                continue
            ch_name = get_chapter(version, name)
            sub_tree = get_sections(version, name)
            complete_tree.append((ch_name, name, [], sub_tree))
    return complete_tree


def get_text(version, name, parent=None):
    with open(_build_filepath(version, name, parent)) as f:
        text = f.read()
    return text


def get_html(version, name, parent=None):
    text = get_text(version, name, parent)
    if text is None:
        return text
    extras = ['tables', 'fenced-code-blocks', 'header-ids']
    return markdown(text, extras=extras).encode('utf-8')


def _navigation_tree_pos(tree, pname):
    rv = None
    for i in range(0, len(tree)):
        if tree[i][1] == pname:
            rv = i
            break
    return rv


def _navigation_data(version, tree_obj, parent=None):
    if tree_obj is None:
        return tree_obj
    return tree_obj[0], tree_obj[1], parent, version


def _tree_nav(version, tree, page, subtree=True):
    prev, after = None, None
    index = _navigation_tree_pos(tree, page)
    if index > 0:
        prev = tree[index - 1]
    if index < len(tree) - 1:
        after = tree[index + 1]
    current_parent = None
    if subtree and tree[index][2]:
        after = tree[index][2][0]
        current_parent = page
    return (
        _navigation_data(version, prev),
        _navigation_data(version, after, current_parent))


def get_navigation(version, page, parent=None):
    prev, after = None, None
    tree = build_tree(version)
    if not parent:
        prev, after = _tree_nav(version, tree, page)
    else:
        pindex = _navigation_tree_pos(tree, parent)
        subtree = tree[pindex]
        index = _navigation_tree_pos(subtree[2], page)
        if index > 0:
            prev = _navigation_data(version, subtree[2][index - 1], parent)
        else:
            prev = _navigation_data(version, tree[pindex])
        if index < len(subtree[2]) - 1:
            after = _navigation_data(version, subtree[2][index + 1], parent)
        else:
            after = _tree_nav(version, tree, parent, False)[1]
    return prev, after
