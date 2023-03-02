from html_to_epub.callbacks import Callbacks
import lxml.html

class TestCallbacks(Callbacks):
    
    def chapter_section_callback(self, selector_matches):
        return "IR"

    def chapter_text_callback(self, selector_match):
        selector_match.cssselect('p')[0].drop_tree()

        for table in selector_match.cssselect('table'):
            table.set('style', None)

        for td in selector_match.cssselect('td'):
            td.set('style', "border: solid 1px; width: 100%;")

            
        for hr in selector_match.cssselect('hr'):
            img_src = self.book.get_image_src('sep.png')
            div = f'<div align="center" style="text-align:center"> <img src="{img_src}" width=50%></div>'
            img = lxml.html.fromstring(div)
            hr.getparent().replace(hr, img)

        return selector_match
