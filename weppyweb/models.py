# -*- coding: utf-8 -*-

from weppy import now
from weppy.orm import Model, Field


class Version(Model):
    name = Field()
    gittag = Field()


class Extension(Model):
    name = Field()
    slug = Field()
    description = Field()
    author_name = Field()
    author_email = Field()
    github = Field()
    pypi = Field()
    version = Field()
    website = Field()
    bugtracker = Field()
    license = Field()
    status = Field()
    data = Field.text()
    updated = Field.datetime()

    default_values = {
        'updated': now
    }

    update_values = {
        'updated': now
    }
