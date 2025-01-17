# from ebooklib import epub
# import uuid, logging

import os

from .util import Network

class Image:
    data = None


    def __init__(self, config, ref, url, ext=None):
        self.config = config
        self.ref = ref

        ## References to this image in the book. Useful for debugging
        self.references = []

        self.is_local = not (url.startswith("http://") or url.startswith("https://"))

        # TODO: This might crash
        if ext:
            self.fileext = ext
        else:
            self.fileext = os.path.splitext(url)[1]

        if self.is_local:
            self.url = url
            self.cache_filename = None
        else:
            self.url = Network.clean_url(url)

            self.cache_filename = Network.cache_filename(self.config.cache, self.url, self.fileext)

    def add_reference(self, reference):
        self.references.append(reference)


    def get_epub_src(self):
        return "./" + self.config.images_dir + self.ref + "." + self.fileext 

    def media_type(self):
        return {
                "png": "image/png",
                "jpg": 'image/jpeg',
                "jpeg": 'image/jpeg',
                "svg": "image/svg+xml",
        }.get(self.fileext, "image/jpeg");

    '''
    Cache (if necessary) and load file descriptor into memory
    '''
    def load_file(self):
        if self.data:
            return self.data

        if self.is_local:
            with open(self.url, 'rb') as f:
                self.data = f.read()
                return self.data

        try:
            with Network.load_and_cache(self.url, self.cache_filename, self.config.ignore_cache) as f:
                self.data = f.read()
                return self.data
        except:
            return None
        
