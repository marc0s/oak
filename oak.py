# -*- coding: utf-8 -*-

import sys
import os
import glob
import codecs

from optparse import OptionParser
from oak import Processor, Post
import settings

def main(argv):
    parser = OptionParser(usage="%prog [OPTIONS]", version="%prog 0.1")
    parser.add_option("-g", "--generate", action = "store_true",
                        dest = "generate", default = False,
                        help = "Generate the source for your site.")
    parser.add_option("-l", "--layout", dest = "layout", default = settings.DEFAULT_LAYOUT)
    parser.add_option("-d", "--destination", dest="destination", default = settings.OUTPUT_PATH)

    (options, args) = parser.parse_args()

    cwd = os.getcwdu()
    content = os.path.sep.join([cwd, settings.CONTENT_PATH])
    templates = os.path.sep.join([cwd, settings.LAYOUTS_PATH, options.layout])
    destination = options.destination

    S = os.path.sep

    if options.generate:
        # We have to generate lot of things here :)
        # First of all we have to render all the posts
        # At the same time (to save loops) we'll cache the different
        # tags and authors
        # Then we have to create the tags page
        # Also we have to create the index and archive pages

        tags = {} # { 'tag': [post1, post2, ..., postn], ... }
        authors = {} # {'author': [post1, post2, ..., postn], ...}
        posts = {} # {'post': metadata, ...}

        # The master Processor
        proc = Processor.Processor(templates)

        # ------ POSTS ------- 
        # Let's iterate through all posts sources and render them
        # TODO Move all those ugly print's to a logger!
        print(" * Rendering posts...")
        print(" * Using %s as source of content" % (content,))
        print(" * Using '%s' as layout name" % (options.layout,))

        for f in glob.glob("%s/*.%s" % (content,settings.SRC_EXT)):
            filename = os.path.basename(f)
            # TODO add sanity check on source filename (count of - ...)
            path = S.join([destination] + filename.split('-')[:2])
            newfilename = "%s.html" % (os.path.splitext(filename)[0],)
            destinationfile = S.join([path, newfilename])

            print(" * processing %s..." % (filename,))
            post = Post.Post(f)
            posts[filename] = post.get_metadata().__dict__()
            # cache the tags of the current post
            for t in posts[filename]['tags']:
                if t not in tags.keys():
                    tags[t] = [destinationfile]
                else:
                    tags[t].append(destinationfile)
            # cache the author of the current post
            author = posts[filename]['author']
            if author not in authors.keys():
                authors[author] = [destinationfile]
            else:
                authors[author].append(destinationfile)

            # make sure we have the final path created
            if not os.path.exists(path) or not os.path.isdir(path):
                os.makedirs(path)

            output = proc.render(settings.TEMPLATES['post'], post.__dict__())
            # TODO probably let the processor handle the writing of the output
            print(" * generating output file in %s" % (destinationfile,))
            outfile = codecs.open(destinationfile, mode='w', encoding='utf-8')
            outfile.write(output)
            outfile.close()
        # ------ TAGS INDEX ------
        # tagfile = proc.render(settings.TEMPLATES['tags'], tags)
        
        # ------ POSTS INDEX ------
        # index = proc.render(settings.TEMPLATES['index'], posts)
        print(tags)
        print(authors)
        print(posts)
if __name__ == "__main__":
    main(sys.argv[1:])

