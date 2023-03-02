from html_to_epub.callbacks import Callbacks
import lxml.html

class Callbacks(Callbacks):

    def chapter_section_callback(self, selector_matches):
        return "Vainqueur the Dragon"

    def chapter_text_callback(self, selector_match):
        for table in selector_match.cssselect('table'):
            table.set('style', "border: solid 1px; width: 100%;")
            table.set('width', None)
            par = table.getparent()
            par.getparent().replace(par, table)

        for td in selector_match.cssselect('td'):
            td.set('style', "border: solid 1px; width: 100%;")
            td.set('width', None)
        

        for div in selector_match.cssselect('strong'):
            if div.text and "webtoon adaptation" in div.text:
                div.drop_tree()
                # div.getparent().remove(div)

        for div in selector_match.cssselect('a'):
            if div.get('href') == "https://tapas.io/episode/2454114":
                div.drop_tree()
                # div.getparent().remove(div)

        for hr in selector_match.cssselect('hr'):
            print("Hey")

        return selector_match



