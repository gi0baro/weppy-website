# -*- coding: utf-8 -*-

block_routing = """
from weppy import App, request
from weppy.orm import Database, Model, Field
from weppy.tools import service

class Task(Model):
    name = Field.string()
    is_completed = Field.bool(default=False)

app = App(__name__)
db = Database(app)
db.define_models(Task)
app.pipeline = [db.pipe]

@app.route(methods='get')
@service.json
def tasks():
    page = request.params.page or 1
    return {
        'tasks': Task.all().select(
            paginate=(page, 20))}"""

block_orm_relations = """
from weppy.orm import Model, Field, has_many, belongs_to

class User(Model):
    name = Field.string()
    email = Field.string()
    has_many('posts')

    validation = {
        'email': {'is': 'email'}
    }

class Post(Model):
    belongs_to('user')
    body = Field.text()

    validation = {
        'body': {'presence': True}
    }"""

block_orm_aggregation = """
class Event(Model):
    location = Field.string()
    happens_at = Field.datetime()

db.define_models(Event)

events_count = Event.id.count()

db.where(
    Event.happens_at.year() == 1955
).select(
    Event.location,
    events_count,
    groupby=Event.location,
    orderby=~events_count,
    having=(events_count > 10))"""

block_templates = """
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


blocks = {
    'routing': block_routing,
    'orm_relations': block_orm_relations,
    'orm_aggregation': block_orm_aggregation,
    'templates': block_templates
}
