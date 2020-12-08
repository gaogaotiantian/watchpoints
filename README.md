# watchpoints

[![build](https://github.com/gaogaotiantian/watchpoints/workflows/build/badge.svg)](https://github.com/gaogaotiantian/watchpoints/actions?query=workflow%3Abuild)

watchpoints is an easy-to-use, intuitive variable/object monitor tool for python that behaves similar to watchpoints in gdb.

## Install

```
pip install watchpoints
```

## Usage

### watch

Simply ```watch``` the variables you need to monitor!

```python
from watchpoints import watch

a = 0
watch(a)
a = 1
```

will generate

```
<module> (my_script.py:5):
a:
0
->
1
```

It works on both variable change and object change

```python
from watchpoints import watch

a = []
watch(a)
a.append(1)
a = {}
```

```
<module> (my_script.py:5):
a:
[]
->
[1]

<module> (my_script.py:6):
a:
[1]
->
{}
```

Even better, it can track the changes of the object after the changes of the variable

```python
from watchpoints import watch

a = []
watch(a)
a = {}
a["a"] = 2
```

```
<module> (my_script.py:5):
a:
[]
->
{}

<module> (my_script).py:6):
a:
{}
->
{'a': 2}
```

Without doubts, it works whenever the object is changed, even if it's not in the same scope

```python
from watchpoints import watch

def func(var):
    var["a"] = 1

a = {}
watch(a)
change(a)
```

```
func (my_script.py:4):
a:
{}
->
{'a': 1}
```

As you can imagine, you can monitor attributes of an object, or a specific element of a list or a dict

```python
from watchpoints import watch

class MyObj:
    def __init__(self):
        self.a = 0

obj = MyObj()
d = {"a": 0}
watch(obj.a, d["a"])  # Yes you can do this
obj.a = 1
d["a"] = 1
```

```
<module> (my_script.py:10):
obj.a:
0
->
1

<module> (my_script.py:11):
d["a"]:
0
->
1
```

**watchpoints will try to guess what you want to monitor, and monitor it as you expect**(well most of the time)

### unwatch

When you are done with the variable, you can unwatch it.

```python
from watchpoints import watch, unwatch

a = 0
watch(a)
a = 1
unwatch(a)
a = 2  # nothing will happen
```

Or you can unwatch everything by passing no argument to it

```python
unwatch()  # unwatch everything
```

**monitoring variables will introduce a significant overhead, and should be used for debugging only.**

### alias

You can give an alias to a monitored variable, so you can unwatch it anywhere. And the alias will be printed instead of the variable name
```python
from watchpoints import watch, unwatch

watch(a, alias="james")
# Many other stuff, scope changes
unwatch("james")
```

### customize callback

Of course sometimes you want to print in your own format, or even do something more than print. You can use your own callback for monitored variables

```python
watch(a, callback=my_callback)
```

The callback function takes three arguments

```
def my_callback(frame, elem, exec_info)
```

* ```frame``` is the current frame when a change is detected.
* ```elem``` is a ```WatchElement``` object that I'm to lazy to describe for now.
* ```exec_info``` is a tuple of ```(funcname, filename, lineno)``` of the line that changed the variable

You can also set change the callback function globally by

```python
watch.config(callback=my_callback)
```

Use ```restore()``` to restore the default callback
```python
watch.restore()
```

## Bugs/Requests

Please send bug reports and feature requests through [github issue tracker](https://github.com/gaogaotiantian/watchpoints/issues).

## License

Copyright Tian Gao, 2020.

Distributed under the terms of the  [Apache 2.0 license](https://github.com/gaogaotiantian/watchpoints/blob/master/LICENSE).