Caching
=======

When you code a dynamic application, you will soon face its trade-off: **it is** dynamic. Each time a user does a request, your server makes all sorts of calculations – database queries, template rendering and so on – to create the final response.   
Now, for most web applications, this is not a big deal. But when your application starts becoming big and highly visited you would like to limit the overhead on your machines.

And that's where caching comes in.

The main idea behind cache is simple: we store somewhere the result of an expensive calculation to avoid performing the calculation next time. But, sincerely speaking, designing a good caching scheme is mainly a *PITA*, since it involves many complex evaluations about what you should store, where to store it, and so on.

So how weppy can help you on this? It provides some tools out of the box that let your development process focus on *what* to cache and not on *how* you should do that.

Low-level cache
---------------
Low-level caching becomes convenient when you want to cache a specific action, as a select on the database or a computation. Let's say, for example, that you have a blog and a certain function that exposes the last ten posts:

```python
@app.expose("/last")
def last():
    rows = db(db.Post.id > 0).select(orderby=~db.Post.date, limitby=(0, 10))
    return dict(posts=rows)
``` 

Now, since the performance bottleneck here is the call to the database, you can limit the overhead by caching the select result for 30 seconds, so you decrease the number of calls to your database. Here's where the weppy `Cache` class becomes handy:

```python
from weppy import Cache
cache = Cache()

@app.expose("/last")
def last():
    def _get():
        return db(db.Post.id > 0).select(orderby=~db.Post.date, limitby=(0, 10))
    return dict(posts=cache('last_posts', _get, 30))
```

You got how it works: you encapsulate the action you want to cache into a function, and then call your `cache` instance with a key, the function, and the amount of time (in seconds) you want to store the result of your function. weppy will take care of the rest.

> – ok dude. But where does weppy store the result?   
> – *you can choose it*

By default weppy stores your cached content into the RAM of your machine. But you can also use the disk or redis as storage system. Let's see these 3 systems in detail.

### RAM cache
This is the default cache mechanism of weppy. To use this system you just create a `Cache` instance and you can call it directly:

```python
from weppy import Cache
cache = Cache()
v = cache('my_key', my_f, my_time)
```
and the result of the `my_f` function will be stored and retrieved from RAM. Due to that, when you use this caching system, you must consider the size of the data you're storing, to avoid filling up all the memory of the machine. When you need to store large data in the cache – and when it happens you may ask yourself *why* you need to cache so much data – you'd better use the *disk cache*.

> **Note on multi-processing:**   
> When you store data in RAM cache, you are actually using the python process' memory. If you're running your web application using multiple processes/workers, every process will have its own cache and the data you store wont be available to the other ones.   
> If you need to have a shared cache between processes, you should use the *disk* or *redis*. 

### Disk cache
The disk cache is actually slower than the RAM or the redis ones, but if you need to cache large amounts of data, it fits the role perfectly. Here is how to use it:

```python
from weppy.cache import Cache, DiskCache
cache = Cache(disk=DiskCache())
v = cache('my_key', my_f, my_time)
```

### Redis Cache
[Redis](http://redis.io) is quite a good system for caching: is really fast – *really* – and if you're running your application with several workers, your data will be shared between your processes. To use it you just init the `Cache` class with the `RedisCache` handler:

```python
from weppy.cache import Cache, RedisCache
cache = Cache(redis=RedisCache(host='localhost', port=6379))
v = cache('my_key', my_f, my_time)
```

### Using multiple systems together
As you probably supposed, you can use multiple caching system together. Let's say you want to use the three systems we just described. You can do it simply:

```python
from weppy.cache import Cache, RamCache, DiskCache, RedisCache
cache = Cache(
    ram=RamCache(),
    disk=DiskCache(),
    redis=RedisCache()
)
v_ram = cache.ram('my_key', my_f, my_time)
v_disk = cache.disk('my_key', my_f, my_time)
v_redis = cache.redis('my_key', my_f, my_time)
```

You can also call

```python
v = cache('my_key', my_f, my_time)
```

and weppy will use the first handler you passed to `Cache` class when you created the instance – in this example would be the RAM one. And if you don't like configuring the default system using parameter order, you may prefer using the `default` parameter:

```python
cache = Cache(m=RamCache(), r=RedisCache(), default='r')
# ram cache get/store
v_ram = cache.m('my_key', my_f, my_time)
# redis cache get/store
v_redis1 = cache('my_key1', my_f1, my_time1)
v_redis2 = cache.r('my_key2', my_f2, my_time2)
```

### Custom caching handlers
*section under writing*
