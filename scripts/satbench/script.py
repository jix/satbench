from .env_reexec import root
import argparse
import json
import os
import re
import sys
import resource
import traceback
from pathlib import Path
from duct import cmd

from . import runner, flock

task_id = os.environ.get("BENCHRUNNER_TASK")
task_name = os.environ.get("BENCHRUNNER_NAME")
cleanup_task = os.environ.get("BENCHRUNNER_CLEANUP")

_soft, _hard = resource.getrlimit(resource.RLIMIT_NOFILE)

resource.setrlimit(resource.RLIMIT_NOFILE, (_hard, _hard))


__all__ = ["root", "task_id", "task_name", "cleanup_task"]

__all__ += ["runner", "flock"]

__all__ += ["cmd", "Path"]

__all__ += ["argparse", "os", "sys", "re", "json", "traceback"]
