#!/usr/bin/env python3

from argparse import Namespace
from collections.abc import Iterable
from functools import partial
from itertools import groupby
from pathlib import Path
from sys import stdout

from _command_line import setup_command_line
import filesystem

_INDENT = ' ' * 2

def print_files_by_extension(grouped_files: Iterable[str, Iterable[Path]],
    file=stdout) \
        -> None:
    
    printf = partial(print, file=file)
        
    for ext, files in grouped_files:
        if not ext:
            printf(f'{_INDENT}(no extension)')
        else:
            printf(f'{_INDENT}{ext}')
        for file in files:
            printf(f'{_INDENT * 2}{file}')

def get_sort_key(p: Path):
    return (p.suffix, str(p))

def main():
    args : Namespace = setup_command_line()

    print('Extensions:')
    top_level_dir = args.top_level_dir.expanduser()

    file_list = sorted(filesystem.get_files(top_level_dir), key=get_sort_key)
    grouped_files = groupby(file_list, key=lambda p: p.suffix)

    print_files_by_extension(grouped_files)
    
if __name__ == '__main__':
    main()
