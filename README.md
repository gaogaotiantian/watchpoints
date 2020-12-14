# watchpoints

[![build](https://github.com/gaogaotiantian/watchpoints/workflows/build/badge.svg)](https://github.com/gaogaotiantian/watchpoints/actions?query=workflow%3Abuild)  [![coverage](https://img.shields.io/codecov/c/github/gaogaotiantian/watchpoints)](https://codecov.io/gh/gaogaotiantian/watchpoints)  [![pypi](https://img.shields.io/pypi/v/watchpoints.svg)](https://pypi.org/project/watchpoints/)  [![support-version](https://img.shields.io/pypi/pyversions/watchpoints)](https://img.shields.io/pypi/pyversions/watchpoints)  [![license](https://img.shields.io/github/license/gaogaotiantian/watchpoints)](https://github.com/gaogaotiantian/watchpoints/blob/master/LICENSE)  [![commit](https://img.shields.io/github/last-commit/gaogaotiantian/watchpoints)](https://github.com/gaogaotiantian/watchpoints/commits/master)

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
====== Watchpoints Triggered ======
Call Stack (most recent call last):
  <module> (my_script.py:5):
>   a = 1
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
a.append(1)  # Trigger
a = {}  # Trigger
```

Even better, it can track the changes of the object after the changes of the variable

```python
from watchpoints import watch

a = []
watch(a)
a = {}  # Trigger
a["a"] = 2  # Trigger
```

Without doubts, it works whenever the object is changed, even if it's not in the same scope

```python
from watchpoints import watch

def func(var):
    var["a"] = 1

a = {}
watch(a)
func(a)
```

```
====== Watchpoints Triggered ======
Call Stack (most recent call last):
  <module> (my_script.py:8):
>   func(a)
  func (my_script.py:4):
>   var["a"] = 1
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
obj.a = 1  # Trigger
d["a"] = 1  # Trigger
```

Also, watchpoints supports native ```threading``` library for multi-threading. It will tell you which thread is changing the
value as well.

```
====== Watchpoints Triggered ======
---- Thread-1 ----
Call Stack (most recent call last):
  _bootstrap (/usr/lib/python3.8/threading.py:890):
>   self._bootstrap_inner()
  _bootstrap_inner (/usr/lib/python3.8/threading.py:932):
>   self.run()
  run (my_script.py:15):
>   a[0] = i
a:
[0]
->
[1]
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

### alias

You can give an alias to a monitored variable, so you can unwatch it anywhere. And the alias will be printed instead of the variable name
```python
from watchpoints import watch, unwatch

watch(a, alias="james")
# Many other stuff, scope changes
unwatch("james")
```

### conditional callback

You can give an extra condition filter to do "conditional watchpoints". Pass a function ```func(obj)``` which returns ```True```
if you want to trigger the callback to ```when``` of ```watch```

```python
a = 0
watch(a, when=lambda x: x > 0)
a = -1  # Won't trigger
a = 1  # Trigger
```

### variable vs object

When you do ```watch()``` on an object, you are actually tracking both the object and the variable holding it. In most cases, that's what
you want anyways. However, you can configure precisely which you want to track.

```python
a = []
watch(a, track="object")
a.append(1)  # Trigger
a = {}  # Won't trigger because the list object does not change

a = []
watch(a, track="variable")
a.append(1)  #  Won't trigger, because "a" still holds the same object
a = {}  # Trigger
```

### object compare and deepcopy

Nested object comparison is tricky. It's hard to find a solid standard to compare complicated customized objects.
By default, watchpoints will do a shallow copy of the object. You can override this behavior by passing ```deepcopy=True``` to ```watch()```

```python
watch(a, deepcopy=True)
```

watchpoints will honor ```__eq__``` method for user-defined classes first. If ```__eq__``` is not implemented, watchpoints will compare
```__dict__```(basically attibures) of the object if using shallow copy, and raise an ```NotImplementedError``` if using deepcopy.

The reason behind this is, if you deepcopied a complicated structure, there's no way for watchpoints to figure out if it's the same object
without user defined ```__eq__``` function.

### stack limit

You can specify the call stack limit printed using ```watch.config()```. The default value is ```5```, any positive integer is accepted.
You can use ```None``` for unlimited call stack, which means it will prints out all the frames.

```python
watch.config(stack_limit=10)
```

### customize callback

Of course sometimes you want to print in your own format, or even do something more than print. You can use your own callback for monitored variables

```python
watch(a, callback=my_callback)
```

The callback function takes three arguments

```python
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

### Integrating with pdb

watchpoints can be used with pdb with ease. You can trigger pdb just like using ```breakpoint()``` when
your monitored variable is changed. Simply do

```python
watch.config(pdb=True)
```

When you are in pdb, use ```q(uit)``` command to exit pdb, and the next change on the variable will trigger the pdb again.

### Avoid import

Sometimes it's a hassle having to import the function in every single file. You can install the watch function to builtins
and be able to call it in any files:

```python
watch.install()  # or watch.install("func_name") and use it as func_name()
# Remove it from the builtins
watch.uninstall()  # if installed with a name, pass it to uninstall() as well
```

## Limitations

* watchpoints uses ```sys.settrace()``` so it is not compatible with other libraries that use the same function.
* watchpoints will slow down your program significantly, like other debuggers, so use it for debugging purpose only
* ```watch()``` needs to be used by itself, not nested in other functions, to be correctly parsed
* at this point, there might be other issues because it's still in development phase

## Bugs/Requests

Please send bug reports and feature requests through [github issue tracker](https://github.com/gaogaotiantian/watchpoints/issues).

## License

Copyright Tian Gao, 2020.

Distributed under the terms of the  [Apache 2.0 license](https://github.com/gaogaotiantian/watchpoints/blob/master/LICENSE).