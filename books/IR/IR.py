from books.RR_Template.cbs_base import Callbacks
import lxml.html

class TestCallbacks(Callbacks):
    
    def chapter_text_callback(self, selector_match):
        # selector_match.cssselect('p')[0].drop_tree()
        
        self.handle_tables(selector_match)
        
        # hr_image_src = "https://www.royalroad.com/dist/img/ornaments/16.png"
        hr_image_src = "./books/IR/sep.png"
        self.handle_hr_imgages(selector_match, hr_image_src)
        
        return selector_match
