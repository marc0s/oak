# -*- coding: utf-8 -*-

# Settings file for oak

# Set the default author name for the blog
AUTHOR = 'Marcos'

# Set the blog title
BLOG_TITLE = 'marc0s.blog'

# URL prefixes
PREFIX = '' # Empty for / base path, /foo for foo base path
ARCHIVE_PREFIX = 'archive'
TAGS_PREFIX = 'tag'

# Set the path to the directory where the contents will be created
CONTENT_PATH = 'content'

# Set the extension that the sources will have
SRC_EXT = 'md'

# Set the format of the post file name
# UNUSED
POST_FILE_FORMAT = "%Y-%m-%s.html"

# Set the path to the static content directory, it will be copied as-is to OUTPUT_PATH/static
STATIC_PATH = 'static'

# Set the path where the output will be generated
OUTPUT_PATH = 'site'

# Set the path to the layouts directory, relative to the settings.py path
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
    'tag': 'tag.jinja', # the template for one tag
}

HTMLS = {
    'index': 'index.html',
    'taglist': 'tags.html',
#    'tag': '%s/%%s.html' % (TAGS_PREFIX,),
}

# Wether to generate a 'tags' index page or not (True or False)
GENERATE_TAGS = True

# This is a dict with the default options for posts, which can be overriden
# by setting the keys on the YAML header in the post .md file
POST_DEFAULTS = {
    'title': 'Post title',
    'author': AUTHOR,
    'layout': 'post',
    'tags': [],
}


