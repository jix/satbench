from contextlib import contextmanager
import fcntl
import os
import json


def append_line(path, line):
    with open(path, "r+b") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        file.seek(0, os.SEEK_END)
        pos = file.tell()
        if pos == 0:
            file.write(f"{line}\n".encode())
        else:
            # Make sure we always start writing on a new line in case the previous
            # writer got interrupted
            file.seek(pos - 1, os.SEEK_SET)
            file.write(f"\n{line}\n".encode())
        file.flush()


def append_json(path, **data):
    append_line(path, json.dumps(data))
