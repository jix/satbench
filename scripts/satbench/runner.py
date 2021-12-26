import socket
import json
import os

from . import root


def connect(command):
    connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    connection.connect(f"/run/user/{os.getuid()}/benchrunner/benchrunner.sock")
    connection_file = connection.makefile("rw")
    print(json.dumps(command), file=connection_file, flush=True)

    for line in connection_file:
        response = json.loads(line)
        if err := response.get("Err"):
            raise RuntimeError(err)
        yield response["Ok"]


def add_tasks(tasks):
    return connect(dict(AddTasks=dict(tasks=list(tasks))))


def task(**kwargs):
    kwargs.setdefault("env", {})
    kwargs["env"] = {
        "PATH": f"{root}/env/bin:{root}/scripts:/usr/local/bin:/usr/bin",
        **kwargs.get("env", {}),
    }
    return kwargs


def ping():
    got_pong = False
    for reply in connect("Ping"):
        if reply == "Pong":
            got_pong = True
    if not got_pong:
        raise RuntimeError("no Pong reply")
