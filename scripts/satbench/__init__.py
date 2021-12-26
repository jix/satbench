from pathlib import Path

root = Path(__file__).parent.parent.parent

if root == root.parent:
    raise RuntimeError("could not find satbench root path")

__all__ = ["root"]
