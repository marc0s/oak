# -*- coding: utf-8 -*-

import sys
import os
import glob
import codecs
import logging

from optparse import OptionParser
from oak import Processor, Post

import settings


LOG_LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

# TODO FIX paths when -d option is supplied (remove os.getcwdu())

def postfilepath(filename):
    year, month = filename.split('-')[:2]
    newfilename = "%s.html" % (os.path.splitext(filename)[0],)
    return os.path.sep.join([os.getcwdu(), settings.STATIC_PATH, year, month, newfilename])

def postfileurl(filename):
    year, month = filename.split('-')[:2]
    newfilename = "%s.html" % (os.path.splitext(filename)[0],)
    postfileurl = os.path.sep.join([settings.PREFIX, year, month, newfilename])
    return postfileurl

def tagfilepath(tagname):
    return os.path.sep.join([os.getcwdu(), settings.STATIC_PATH, settings.TAGS_PREFIX, "%s.html" % (tagname,)])

def tagfileurl(tagname):
    return os.path.sep.join([settings.PREFIX, settings.TAGS_PREFIX, "%s" % (tagname,)])

def writefile(filename, content):
    outfile = codecs.open(filename, mode='w', encoding='utf-8')
    outfile.write(content)
    outfile.close()

def main(argv):
    parser = OptionParser(usage="%prog [OPTIONS]", version="%prog 0.1")
    parser.add_option("-g", "--generate", action = "store_true", dest = "generate", default = False, help = "Generate the source for your site.")
    parser.add_option("-l", "--layout", dest = "layout", default = settings.DEFAULT_LAYOUT, help="Set the layout to use")
    parser.add_option("-d", "--destination", dest="destination", default = settings.OUTPUT_PATH, help="Set the destination of the output")
    parser.add_option("--loglevel", dest="loglevel", default="warning", help="Set the log output level")

    (options, args) = parser.parse_args()

    cwd = os.getcwdu()
    content = os.path.sep.join([cwd, settings.CONTENT_PATH])
    templates = os.path.sep.join([cwd, settings.LAYOUTS_PATH, options.layout])
    destination = options.destination
    loglevel = LOG_LEVELS[options.loglevel]

    # set up logging
    logger = logging.getLogger('oak')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
    ch.setFormatter(formatter)
    ch.setLevel(loglevel)
    logger.addHandler(ch)
    logger.setLevel(loglevel)

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
        posts = [] # [Post1, Post2, ..., PostN] 

        # The master Processor
        proc = Processor.Processor(templates)

        # ------ POSTS ------- 
        # Let's iterate through all posts sources and render them
        logger.info("Rendering posts...")
        logger.info("Using %s as source of content" % (content,))
        logger.info("Using '%s' as layout name" % (options.layout,))

        for f in glob.glob("%s/*.%s" % (content,settings.SRC_EXT)):
            filename = os.path.basename(f)
            # TODO add sanity check on source filename (count of - ...)
            path = S.join([destination] + filename.split('-')[:2])
            newfilename = "%s.html" % (os.path.splitext(filename)[0],)
            logger.info("Processing %s..." % (filename,))
            post = Post.Post(f)
            post.set_url(postfileurl(newfilename))
            posts.append(post)
            # posts[filename] = post.get_metadata().__dict__()
            # cache the tags of the current post
            for t in post.get_metadata().__dict__()['tags']:
                if t not in tags.keys():
                    tags[t] = [postfileurl(newfilename)]
                else:
                    tags[t].append(postfileurl(newfilename))
            # cache the author of the current post
            author = post.get_metadata().__dict__()['author']
            if author not in authors.keys():
                authors[author] = [postfileurl(newfilename)]
            else:
                authors[author].append(postfileurl(newfilename))

            # make sure we have the final path created
            if not os.path.exists(path) or not os.path.isdir(path):
                logger.debug("Output directory not found, creating")
                os.makedirs(path)
            output = proc.render(settings.TEMPLATES['post'], post.__dict__())
            logger.info("Generating output file in %s" % (postfilepath(filename),))
            writefile(postfilepath(filename), output)
        # ------ TAGS INDEX ------
        tagfile = proc.render(settings.TEMPLATES['taglist'], {'tags': tags.keys()})
        writefile(settings.HTMLS['taglist'], tagfile)
        for t in tags.keys():
            f = proc.render(settings.TEMPLATES['tag'], {'tag': t, 'posts': tags[t]})
            logger.info("Generating tag page for %s in %s" % (t, tagfilepath(t)))
            writefile(tagfilepath(t), f)
        # ------ POSTS INDEX ------
        # index = proc.render(settings.TEMPLATES['index'], posts)
        logger.debug("Read tags: %s" % (tags,))
        logger.debug("Read authors: %s" % (authors,))
        logger.debug("Read posts: %s" % (posts,))

if __name__ == "__main__":
    main(sys.argv[1:])

