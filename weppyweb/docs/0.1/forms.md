Forms
=====

weppy provides the `Form` class to let you easily create forms for your application.

Let's see how to use it with an example:

```python
form weppy import Field, Form
from weppy.validators import IS_IN_SET

# create a form
@app.expose('/form')
def a():
    name_field = Field('name')
    int_field = Field('number', 'integer')
    type_field = Field('type')
    type_field.requires = IS_IN_SET(['type1', 'type2'])
    simple_form = Form([name_field, int_field, type_field])
    if simple_form.accepted:
        inserted_number = form.vars.number
        #do something
    return dict(form=simple_form)
```

As you can see the `Form` class accepts a list of `Field` objects for the input, we described them in the [DAL chapter](./dal#the-models-layer) of the documentation.   
Forms validate the input of the clients using their fields' validators: when the input passes the validation, the `accepted` attribute is set to `True`. The example above shows you that you can use this attribute to do stuffs when clients submit the form, and the submitted values are stored in `form.vars`.

Forms with DAL entities
-----------------------
Forms become quite handy to insert or edit data in your database, for this purpose weppy provides another class: `DALForm`.   
The usage is the same of the form, except that you pass one of your database tables to the constructor:

```python
from weppy import DALForm

# create a form for db.post table
@app.expose('/dalform')
def b():
    form = DALForm(db.post)
    if form.accepted:
        #do something
    return dict(form=form)
```

and if you are using models, creating a form is even easier:

```python
# create a form for Post model
@app.expose('/dalform')
def b():
    form = Post.form()
    if form.accepted:
        #do something
    return dict(form=form)
```

where obviously the `form()` method of the models is a shortcut for the `DALForm` class.

> – Wait, what if I need to edit a record?

You can pass the record as the second argument of `DALForm` or first argument in `Model.form()`:

```python
record = db.post(id=someid)
form = DALForm(db.post, record)
# or with models
record = db.Post(id=someid)
form = Post.form(record)
```

If you prefer, you can also use a record id:

```python
form = DALForm(db.post, record_id=someid)
# or with models
form = Post.form(record_id=someid)
```

Here is the complete list of parameters accepted by `Form` class:

| parameter | default | description |
| --- | --- | --- |
| _action | `None` | allows you to set the html `action` tag of the form |
| _method | `'POST'` | set the form submit method (GET or POST) |
| _enctype | `'multipart/form-data'` | allows you to change the encoding type for the submitted data |
| submit | `'Submit'` | the text to show in the submit button |
| formstyle | `FormStyle` | the class used to style the form |
| csrf | `'auto'` | Cross-Site Request Forgery protection |
| keepvalues | `False` | set if the form should keep the values in the input fields after submit |
| id_prefix | `None` | allows you to set a prefix for the id of the form fields |
| onvalidation | `None` | set an additional validation for the form |
| upload | `None` | define a url for download uploaded fields |

`DALForm` class add some parameters to the `Form` ones:

| parameter | description |
| --- | --- |
| record | as we seen above, set a record to edit |
| record_id | alternative to `record` using id |
| fields | list of fields (names) to show in the record |
| exclude_fields | list of fields (names) not to be included in the form |

> **Note:** `fields` and `exclude_fields` parameters should not be used together. The idea behind the presence of these parameters is the advantage of the one above the other depending on the use case. If you need to hide just a few fields you'd better using the `exclude_fields`, while if you have to show only few fields of your table, you should use the `fields` one.

###Uploads with forms
As we seen above, the `upload` parameter of forms needs an url for download. Let's focus a bit on uploads and see an example to completely understand this requirement.

Let's say you want to handle upload of avatar images from your user. So in your model/table you would have an upload field:

```python
Field('avatar', 'upload')
```

and the forms produced by weppy will handle uploads for you. But how would you display this image in your template?   
You need a streaming function like this:

```
from weppy import stream_file 

@app.expose("/download/<str:filename>")
def download(filename):
    stream_file(db, filename)
```

and then in your template you can create an `img` tag pointing to the `download` function you've just exposed:

```html
<img src="{{=url('download', record.avatar')}}" />
```

The `upload` parameter of `Form` class has the same purpose: when you edit an existent record the form will display the image or file link for the existing one uploaded. In this example you would do:

```python
record = db.post(id=someid)
form = DALForm(db.post, record, upload=url('download'))
# or with models
record = db.Post(id=someid)
form = Post.form(record, upload=url('download'))
```

Custom validation
-----------------
The `onvalidation` parameter of forms allows you to add custom validation logics on your form. You can pass a callable function, and it will be invoked after the form has processed the fields validators (which means that your function will be invoked only if there weren't errors with the fields validators).

Let's see what we're talking about with an example:

```python
@app.expose("/myform"):
def myform():
    def process_form(form):
        if form.vars.double != form.vars.number*2:
            form.errors.double = "Double is incorrect!"
        
    field1 = Field('number', 'integer')
    field2 = Field('double', 'integer')
    form = Form([field1, field2], onvalidation=process_form)
    return dict(form=form)
```

where basically the form check if the second number is the double of the first and return an error if the input is wrong.

You've just learnt how to use `onvalidation` parameter and that you can store errors in `form.errors` which is a `Storage` object like `form.vars`.

Customizing forms
-----------------
Good applications also need a good style. This is why weppy forms allows you to set a specific style with the `formstyle` attribute. But how you should edit the style of your form?   
Well, in weppy the style of a form is decided by the `FormStyle` class.

###Creating your style
*sub-section under writing*

###Custom widgets
*sub-section under writing*
