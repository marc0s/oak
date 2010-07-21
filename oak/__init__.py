# -*- coding: utf-8 -*-
"""
.. module:: oak
    :platform: Unix
    :synopsys: A static blog generator

.. moduleauthor:: Marcos <marc0s@fsfe.org>

"""

import codecs
import glob
import os
import shutil
import sys

from jinja2 import Environment, FileSystemLoader

from oak.models.post import Post
from oak.models.tag import Tag
from oak.utils import copytree_, Filters
from oak.processors import processor

class Oak(object):
    """The main Oak class

    """

    logger = None
    settings = None
    posts = []
    authors = {}
    tags = {}

    def __init__(self, logger=None, settings=None):
        """Initializes the class

        The logger and the settings module are stored and the Jinja environment
        set up.

        :param logger: The logger object
        :param settings: The settings module to be used along the generation process
        :type settings: module
        """

        if logger:
            self.logger = logger
        if settings:
            self.settings = settings

        self.logger.info("Starting up...")
        # set up the Jinja environment
        # get the filters
        self.jenv = Environment(loader=FileSystemLoader(os.path.sep.join([self.settings.LAYOUTS_PATH, self.settings.DEFAULT_LAYOUT])))
        self.jenv.filters['datetimeformat'] = Filters.datetimeformat
        self.jenv.filters['longdate'] = Filters.longdate
        self.jenv.filters['shortdate'] = Filters.shortdate
        self.logger.debug("Template environment ready.")
        self.tpl_vars = {
            'blog_title': self.settings.BLOG_TITLE, 
            'links': {
                'site': self.settings.PREFIX or '/', # if there is no prefix, use /
                'taglist': os.path.sep.join([self.settings.PREFIX, self.settings.HTMLS['taglist']]),
                'archive': os.path.sep.join([self.settings.PREFIX, self.settings.HTMLS['archive']]),
                'authors': os.path.sep.join([self.settings.PREFIX, self.settings.HTMLS['authors']]),
            }
        }


    def _post_path(self, filename):
        """Calculates the final path for a post given a filename
        
        :param filename: the name of the input file
        :type filename: string

        :returns: string
        """
        self.logger.debug("_post_path:%s" % (filename,))
        year, month = filename.split('-')[:2]
        newfilename = "%s.html" % (os.path.splitext(filename)[0],)
        self.logger.debug("_post_path:%s" % (newfilename,))
        return os.path.sep.join([self.settings.OUTPUT_PATH, year, month, newfilename])

    def _tag_path(self, tagname=None):
        """Calculates the final path for a tag page given a tag name

        :param tagname: the name of the tag. If None, return just the directory where tag files are write to
        :type tagname: string

        :returns: string
        """
        if tagname:
            return os.path.sep.join([self.settings.OUTPUT_PATH, self.settings.TAGS_PREFIX, "%s.html" % (tagname,)])
        return os.path.sep.join([self.settings.OUTPUT_PATH, self.settings.TAGS_PREFIX])
    
    def _post_url(self, filename):
        """Calculates the URL of a post given a filename

        :param filename: the name of the output (generated) file
        :type filename: string

        :return: string
        """
        year, month = filename.split('-')[:2]
        newfilename = "%s.html" % (os.path.splitext(filename)[0],)
        return os.path.sep.join([self.settings.PREFIX, year, month, newfilename])

    def _tag_url(self, tagname):
        """Calculates the URL for a tag page given a tag name

        :param tagname: the name of the tag
        :type tagname: string

        :return: string
        """
        return os.path.sep.join([self.settings.PREFIX, self.settings.TAGS_PREFIX, "%s.html" % (tagname,)])

    def _index_path(self):
        """Calculates the path of the index page

        :return: string
        """
        return os.path.sep.join([self.settings.OUTPUT_PATH, self.settings.HTMLS['index']])

    def _index_url(self):
        """Calculates the URL for the index page

        :returns: string
        """
        return os.path.sep.join([self.settings.PREFIX, self.settings.HTMLS['index']])

    def _tag_index_url(self):
        """Calculates the URL for the tags index page

        :returns: string
        """
        return os.path.sep.join([self.settings.PREFIX, self.settings.HTMLS['taglist']])

    def _tag_index_path(self):
        """Calculates the PATH for the tags index page

        :returns: string
        """
        return os.path.sep.join([self.settings.OUTPUT_PATH, self.settings.HTMLS['taglist']])

    def _write_file(self, filename, content):
        """Writes content in filename.

        :param filename: the output file name
        :type filename: string

        :param content: the content to write
        :type content: string

        """
        self.logger.debug("Writing to file '%s'" % (filename,))
        if filename.find(os.path.sep): # if it's a path, check for directories
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
        outfile = codecs.open(filename, mode='w', encoding='utf-8')
        outfile.write(content)
        outfile.close()

    def _copy_statics(self):
        """Copies the satic files to the output static path.

        """
        static_path = os.path.sep.join([self.settings.OUTPUT_PATH, self.settings.STATIC_PATH])
        self.logger.debug("Using '%s' as static_path" % (static_path),)
        copytree_(self.settings.STATIC_PATH, static_path)
        tpl_static = os.path.sep.join([self.settings.LAYOUTS_PATH, self.settings.DEFAULT_LAYOUT, self.settings.STATIC_PATH])
        self.logger.debug("Using '%s' as template static path" % (tpl_static),)
        if os.path.exists(tpl_static) and os.path.isdir(tpl_static):
            copytree_(tpl_static, static_path)

    def _do_posts(self):
        """Do the posts generation.
        """
        self.logger.info("Rendering posts...")
        self.logger.info("Using %s as source of content." % (self.settings.CONTENT_PATH,))
        for f in glob.glob("%s/*.%s" % (self.settings.CONTENT_PATH,self.settings.SRC_EXT)):
            filename = os.path.basename(f)
            # TODO add sanity check on source filename (count of - ...)
            post_path = os.path.sep.join([self.settings.CONTENT_PATH] + filename.split('-')[:2])
            newfilename = "%s.html" % (os.path.splitext(filename)[0],)
            self.logger.info("Processing %s..." % (filename,))
            post = Post(f, self.settings.POST_DEFAULTS, processor.MarkdownProcessor)
            post['url'] = self._post_url(newfilename)
            self.posts.append(post)
            # cache the tags of the current post
            for t in post['metadata']['tags']:
                if t not in self.tags.keys():
                    self.tags[t] = Tag(tag=t, url=self._tag_url(t), posts=[post])
                else:
                    self.tags[t]['posts'].append(post)
            # cache the author of the current post
            author = post['metadata']['author']
            if author not in self.authors.keys():
                self.authors[author] = [post]
            else:
                self.authors[author].append(post)

            # make sure we have the final path created
            if not os.path.exists(post_path) or not os.path.isdir(post_path):
                self.logger.debug("Output directory %s not found, creating" % (post_path,))
                os.makedirs(post_path)
            self.tpl_vars.update({'post': post})
            self.logger.debug("tpl_vars: %s" % (self.tpl_vars,))
            output = self.jenv.get_template(self.settings.TEMPLATES['post']).render(self.tpl_vars)
            self.logger.info("Generating output file in %s" % (self._post_path(filename),))
            self._write_file(self._post_path(filename), output)
            self.tpl_vars.pop('post') # remove the aded key

    def _do_tag(self, tag):
        """Create the page for the tag 'tag'
        """
        self.tpl_vars.update({'tag': tag})
        output = self.jenv.get_template(self.settings.TEMPLATES['tag']).render(self.tpl_vars)
        self.logger.info("Generating tag page for %s in %s" % (tag['tag'], self._tag_path(tag['tag'])))
        self._write_file(self._tag_path(tag['tag']), output)
        # remove added keys
        self.tpl_vars.pop('tag') 

    def _do_tags(self):
        """Do the tags index page
        """
        if not os.path.exists(self._tag_path()) or not os.path.isdir(self._tag_path()):
            self.logger.debug("Tag files directory %s not found, creating" % (self._tag_path(),))
            os.makedirs(self._tag_path())
        self.tpl_vars.update({'tags': self.tags})
        output = self.jenv.get_template(self.settings.TEMPLATES['taglist']).render(self.tpl_vars)
        self._write_file(self._tag_index_path(), output)
        self.tpl_vars.pop('tags')
        for t in self.tags.keys():
            self._do_tag(self.tags[t])

    def _do_index(self):
        # ------ POSTS INDEX ------
        # let's sort the posts in chronological order
        self.posts.sort(lambda x, y: cmp(x['metadata']['pub_date'], y['metadata']['pub_date']))
        if self.settings.POSTS_SORT_REVERSE:
            self.posts.reverse()
        self.tpl_vars.update({'posts': self.posts[:self.settings.POSTS_COUNT]})
        self.logger.info("Generating index page at %s" % (self._index_path(),))
        output = self.jenv.get_template(self.settings.TEMPLATES['index']).render(self.tpl_vars)
        self._write_file(self._index_path(), output)
 
    def generate(self):
        """Generates the HTML files to be published.

        :raises: MarkupError, RenderError
        """
        self.logger.info("Using '%s' as layout path." % (self.settings.DEFAULT_LAYOUT,))
    
        posts = []
        tags = {}
        authors = {}

        self._do_posts()
        self._do_tags()
        self._copy_statics()
        self._do_index()

