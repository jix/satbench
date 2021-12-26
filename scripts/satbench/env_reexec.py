import sys
import os
from pathlib import Path
from . import root

if Path(sys.exec_prefix) != root / "env":
    path = root / "env/bin/python3"
    os.environ["PATH"] = ":".join(
        str(path) for path in
        [root / "env/bin", root / "scripts", "/usr/local/bin", "/usr/bin"]
    )
    os.execv(path, [path, *sys.argv])

__all__ = ["root"]
