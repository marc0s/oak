# Quickstart for oak

Oak is already available as a python package, installable with `pip`. I 
recommend you to test it on a `virtualenv` before polluting your system
with packages you probably won't use anymore. You got warned :)

## Setup

  $ pip install oak

## Creating the blog and its contents

  $ cd ~/blog
  $ oak-admin.py --init=blogname

Now some directories will be created and you're ready to write your
posts under `content/`. See below for the files format.

Also you may want to edit the `settings.py` file to fit your needs. The
defaults should be OK for testing it.

You can now generate the files to be published by yor websever of choice:

  $ cd ~/blog/blogname
  $ python manage.py -g

Now you have the HTML files under `site/` ready to be served.

## Posts files format

The posts files contains a YAML header with the posts' metadata, the file
*must* start with that header. A sample header can be:

  ---
    title: 'My post'
    author: 'your name'
    pub_date: 2010-07-22 21:20:00
    tags: ['oak', 'test']
  ---

And the content, in Markdown format, should follow.

By now, the name of the files containing posts *must* follow the pattern
`YYYY-MM-post_title_or_something.md`. Eventually this restriction will be
removed and you'll be able to name them as you want.

