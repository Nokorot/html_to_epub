from books.RR_Template.cbs_base import Callbacks

class Callbacks(Callbacks):
    current_book = 1

    def chapter_section_callback(self, selector_matches):
        markers = [ "Chapter 51", "Chapter 101", "Chapter 147", "Chapter 196", 
                   "Chapter 241", "Chapter 275", "Chapter 316", "Chapter 375", 'EEEENNNNDDDDD']

        if markers[self.current_book-1] in selector_matches[0].text:
            self.current_book += 1
            print("Next Book %s" % self.current_book)
        
        return "Book %s" % (self.current_book)

    def chapter_text_callback(self, selector_match):
        for span in selector_match.cssselect('span'):
            style = span.get('style')
            if not ('color' in style):
                continue

            a = style.split("rgba(", 1)[1]
            a = a.split(')')[0]
            c = [int(v) for v in a.split(',')]

            if not c:
                print(style)
                continue

            k = (c[0] << 16) + (c[1] << 8) + c[2]
            for child in span.iterdescendants():
                child.text = "#{:06x} {}".format(k, child.text)
                break;
    
        self.handle_tables(selector_match)
        
        
        sep_img_src = "./books/BTDM/sep.png"
        # sep_img_src = "https://www.royalroadcdn.com/public/ornaments/36299-ornament.png"
        self.handle_hr_imgages(selector_match, sep_img_src)

        for img in selector_match.cssselect('img'):
            if 'imgur.com' in img.get('src', ""):
                img.drop_tree()


        return selector_match
