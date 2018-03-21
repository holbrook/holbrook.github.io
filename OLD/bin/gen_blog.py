#!/usr/bin/python
# -*- coding: utf-8 -*-
#  _   _       _ _                     _
# | | | | ___ | | |__  _ __ ___   ___ | | __
# | |_| |/ _ \| | '_ \| '__/ _ \ / _ \| |/ /
# |  _  | (_) | | |_) | | | (_) | (_) |   <
# |_| |_|\___/|_|_.__/|_|  \___/ \___/|_|\_\
# wanghaikuo@gmail.com

import yaml
import os
import codecs

JEKYLL_ROOT = '../../holbrook.github.io/_posts'
POSTS_ROOT = '../articles'

f = open('../publish/holbrook.github.io.yaml')
posts = yaml.load(f)
f.close()

here = os.path.abspath('.')

for post in posts:
    filename = os.path.basename(post)
    path = os.path.dirname(post)

    postname = filename[:filename.rfind('.')]


    meta = u''
    f = codecs.open(POSTS_ROOT + os.sep + post,'r','utf-8')
    count = 0

    for line in f:
        if line.startswith('---'):
           count += 1 
           continue
        if count == 2:
            break
        
        if count == 1:
            meta += line

       
    f.close()
    #print meta
    postinfo = yaml.load(meta)


    os.system('mkdir -p '+JEKYLL_ROOT + '/' + path)

    target = here + '/' + JEKYLL_ROOT + '/' + str(postinfo['date']) + '-' + postname + '.html' 
    cmd = 'cd '+ POSTS_ROOT + '/' + path + ' && '
    cmd += 'pandoc -s --mathjax --self-contained -N --template '+ here + '/../templates/pandoc/jekyll.post.tpl --toc '+ filename 
    cmd += ' -o ' + target 
    print cmd
    os.system(cmd)

    print 'gen '+ post + ' to \t'+ target 

     
    

