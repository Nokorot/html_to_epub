
import lxml.html
from lib.callbacks import Callbacks

import re
from parse import parse

class Callbacks(Callbacks):

    def __init__(self, config):
        self.config = config
        self.current_book = 1

    def chapter_section_callback(self, selector_matches):
        return "ThePerfectRun"

    def chapter_title_callback(self, selector_matches):
        return selector_matches[0].text

    def chapter_text_callback(self, selector_match):
        for img in selector_match.cssselect('img'):
            if self.config.custom['load_images']:
                # TODO: Should down-scale imeages, to a more appropriate resolution
                img = self.book.add_image(img.get('src'))
                img.set('src', img.get_src())
            else:
                img.drop_tree()
 
        for table in selector_match.cssselect('table'):
            table.set('style', "border: solid 1px; width: 100%;")
            table.set('width', None)
            par = table.getparent()
            par.getparent().replace(par, table)

        for td in selector_match.cssselect('td'):
            td.set('style', "border: solid 1px; width: 100%;")
            td.set('width', None)

        for hr in selector_match.cssselect('hr'):
            print("Hey")
            # hr.set('style', "backgroud: sep.png")
            # img_src = self.book.get_image_src('sep.png')
            # 
            # img = lxml.html.fromstring(f'<div align="center" style="text-align:center"><img src="{img_src}" width=80%></div>')
            # hr.getparent().replace(hr, img)
        return selector_match
