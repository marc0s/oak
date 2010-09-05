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
        self.jenv.filters['isodate'] = Filters.isodate
        self.logger.debug("Template environment ready.")
        self.tpl_vars = {
            'blog': {
                'title': self.settings.BLOG_TITLE,
                'url': self.settings.BLOG_URL,
                'id': "%s%s%s" % (self.settings.BLOG_URL, os.path.sep, "atom.xml"),
                'last_updated': None, # Will be updated when reading posts.
                'author': self.settings.AUTHOR,
                'email': self.settings.EMAIL,
            },
            'license_text': self.settings.BLOG_LICENSE_TEXT,
            'links': {
                'site': self.settings.PREFIX or '/', # if there is no prefix, use /
                'taglist': os.path.sep.join([self.settings.PREFIX, self.settings.HTMLS['taglist']]),
                'archive': os.path.sep.join([self.settings.PREFIX, self.settings.HTMLS['archive']]),
                'authors': os.path.sep.join([self.settings.PREFIX, self.settings.HTMLS['authors']]),
                'feed': os.path.sep.join([self.settings.BLOG_URL, self.settings.HTMLS['feed']]),
            }
        }


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

    def _feed_path(self):
        """Calculates the PATH for the atom.xml feed

        :returns: string
        """
        return os.path.sep.join([self.settings.OUTPUT_PATH, 'atom.xml'])

    def _archive_path(self):
        """Calculates the PATH for the archive page

        :returns: string
        """
        return os.path.sep.join([self.settings.OUTPUT_PATH, self.settings.HTMLS['archive']])

    def _archive_url(self):
        return os.path.sep.join([self.settings.PREFIX, self.settings.HTMLS['archive']])
        
    def _write_file(self, filename, content):
        """Writes content in filename.

        :param filename: the output file name
        :type filename: string

        :param content: the content to write
        :type content: string

        """
        self.logger.debug("Writing to file '%s'" % (filename,))
        if filename.count(os.path.sep): # if it's a path, check for directories
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
            self.logger.info("Processing %s..." % (f,))
            post = Post(f, self.settings, processor.MarkdownProcessor)
            self.posts.append(post)
            # cache the tags of the current post
            for t in post['metadata']['tags']:
                if t not in self.tags.keys():
                    self.tags[t] = Tag(tag=t, settings=self.settings, posts=[post])
                else:
                    self.tags[t]['posts'].append(post)
            # cache the author of the current post
            author = post['metadata']['author']
            if author not in self.authors.keys():
                self.authors[author] = [post]
            else:
                self.authors[author].append(post)

            # make sure we have the final path created
            if not os.path.exists(os.path.dirname(post['output_path'])) or not os.path.isdir(os.path.dirname(post['output_path'])):
                self.logger.debug("Output directory %s not found, creating" % (os.path.dirname(post['output_path']),))
                os.makedirs(os.path.dirname(post['output_path']))

            self.tpl_vars.update({'post': post})
            self.logger.debug("tpl_vars: %s" % (self.tpl_vars,))
            output = self.jenv.get_template(self.settings.TEMPLATES['post']).render(self.tpl_vars)
            self.logger.info("Generating output file in %s" % (post['output_path'],))
            self._write_file(post['output_path'], output)
            self.tpl_vars.pop('post') # remove the aded key

    def _do_tag(self, tag):
        """Create the page for the tag 'tag'
        """
        self.tpl_vars.update({'tag': tag})
        output = self.jenv.get_template(self.settings.TEMPLATES['tag']).render(self.tpl_vars)
        self.logger.info("Generating tag page for %s in %s" % (tag['tag'], tag['path']))
        self._write_file(tag['path'], output)
        # remove added keys
        self.tpl_vars.pop('tag') 

    def _do_tags(self):
        """Do the tags index page
        """
        tags_dir = os.path.sep.join([self.settings.OUTPUT_PATH, self.settings.TAGS_PREFIX]) 
        if not os.path.exists(tags_dir) or not os.path.isdir(tags_dir):
            self.logger.debug("Tag files directory %s not found, creating" % (tags_dir,))
            os.makedirs(tags_dir)
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
        # Update the blog.last_updated key for self.tpl_vars
        self.tpl_vars['blog']['last_updated'] = self.posts[0]['metadata']['pub_date']
        if self.settings.POSTS_SORT_REVERSE:
            self.posts.reverse()
        self.tpl_vars.update({'posts': self.posts[:self.settings.POSTS_COUNT]})
        self.logger.info("Generating index page at %s" % (self._index_path(),))
        output = self.jenv.get_template(self.settings.TEMPLATES['index']).render(self.tpl_vars)
        self._write_file(self._index_path(), output)
        self.tpl_vars.pop('posts')

    def _do_archive(self):
        self.tpl_vars.update({'posts': self.posts[:]})
        self.logger.info("Generating archive page at %s " % (self._archive_path(),))
        output = self.jenv.get_template(self.settings.TEMPLATES['archive']).render(self.tpl_vars)
        self._write_file(self._archive_path(), output)
        self.tpl_vars.pop('posts')

    def _do_feed(self):
        """Generates an Atom feed of the blog posts

        """
        self.tpl_vars.update({'posts': self.posts})
        self.logger.info("Generating atom.xml at %s" % (self._feed_path(),))
        output = self.jenv.get_template(self.settings.TEMPLATES['feed']).render(self.tpl_vars)
        self._write_file(self._feed_path(), output)
        self.tpl_vars.pop('posts')
        self.logger.info("atom.xml file generated.")

    def generate(self):
        """Generates the HTML files to be published.

        :raises: MarkupError, RenderError
        """
        self.logger.info("Using '%s' as layout path." % (self.settings.DEFAULT_LAYOUT,))

        self._do_posts()
        self._do_tags()
        self._copy_statics()
        self._do_index()
        # the feed MUST be done after the index
        if self.settings.GENERATE_FEED:
            self._do_feed()
        self._do_archive()

