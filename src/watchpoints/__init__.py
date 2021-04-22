# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from .watch import Watch

__version__ = "0.2.4"


all = [
    "watch",
    "unwatch"
]


watch = Watch()
unwatch = watch.unwatch
