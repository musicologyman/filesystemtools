from argparse import ArgumentParser, Namespace
from pathlib import Path

def setup_command_line() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('top_level_dir', type=Path)
    parser.add_argument('-r', '--recursive', action='store_true')
    return parser.parse_args()
