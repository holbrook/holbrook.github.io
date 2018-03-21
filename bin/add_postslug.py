#!/usr/bin/python
# -*- coding: utf-8 -*-
#  _   _       _ _                     _
# | | | | ___ | | |__  _ __ ___   ___ | | __
# | |_| |/ _ \| | '_ \| '__/ _ \ / _ \| |/ /
# |  _  | (_) | | |_) | | | (_) | (_) |   <
# |_| |_|\___/|_|_.__/|_|  \___/ \___/|_|\_\
# wanghaikuo@gmail.com

import os
import codecs

POSTS_ROOT = '../source/_posts'

def process(path, filename):
    src = os.path.join(path,filename)
    print(src)
    lines = []
    with codecs.open(src,'r',encoding='utf8') as f:
        for line in f:
            lines.append(line)
        f.close()
    slug = u'postslug: '+filename[:-3]+'\n'
    lines.insert(2,slug)
    #print(lines[:5])
    with codecs.open(src,'w',encoding='utf8') as f:
        f.writelines(lines)
        f.close()
    
def traval(path):
    for parent,dirs,files in os.walk(path):
        for dirname in dirs:
            traval(dirname)
        for filename in files:
            if(filename.endswith('.md')):
                process(parent, filename)

traval(POSTS_ROOT)