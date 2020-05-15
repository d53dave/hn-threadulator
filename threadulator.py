import sys
import ujson
import requests

from collections import OrderedDict
from typing import Dict, Any, List, Optional
from time import sleep

HN_API_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'


def process_id(hn_id: str, delay=0.0) -> Optional[Dict[str, Any]]:
    sleep(delay)
    print(f'Processing {HN_API_URL.format(hn_id)}')
    r = requests.get(HN_API_URL.format(hn_id))
    r.raise_for_status()

    item = r.json()
    if item is not None:
        try:
            expanded_kids = [process_id(kid, delay=0.5) for kid in item['kids'] if kid is not None]
            item['kids'] = expanded_kids
        except KeyError:
            pass

        ordered_item = OrderedDict(sorted(item.items(), reverse=True, key=lambda t: t[0]))
        return ordered_item

    return item


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python threadulator.py <id>')
        sys.exit(1)

    hn_id = str(sys.argv[1])
    content = process_id(hn_id)

    print(ujson.dumps(content, indent=2))