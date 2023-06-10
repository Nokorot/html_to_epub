from books.RR_Template.cbs_base import Callbacks
import lxml.html

# This also works:
# code="""
# <hr style="border: none; height: 10px; background-image: url('separator.svg'); 
#     background-repeat: no-repeat; background-size: contain; background-position: center;">
# """

# This works in epub. But not on the kindle, with azw3 format
# code="""<div align="center" style="margin:1em;">
# <object data="{url}" type="image/svg+xml" width="80%"> </object>
# </div>
# """

code="""<div align="center" style="text-align:center; margin:1em">
<img src="{url}" width="80%"/></div>"""


class Callbacks(Callbacks):
    def chapter_text_callback(self, selector_match):
        for par in selector_match.cssselect('p'):
            # img = self.book.add_image("./books/MotherOfLearning/separator.svg", ext="svg")
            # url = img.get_epub_src();

            url = "./books/MotherOfLearning/separator.png"
            
            if (par.text == "- break -"):
                img = lxml.html.fromstring(code.format(url=url))
                par.getparent().replace(par, img)

        self.handle_tables(selector_match)
        return selector_match


