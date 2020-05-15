#!/usr/bin/env python3

import sys
import ujson

from html import unescape

def clean_text(text, indent_str):
    unescaped = unescape(text)
    clean = unescaped.replace('\n', '\n' + indent_str)
    return clean


def print_kids(content, indent = 1) -> None:
    indent_str = '> ' * indent
    for kid in content.get('kids', []):
        if kid is None:
            continue
        if 'deleted' in kid:
            print(f'{indent_str} [deleted]')
        else:
            print('')
            print(
                f'{indent_str} **{kid["by"]}** comments: <br /> {clean_text(kid["text"], indent_str)}')
        print_kids(kid, indent=indent+1)
    print('')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print('Usage: cat file.json | markdownulator.py')
        sys.exit(0)

    input_str = sys.stdin.read()
    content = ujson.loads(input_str)

    print(f'# {content["title"]}')
    if 'text' in content:
        print(content['text'])
    print('')
    print_kids(content)
