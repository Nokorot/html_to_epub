
import lxml.html
from lib.callbacks import Callbacks

class TestCallbacks(Callbacks):

    def __init__(self, config):
        self.config = config
        self.sections = dict()
    
    def chapter_section_callback(self, selector_matches):
        return "IR"
    
    def chapter_title_callback(self, selector_matches):
        return selector_matches[0].text

    def chapter_text_callback(self, selector_match):
        selector_match.cssselect('p')[0].drop_tree()

        for table in selector_match.cssselect('table'):
            table.set('style', None)

        for td in selector_match.cssselect('td'):
            td.set('style', "border: solid 1px; width: 100%;")

        for hr in selector_match.cssselect('hr'):
            # hr.set('style', "backgroud: sep.png")
            img = lxml.html.fromstring('<div align="center"><img src="sep.png" width=80%></div>')
            hr.getparent().replace(hr, img)
            # help(hr)
            # import sys
            # sys.exit(0)
        # for sm in selector_match:
        # if len(selector_match.cssselect('table')) == 0:
        #     return selector_match
        # else:
        #     return None
        # if len(selector_match.cssselect('a')) == 0:
        #     return selector_match
        # else:
        #     return None
        return selector_match

    # def text_css_selector(self, )<++>: 'div.chapter-inner table, div.chapter-inner hr, div.chapter-inner p'
