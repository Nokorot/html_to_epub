from collections import OrderedDict
from ebooklib import epub
from tqdm import tqdm
import pickle, uuid, logging

import hashlib

from .chapter import Chapter
from .image import Image

'''
Book class - handles most of the epub stuff as well as initalizing TableOfContents and Chapters
'''
class Book:
    def __init__(self, config, callbacks):
        self.config = config
        self.callbacks = callbacks
        self.chapters = []
        self.title = config.book.title
        self.author = config.book.author

        callbacks.book = self

        print(config.book.cover_img)
        if config.book.cover_img:
            # TODO: This ext should not be hard coded here
            self.cover_img = Image(config, "cover", config.book.cover_img, ext='.png')
        else:
            self.cover_img = None

        self.images = {}
        for (key, value) in config.book.images.items():
            self.add_image(value, key)

        with open(config.book.css_filename, 'r') as css:
            self.css = epub.EpubItem(uid='default', file_name="style/"+config.book.css_filename, media_type="text/css", content=css.read())


    def add_image(self, url, ref=None):
        if not ref:
            # TODO: This could be more clever
            # ref = "image_%u" % len(self.images)
            ref = hashlib.md5(url.encode('utf-8')).hexdigest()
        if not self.images.__contains__(ref):
            self.images[ref] = Image(self.config, ref, url)

        return self.images[ref];

    '''
    Walks through a web page starting with config.book.entry_points, finding a 'next chapter' link and continueing until
    a next chapter link cannot be found. If a web page exists in the cache it will be loaded from the local file,
    otherwise it will download the web page and then load the dom.

    Must be called before generate_epub. Thought of having generate_epub call this but since it does so much (downloading potentially
    hundreds of megs of data) I wanted to give the caller more control over it.
    '''
    def load_html(self):
        entry_points = self.config.book.entry_points
        entry_point_count = 0
        max_iterations = self.config.max_chapter_iterations
        i = 0

        current = None
        logging.getLogger().info('Walking through chapters (this could take a while)')
        with tqdm() as pbar:
            while  i < max_iterations:
                if current is None:
                    if len(entry_points) <= entry_point_count:
                        break;
                    current = Chapter(self, entry_points[entry_point_count], \
                            self.config, self.callbacks)
                    entry_point_count += 1

                current.load_html()
                self.chapters.append(current)
                print(f"Adding chapter \"{current.title}\"")

                next = current.get_next_chapter()
                if (next is None) and current.is_cashed \
                       and self.config.ignore_last_cache \
                       and (not self.config.ignore_cache):
                    current.load_html(ignore_cache=True)
                    next = current.get_next_chapter()
                current = next
                i += 1
                pbar.update(1)

            if i == max_iterations:
                # Note: Infinite loop detection could also be detecte by, storing a list of visited urls
                logging.getLogger().warn('Possible infinite loop detected, check your next_chapter_css_selector and/or chapter_next_callback callback function or increase config.max_chapter_iterations value')
            
            self.chapters = self.callbacks.sort_chapters(self.chapters)



    # initalizes some basic stuff needed by ebooklib: title, author, css, etc.
    def init_epub(self):
        self.book = epub.EpubBook()
        self.book.set_identifier(str(uuid.uuid4()))
        self.book.set_title(self.title)
        self.book.set_language('en')
        self.book.add_author(self.author)
        self.book.add_item(self.css)

        if self.cover_img:
            print("Adding Conver: '%s'" % self.cover_img.ref)
            data = self.cover_img.load_file()
            self.book.set_cover(self.cover_img.ref + self.cover_img.fileext, data)

    '''
    Turn our TableOfContetns and Chapter objects into epub format. At this point you should have called
    init_html() or you will get NoneType exceptions because the dom isnt loaded.
    '''
    def generate_epub(self):
        logging.getLogger().info('Initializing epub')
        self.init_epub()

        #spine is used when navigating forward and backward through the epub
        #first element is 'nav' followed by each epub.EpubHtml chapter in order
        self.book.spine = ['nav']

        sections = OrderedDict()
        current_section = None

        logging.getLogger().info('Generate chapters')
        for chapter in tqdm(self.chapters, disable=self.config.debug):
            epub_chapter = chapter.to_epub(self.css)

            self.book.add_item(epub_chapter)
            self.book.spine.append(epub_chapter) # the spin is yet another epub navigational thing. theres lots of that.

            # TODO: make table of contents section optional
            epub_section = chapter.get_epub_section()

            if epub_section not in sections:
                sections[epub_section] = []
            sections[epub_section].append(epub_chapter)

        logging.getLogger().info('Generating table of contents')

        # Load and include all images into the epub
        for i, (ref, img) in enumerate(self.images.items()):
            # TODO:3 At the moment I'm expecting ext as a part of key
            # print("Adding Image: '%s'" % img.url)
            print("Adding Image: '%s' as '%s'" % (img.url, ref))
            data = img.load_file()

            # TODO: Need to fix the media type, though it seams to work fine also with png atm.
            img = epub.EpubImage(
                    uid         = 'image_%u' % (i),
                    file_name   =  self.config.images_dir + ref,
                    media_type  = 'image/jpeg',
                    content     = data)
            self.book.add_item(img)


        # TODO: make table of contents section optional
        self.book.toc = [(epub.Section(section), tuple(chapters)) for section, chapters in tqdm(sections.items(), disable=self.config.debug)]

        # this is some boiler plate to build the navigational structures required by epub
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        logging.getLogger().info('Finished genetaring ebook')
        return self.book
