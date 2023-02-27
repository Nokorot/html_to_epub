from html_to_epub.callbacks import Callbacks
import lxml.html

class Callbacks(Callbacks):

    def chapter_text_callback(self, selector_match):
        for img in selector_match.cssselect('img'):
            if self.config.custom['load_images']:
                # TODO: Should down-scale imeages, to a more appropriate resolution
                img = self.book.add_image(img.get('src'))
                img.set('src', img.get_src())
            else:
                img.drop_tree()
 

        for bq in selector_match.cssselect('blockquote'):
            bq.set('style', "border-left: solid 1px; width: 100%;")

        for table in selector_match.cssselect('table'):
            table.set('style', None)


        for td in selector_match.cssselect('td'):
            td.set('style', "border: solid 1px; width: 100%;")

        return selector_match
