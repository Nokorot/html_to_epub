from ebooklib import epub
from lib.book import Book
from lib.chapter import Chapter
from lib.config import Config
from books.parahumans.parahumans import ParahumansHtmlCallbacks
import optparse, os, traceback, shutil, logging, sys

def parse_options():
    parser = optparse.OptionParser()
    parser.add_option('-c', '--clear-cache', dest='clear', default = False, action = 'store_true', help='Set to download a local copy of the website, clears local cache if it exists')
    parser.add_option('--config', dest='config', help='yaml config file')
    parser.add_option('-d', '--debug', dest='debug', default=False, action='store_true', help='enable debug output')

    return parser.parse_args()

def setup_logger(debug):
    root = logging.getLogger()
    ch = logging.StreamHandler(sys.stdout)

    if debug:
        root.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

if __name__ == '__main__':
    (options, args) = parse_options()

    setup_logger(options.debug)

    config = Config(options.config, options.debug)
    logging.getLogger().info(str(config))

    if options.clear and os.path.exists(config.cache):
        shutil.rmtree(config.cache)

    os.makedirs(config.cache, exist_ok=True)

    book = Book(config, ParahumansHtmlCallbacks(config))
    book.load_html()

    try:
        epub.write_epub(config.book.epub_filename, book.generate_epub(), {})
    except Exception as e:
        print(traceback.format_exc())