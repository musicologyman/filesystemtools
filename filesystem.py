#!/usr/bin/env python3

from collections.abc import Iterable, Sequence
from functools import partial
from itertools import chain, groupby
from pathlib import Path
from typing import Any
from toolz.functoolz import curry, pipe

def get_files(parent: Path, recursive: bool=True) -> Iterable[Path]:
    return chain((p for p in parent.iterdir() if p.is_file()),
                 *(get_files(p) for p in parent.iterdir() 
                   if recursive and p.is_dir()))

def get_extensions(parent: Path, recursive: bool=True) -> Iterable[str]:
    return (p.suffix for p in get_files(parent, recursive))

def get_extensions_set(parent: Path, recursive: bool=True) -> Iterable[str]:
    return pipe(get_extensions(parent, recursive),
                set,
                partial(sorted, key=str.lower))
