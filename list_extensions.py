#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from collections.abc import Iterable
from pathlib import Path
from toolz.functoolz import pipe
import filesystem

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
    pipe(filesystem.get_extensions_set(top_level_dir, recursive=args.recursive),
         print_extensions)
    
if __name__ == '__main__':
    main()
