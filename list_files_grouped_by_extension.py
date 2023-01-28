#!/usr/bin/env python3

import subprocess

from argparse import Namespace
from collections.abc import Iterable
from datetime import datetime, date, time
from functools import partial
from itertools import groupby
from pathlib import Path
from sys import stdout

from _command_line import setup_command_line
import filesystem

_INDENT = ' ' * 2

# TODO: Refactor to generalize, possibly using callbacks to handle formatting 
# differences
def print_files_by_extension(grouped_files: Iterable[str, Iterable[Path]], \
    file=stdout) -> None:
    
    printf = partial(print, file=file)
        
    for ext, files in grouped_files:
        if not ext:
            printf(f'{_INDENT}(no extension)')
        else:
            printf(f'{_INDENT}{ext}')
        for file in files:
            printf(f'{_INDENT * 2}{file}')
            
_ASCIIDOC_SUFFIX = '.adoc'

def print_to_asciidoc(grouped_files: Iterable[str, Iterable[Path]], 
    filename: str, top_level_dir: Path=None) -> None:
        
    asciidoc_path = Path(filename)
    if asciidoc_path.suffix != _ASCIIDOC_SUFFIX:
        asciidoc_path.rename(asciidoc_path.with_suffix(_ASCIIDOC_SUFFIX))
    with asciidoc_path.open(mode='w') as fp:
        printf = partial(print, file=fp)
        
        if top_level_dir:
            printf(f'= {top_level_dir}')
        else:
            printf(f'= {asciidoc_path.as_posix()}')

        printf(':toc: left')
        printf()
        printf('== Extensions')
        
        for ext, file_names in grouped_files:
            if not ext:
                printf(f'=== (no extension)')
            else:
                printf(f'=== {ext}') 
           
            printf('----')
            printf()
            for file_name in file_names:
                printf(f'{file_name}')   
            printf('----')
            
def get_sort_key(p: Path):
    return (p.suffix, str(p))

def format_with_date(format_string='{date_str}', with_time=False) -> str:
    if with_time:
        now_str =  f'{datetime.now(): "%Y_%m_%d_%H_%M"}'
        return format_string.format(date_str=now_str)
    else:
        today_str = f'{datetime.today():%Y_%m_%d}'
        return format_string.format(date_str=today_str)

def main():
    args : Namespace = setup_command_line()

    top_level_dir: Path = args.top_level_dir.expanduser()

    file_list = sorted(filesystem.get_files(top_level_dir), key=get_sort_key)
    grouped_files = groupby(file_list, key=lambda p: p.suffix)

    # print_files_by_extension(grouped_files)
    asciidoc_dest_folder = top_level_dir.parent
    asciidoc_file_name = format_with_date('YouTube_DL_{date_str}.adoc')
    print_to_asciidoc(grouped_files, 
                  Path(asciidoc_dest_folder / asciidoc_file_name).as_posix(),
                  top_level_dir)
    
if __name__ == '__main__':
    main()
