from html_to_epub.callbacks import Callbacks
import lxml.html

class TestCallbacks(Callbacks):
    def __init__(self, config):
        super(self, config)
        self.sections = dict()
    
    def chapter_section_callback(self, selector_matches):
        return "IR"

    def chapter_text_callback(self, selector_match):
        selector_match.cssselect('p')[0].drop_tree()

        for table in selector_match.cssselect('table'):
            table.set('style', None)

        for td in selector_match.cssselect('td'):
            td.set('style', "border: solid 1px; width: 100%;")

        for hr in selector_match.cssselect('hr'):
            img = lxml.html.fromstring('<div align="center"><img src="sep.png" width=80%></div>')
            hr.getparent().replace(hr, img)
        return selector_match
