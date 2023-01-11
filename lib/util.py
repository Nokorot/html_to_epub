import lxml.html
from urllib import parse
from urllib.request import urlopen, Request
import os, logging, hashlib

class Network:
    def __init__():
        pass    

    @staticmethod
    def clean_url(url):
        url = parse.urlsplit(url)
        url = list(url)
        url[2] = parse.quote(url[2])
        url = parse.urlunsplit(url)

        return url

    @staticmethod
    def cache_filename(cache_dir, url):
        return os.path.join(cache_dir, hashlib.md5(url.encode('utf-8')).hexdigest()+'.html')

    @staticmethod
    def load_and_cache_html(url, cache_filename):
        
        print(f"Load '{url}'");


        if not os.path.isfile(cache_filename):
            logging.getLogger().debug('Cache miss - Downloading ' + url + ' to ' + cache_filename)
            
            hdrs = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}
            req = Request(url, headers=hdrs)
    
            response = urlopen(req)
            content = response.read().decode('utf-8', 'ignore')
            response.close()

            with open(cache_filename, 'w') as f:
                f.write(content)

        logging.getLogger().debug('Loading html dom from ' + cache_filename)

        with open(cache_filename, 'r') as f:
            return lxml.html.fromstring(f.read())
