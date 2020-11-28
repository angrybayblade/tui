import sys

from watcher import watcher

config = {
    "proc":watcher.PROCESS,
    "trigger":["python","./run.py"],
    "mode":1,
    "path":"./",
    "files":[

    ],
}

watch = watcher.Watcher(**config)
watch.start()
watch.observe()