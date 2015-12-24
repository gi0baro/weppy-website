from datetime import datetime
from weppy.dal import Model, Field


class Version(Model):
    tablename = "versions"

    name = Field()
    gittag = Field()


class Extension(Model):
    tablename = "extensions"

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
    data = Field('text')
    updated = Field('datetime')

    default_values = {
        'updated': lambda: datetime.utcnow()
    }

    update_values = {
        'updated': lambda: datetime.utcnow()
    }
