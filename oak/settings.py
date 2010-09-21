# -*- coding: utf-8 -*-

# Settings file for oak

# Set the default author name for the blog
AUTHOR = 'your name will be fine'
EMAIL = 'your email' # not required

# Set the blog title
BLOG_TITLE = 'your blog title'

# Set the URL of your blog, only used when generating the Atom feed. Without 'http://'.
BLOG_DOMAIN = 'example.com'
# Put 'blog' if your blog will be in http://example.com/blog and let it empty if your blog will be in http://example.com/
BLOG_PREFIX = ''

# The blog's contents license, you can include HTML
BLOG_LICENSE_TEXT = 'The contents of this site are put on the <a href="http://creativecommons.org/publicdomain/zero/1.0/">public domain</a>'

# URL prefixes
# Put / if your blog will be in http://example.com/ or /blog if it will be in http://example.com/blog and so on
ARCHIVE_PREFIX = 'archive'
TAGS_PREFIX = 'tag'
AUTHORS_PREFIX = 'author'

# Set the path to the directory where the contents will be created
CONTENT_PATH = 'content'

# Set the extension that the sources will have
SRC_EXT = 'md'

# Set the format of the post file name, now posts MUST have the format below!
# UNUSED, changing it has no effect!!
POST_FILE_FORMAT = "%Y-%m-%s.html"

# Set the path to the static content directory, it will be copied as-is to OUTPUT_PATH/static
# It will serve as the name for layout-relative static files (i.e.: layouts/foo/static)
STATIC_PATH = 'static'

# Set the path where the output will be generated
OUTPUT_PATH = 'site'

# Set the path to the layouts directory, the default is OK if you are using the installed oak package
# Use an ABSOLUTE path if you want to point a custom location
LAYOUTS_PATH = 'layouts'

# Set the name of the default layout
DEFAULT_LAYOUT = 'default'

# Set how many posts will be shown in the frontpage, set it to None to show them all
POSTS_COUNT = 10

# By default, posts are sort from older to newer, set to True to invert this behaviour (newer first)
POSTS_SORT_REVERSE = True

# The names of the templates
TEMPLATES = {
    '*': 'base.jinja', # for unknown page types
    'index': 'index.jinja', # the template will receive a list with the last N links to individual pages
    'archive': 'archive.jinja', # the template will receive a full list of individual pages
    'post': 'post.jinja', # the template will receive ...
    'taglist': 'tags.jinja', # the template will receive a list of tags
    'authorlist': 'authors.jinja', # the template will receive a list of authors
    'tag': 'tag.jinja', # the template for one tag
    'author': 'author.jinja', # the template for one author
    'feed': 'atom.jinja', # the template for the atom feed
}

HTMLS = {
    'index': 'index.html',
    'taglist': 'tags.html',
    'archive': 'archive.html',
    'authorlist': 'authors.html',
    'feed': 'atom.xml',
    'css': 'static/css/main.css',
}

# Wether to generate a 'tags' index page or not (True or False)
# Still not used, tag page is always generated
GENERATE_TAGS = True

# Wether to generate an 'atom.xml' feed or not (True or False)
GENERATE_FEED = True

# This is a dict with the default options for posts, which can be overriden
# by setting the keys on the YAML header in the post .md file
POST_DEFAULTS = {
    'title': 'Post title',
    'author': AUTHOR,
    'layout': 'post',
    'tags': [],
}

