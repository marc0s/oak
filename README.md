# Oak

Oak is a simple static-blog generator. The goal is to have a blog backed
up by a (D)VCS and that the blog itself is all made up by static content.

## Status

Oak is already usable but lot of things are still left: testing, some 
things still need to be reviewed, more layouts will be nice, ...

## Design

The design principles are:

1. all the blog site is made up of static content, no hole
   for SQL-injection or similar,
1. version controled content, achieved now with git (but you're free to use
whatever system you want),
1. you can write your posts with your favorite $EDITOR,
1. easy syntax for the posts contents, using Markdown.

## Implementation

The implementation of oak is done around a few python classes
and libs.

There is the main package `oak` which is the responsible of
generating the blog's content and of initializing the blog
path structure.

We're using external python libraries such as Jinja2 for the 
templates and `python-markdown` for parsing the raw post files.

Git is used to version the blog contents and the whole set of
folders that are involved in the process. But this is not
managed by Oak, so you're free to use other VC system or none
at all.

## Workflow

Initially, there is one git repo (let's call it Hub) living in
the server which will serve the blog. We have to clone it
somewhere else in the server (will call it Live). Live will
pull from Hub whenever a change occurs in Hub, so new content
gets updated in the Live clone. One of the folders of the repository
is the folder that holds the public content, let's assume it's
called site/. That folder is the one which the webserver has to
publish. The Live pulls are automatically done via git hooks.

Why don't use the Live clone directly? Using the Hub repository
will allow us to make as many clones as we want, and from any of
that clones we will be able to push new content to the blog.

## Features

* Secure
* Lightweight
* Easy to write syntax: Markdown
* Code highlighting: thanks to Pygments
* Small dependency set: just Git, Markdown, Jinja2, Pygments and YAML

## Contact

If you want to collaborate with the oak development you can get in touch
with us in the #oakblog channel at irc.freenode.org. Also you can report
bugs at https://dev.tenak.net/projects/oak. 

There is also a mailing list at https://llistes.tenak.net/listinfo/oak

