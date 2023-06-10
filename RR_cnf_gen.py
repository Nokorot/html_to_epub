#!/usr/bin/python3

import sys, os, optparse

from pprint import pprint

from ruamel.yaml import YAML

__description = '''
    A simple program
'''

from html_to_epub.util import Network

from lxml.cssselect import CSSSelector

cache = "./cache/RR"

def first_match(tree, css_selector):
    matches = CSSSelector(css_selector)(tree)
    return matches[0]

def foldername_from_title(title):
    wrds = title.split(' ')
    return ''.join(map(lambda wd: wd[0].upper() + wd[1:], wrds))

def main(options, args):
    url = args[0]
    ignoe_cache = False

    out_file = './bookVars.sh'
    generate_script = "./books/RR_Template/gen_RR_book.sh"
    download_script = "./html_to_epub-cli.py"

    base_url = "https://www.royalroad.com"
    
    cache_filename = Network.cache_filename(cache, url)
    tree = Network.load_and_cache_html(url, cache_filename, ignoe_cache)

    result = {}
    result['title']  = first_match(tree, "div.fic-header h1").text;
    result['author'] = first_match(tree, "div.fic-header h4 a").text;
    result['cover']  = first_match(tree, "div.fic-header img").get('src').split('?')[0];
    result['entry']  = base_url + first_match(tree, "div.portlet table a").get('href').split('?')[0];
    result['foldername'] = foldername_from_title(result['title'])

    with open(out_file, 'w') as fp:
        fp.write("export       TITLE='\"%s\"'\n" % result["title"]);
        fp.write("export  FOLDERNAME='%s'\n" % result["foldername"]);
        fp.write("export      AUTHOR='%s'\n" % result["author"]);
        fp.write("export COVER_IMAGE='%s'\n" % result["cover"]);
        fp.write("export ENTRY_POINT='%s'\n" % result["entry"]);

    os.system("nvim '%s'" % out_file)

    ## THIS IS VERY MUCH A HACK!!
    with open(out_file, 'r') as f:
        for l in f:
            if "FOLDERNAME" in l:
                result['foldername'] = eval(l.split("=")[1])
                break;
        else:
            sys.stderr.write('ERROR: FOLDERNAME not found\n')

    while os.path.exists('./books/%s' % result['foldername']):
        # Optional: Add a delay before checking again
        ## TODO: This should really be a check, of wheter the input url has been used to genereate before.
        if input("The foldername already, do you want to change it and try agian? [y/N]: ")[0].lower() != 'y':
            return

        os.system("nvim '%s'" % out_file)

        ## THIS IS VERY MUCH A HACK!!
        with open(out_file, 'r') as f:
            for l in f:
                if "FOLDERNAME" in l:
                    result['foldername'] = eval(l.split("=")[1])
                break;
            else:
                sys.stderr.write('ERROR: FOLDERNAME not found\n')

    
    if not options.generate and input("Generate? [y/N]: ")[0].lower() != 'y':
        return

    os.system("%s --config '%s'" % (generate_script, out_file))
    

    with open("RR_List.lst", "a") as f:
        f.write("books/%s\n" % result['foldername'])

    if options.not_download or \
            (not options.download and input("Download? [y/N]: ")[0].lower() != 'y'):
        return

    os.system("%s --config './books/%s/config.yaml'" % (download_script, result['foldername']))


    # yaml = YAML()
    # yaml.indent(mapping=ind, sequence=ind, offset=bsi)
    # with open(out_file, 'w') as fp:
    #     yaml.dump(restult, fp)

    # restult['foldername'] = restult['title'].

if __name__ == "__main__":
    usage = "{1} [options] <arg1>"
    parser = optparse.OptionParser(usage = usage, description=__description)

    # parser.add_option('--config', dest='config', help='config file')
    parser.add_option('-g', '--genereate', dest='generate', default=False, action='store_true', help='Automatically generate the config, without conformation')
    parser.add_option('-d', '--download', dest='download', default=False, action='store_true', help='Automatically download, without conformation')
    parser.add_option('-n', '--not-download', dest='not_download', default=False, action='store_true', help='Automatically do not download')

    (options, args) = parser.parse_args()

    err = sys.stderr
    if len(args) < 1:
       err.write('ERROR: Not enough arguments!\n');
       err.write('use -h for more infromation.\n')
       sys.exit(1)
    
    # Loop?
    print(args)
    main(options, args)

