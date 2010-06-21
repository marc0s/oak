# -*- coding: utf-8 -*-

import sys
import os
import glob
import codecs
import logging
import shutil

from optparse import OptionParser
from oak import Processor, Post, Tag

import settings


LOG_LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

def postfilepath(filename, destination):
    year, month = filename.split('-')[:2]
    newfilename = "%s.html" % (os.path.splitext(filename)[0],)
    return os.path.sep.join([destination, year, month, newfilename])

def postfileurl(filename):
    year, month = filename.split('-')[:2]
    newfilename = "%s.html" % (os.path.splitext(filename)[0],)
    postfileurl = os.path.sep.join([settings.PREFIX, year, month, newfilename])
    return postfileurl

def tagindexfilepath(destination):
    return os.path.sep.join([destination, settings.HTMLS['taglist']])

def tagindexurl():
    return os.path.sep.join([settings.PREFIX, settings.HTMLS['taglist']])

def tagfilespath(destination):
    return os.path.sep.join([destination, settings.TAGS_PREFIX])

def tagfilepath(tagname, destination):
    return os.path.sep.join([tagfilespath(destination), "%s.html" % (tagname,)])

def tagfileurl(tagname):
    return os.path.sep.join([settings.PREFIX, settings.TAGS_PREFIX, "%s.html" % (tagname,)])

def indexfilepath(destination):
    return os.path.sep.join([destination, settings.HTMLS['index']])

def writefile(filename, content):
    outfile = codecs.open(filename, mode='w', encoding='utf-8')
    outfile.write(content)
    outfile.close()

def main(argv):
    parser = OptionParser(usage="%prog [OPTIONS]", version="%prog 0.1-alpha")
    parser.add_option("-i", "--init", action="store_true", dest="init", default=False, help="Initialize the environment.")
    parser.add_option("-g", "--generate", action="store_true", dest="generate", default=False, help = "Generate the source for your site.")
    parser.add_option("-l", "--layout", dest="layout", default=settings.DEFAULT_LAYOUT, help="Set the layout to use")
    parser.add_option("-d", "--destination", dest="destination", default=settings.OUTPUT_PATH, help="Set the destination of the output")
    parser.add_option("--loglevel", dest="loglevel", default="warning", help="Set the log output level")

    (options, args) = parser.parse_args()

    cwd = os.getcwdu()
    content = os.path.sep.join([cwd, settings.CONTENT_PATH])
    templates = os.path.sep.join([cwd, settings.LAYOUTS_PATH, options.layout])
    destination = os.path.abspath(options.destination)
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

    if options.init:
        if not os.path.exists(destination):
            os.makedirs(destination)
        if not os.path.exists(content):
            os.makedirs(content)
        # TODO fix that ugly hardcoded path!
        if not os.path.exists("static"):
            os.makedirs("static")
    elif options.generate:
        # We have to generate lot of things here :)
        # First of all we have to render all the posts
        # At the same time (to save loops) we'll cache the different
        # tags and authors
        # Then we have to create the tags page
        # Also we have to create the index and archive pages
        # And last but not least, we have to copy the static content

        tags = {} # {'tagname': <Tag object>, ...} 
        authors = {} # {'author': [<Post object>, ...], ...}
        posts = [] # [<Post object>, ...] 

        # The master Processor
        proc = Processor.Processor(templates)
        # The dict passed to templates
        tpl_vars = {
            'site_path': settings.PREFIX or '/', # if there is no prefix, use / 
            'blog_title': settings.BLOG_TITLE,
        }
        # ------ POSTS ------- 
        # Let's iterate through all posts sources and render them
        logger.info("Rendering posts...")
        logger.info("Using %s as source of content" % (content,))
        logger.info("Using '%s' as layout name" % (options.layout,))

        for f in glob.glob("%s/*.%s" % (content,settings.SRC_EXT)):
            filename = os.path.basename(f)
            # TODO add sanity check on source filename (count of - ...)
            post_path = S.join([destination] + filename.split('-')[:2])
            newfilename = "%s.html" % (os.path.splitext(filename)[0],)
            logger.info("Processing %s..." % (filename,))
            post = Post.Post(f)
            post['url'] = postfileurl(newfilename)
            posts.append(post)
            # cache the tags of the current post
            for t in post['metadata']['tags']:
                if t not in tags.keys():
                    tags[t] = Tag.Tag(tag=t, url=tagfileurl(t), posts=[post])
                else:
                    tags[t]['posts'].append(post)
            # cache the author of the current post
            author = post['metadata']['author']
            if author not in authors.keys():
                authors[author] = [post]
            else:
                authors[author].append(post)

            # make sure we have the final path created
            if not os.path.exists(post_path) or not os.path.isdir(post_path):
                logger.debug("Output directory not found, creating")
                os.makedirs(post_path)
            tpl_vars.update({'post': post})
            logger.debug("tpl_vars: %s" % (tpl_vars,))
            output = proc.render(settings.TEMPLATES['post'], tpl_vars)
            logger.info("Generating output file in %s" % (postfilepath(filename,destination),))
            writefile(postfilepath(filename, destination), output)
            tpl_vars.pop('post') # remove the aded key

        # ------ TAGS INDEX ------
        if not os.path.exists(tagfilespath(destination)) or not os.path.isdir(tagfilespath(destination)):
            logger.debug("Tag files directory not found, creating")
            os.makedirs(tagfilespath(destination))
        tpl_vars.update({'tags': tags})
        tagfile = proc.render(settings.TEMPLATES['taglist'], tpl_vars)
        writefile(tagindexfilepath(destination), tagfile)
        tpl_vars.pop('tags')
        for t in tags.keys():
            tpl_vars.update({'tag': tags[t]})
            f = proc.render(settings.TEMPLATES['tag'], tpl_vars)
            logger.info("Generating tag page for %s in %s" % (t, tagfilepath(t, destination)))
            writefile(tagfilepath(t, destination), f)
            # remove added keys
            tpl_vars.pop('tag') 

        # ------ POSTS INDEX ------
        # let's sort the posts in chronological order
        posts.sort(lambda x, y: cmp(x['metadata']['pub_date'], y['metadata']['pub_date']))
        if settings.POSTS_SORT_REVERSE:
            posts.reverse()
        tpl_vars.update({'posts': posts[:settings.POSTS_COUNT]})
        index = proc.render(settings.TEMPLATES['index'], tpl_vars)
        logger.info("Generating index page at %s" % (indexfilepath(destination)),)
        writefile(indexfilepath(destination), index)
        tpl_vars.pop('posts') # remove added key

        # ------ COPY static content ------
        # TODO allow to overwrite contents
        static_dst = S.join([destination, 'static'])
        if not os.path.exists(static_dst):
            shutil.copytree(settings.STATIC_PATH, static_dst)

if __name__ == "__main__":
    main(sys.argv[1:])

