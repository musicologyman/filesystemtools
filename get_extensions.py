#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from collections.abc import Iterable
from functools import partial
from itertools import chain
from pathlib import Path
from toolz.functoolz import pipe

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

def setup_command_line() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('top_level_dir', type=Path)
    parser.add_argument('-r', '--recursive', action='store_true')
    return parser.parse_args()

def print_extensions(extensions: Iterable[str]) -> None:
    INDENT = ' ' * 2
    for ext in extensions:
        if not ext:
            print(f'{INDENT}(no extension)')
        else:
            print(f'{INDENT}{ext}')

def main():
    args : Namespace = setup_command_line()

    print('Extensions:')
    top_level_dir = args.top_level_dir.expanduser()
    pipe(get_extensions_set(top_level_dir, recursive=args.recursive),
         print_extensions)
    
if __name__ == '__main__':
    main()
