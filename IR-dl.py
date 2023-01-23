
import sys, os, optparse
import json, yaml
import tempfile
import requests, xmltodict
from datetime import datetime
from dateutil import parser as date_parser

from lib.callbacks import get_callback_class
from lib.book import Book

from ebooklib import epub

__description = '''\
Download the new chapters from royal road and turn them into an epub file.'''

from lib.config import Config


def getChapters(url, data):
    def genConfig():
        config = {}
        config['cache'] = data['cache']
        config['ignore_cache'] = data.get('ignore_cache', True)
        config['callbacks'] = data['callbacks']
        config['book'] = data['book']
        config['book']['entry_point'] = url
        date = datetime.now().__format__("%F")
        config['book']['epub_filename'] = \
                data['book']['epub_filename'].replace('%date', date)
        return config

    config = Config(genConfig())

    os.makedirs(config.cache, exist_ok=True)

    # Note: This looks very relative
    klass = get_callback_class(config.callbacks)

    book = Book(config, klass(config))
    book.load_html()

    print(config.book.epub_filename)
    epub.write_epub(config.book.epub_filename, book.generate_epub(), {})


# Note: this code is very spesific
def getOldestNew(url, lastTime):
    r = requests.get(url, allow_redirects=True)
    feed = xmltodict.parse(r.content.decode("utf8"))
    channel = feed['rss']['channel']

    # This is crapy code, but who cears
    oldestNew = None
    for item in channel['item']:
        item['pubDate'] = pubDate = date_parser.parse(item['pubDate'])
        if (pubDate > lastTime and \
                (not oldestNew or oldestNew['pubDate'] > pubDate)):
            print(item['link'])
            oldestNew = item
    return oldestNew


def main(dataFile, *args):
    # For preserving the structure of the yaml file
    from ruamel.yaml import YAML, util

    data, ind, bsi = util.load_yaml_guess_indent(open(dataFile))
    # with open(dataFile, "r") as f:
    #     data = yaml.safe_load(f)

    rss_url = data['rss_url']
    lastTime = date_parser.parse(data['lastTime'])
    oldestNew = getOldestNew(rss_url, lastTime)

    if not oldestNew:
        print("There are no updates!")
        sys.exit(0)

    getChapters(oldestNew['link'], data)
    data['lastTime'] = datetime.now().isoformat(timespec='seconds') + '+0000'

    yaml = YAML()
    yaml.indent(mapping=ind, sequence=ind, offset=bsi)
    with open(dataFile, 'w') as fp:
        yaml.dump(data, fp)
    # with open(dataFile, "wb") as f:
    #     f.write(bytes(yaml.dump(data), 'utf-8'))


if __name__ == "__main__":
    usage = "%prog [options] <dataFile>"
    parser = optparse.OptionParser(usage = usage, description=__description)
    parser.add_option('--config', dest='config', help='yaml config file')
    parser.add_option('-d', '--debug', dest='debug', default=False, action='store_true', help='enable debug output')
    parser.add_option('--toc-break', dest='toc_break', default=False, action='store_true', help='Only parse table of contents, useful when debugging a new web site')

    (options, args) = parser.parse_args()

    if len(args) < 1:
       sys.stderr.write('ERROR: Not enough arguments!\n');
       parser.print_usage(sys.stderr)
       sys.stderr.write('use -h for more infromation.\n')
       sys.exit(1)

    main(*args)
