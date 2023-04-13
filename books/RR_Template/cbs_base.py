from html_to_epub.callbacks import Callbacks
import lxml.html

class Callbacks(Callbacks):

    def chapter_section_callback(self, selector_matches):
        return self.config.book.title

    def handle_tables(self, selector_match):
        for table in selector_match.cssselect('table'):
            table.set('style', "border: solid 1px; width: 100%;")
            table.set('width', None)
            par = table.getparent()
            par.getparent().replace(par, table)

        for td in selector_match.cssselect('td'):
            td.set('style', "border: solid 1px; width: 100%;")
            td.set('width', None)

    def handle_hr_imgages(self, selector_match, hr_image_src):
        for hr in selector_match.cssselect('hr'):
            code = '<div align="center" style="text-align:center">' + \
                  f'<img src="{hr_image_src}" width=80%></div>'
            img = lxml.html.fromstring(code)
            hr.getparent().replace(hr, img)

    def chapter_text_callback(self, selector_match):
        self.handle_tables(selector_match)
        return selector_match

