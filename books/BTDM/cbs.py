from html_to_epub.callbacks import Callbacks
import lxml.html

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
        for img in selector_match.cssselect('img'):
            if self.config.custom['load_images']:
                # TODO: Should down-scale imeages, to a more appropriate resolution
                img = self.book.add_image(img.get('src'))
                img.set('src', img.get_src())
            else:
                img.drop_tree()
 
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

        for table in selector_match.cssselect('table'):
            table.set('style', "border: solid 1px; width: 100%;")
            table.set('width', None)
            par = table.getparent()
            par.getparent().replace(par, table)

        for td in selector_match.cssselect('td'):
            td.set('style', "border: solid 1px; width: 100%;")
            td.set('width', None)

        for hr in selector_match.cssselect('hr'):
            img_src = self.book.get_image_src('sep.png')
            
            img = lxml.html.fromstring(f'<div align="center" style="text-align:center"><img src="{img_src}" width=80%></div>')
            hr.getparent().replace(hr, img)
        return selector_match
