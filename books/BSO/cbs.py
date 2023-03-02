from html_to_epub.callbacks import Callbacks
import lxml.html
from lxml.etree import tostring

class Callbacks(Callbacks):

    def chapter_section_callback(self, selector_matches):
        return "Blade Skill Online"

    def chapter_text_callback(self, selector_match):
        for table in selector_match.cssselect('table'):
            table.set('style', "border: solid 1px; width: 100%;")
            table.set('width', None)
            par = table.getparent()
            par.getparent().replace(par, table)

        for td in selector_match.cssselect('td'):
            td.set('style', "border: solid 1px; width: 100%;")
            td.set('width', None)

        return selector_match
    
    def chapter_next_callback(self, selector_matches):
        for match in selector_matches:
            if match.text == "Next":
                return match.get('href')

        return None
