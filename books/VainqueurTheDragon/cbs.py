from books.RR_Template.cbs_base import Callbacks

class Callbacks(Callbacks):

    def chapter_text_callback(self, selector_match):
        self.handle_tables(selector_match)

        for div in selector_match.cssselect('strong'):
            if div.text and "webtoon adaptation" in div.text:
                div.drop_tree()
                # div.getparent().remove(div)

        for div in selector_match.cssselect('a'):
            if div.get('href') == "https://tapas.io/episode/2454114":
                div.drop_tree()
                # div.getparent().remove(div)

        return selector_match
