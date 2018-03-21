#!/usr/bin/python
# -*- coding: utf-8 -*-

#  _   _       _ _                     _
# | | | | ___ | | |__  _ __ ___   ___ | | __
# | |_| |/ _ \| | '_ \| '__/ _ \ / _ \| |/ /
# |  _  | (_) | | |_) | | | (_) | (_) |   <
# |_| |_|\___/|_|_.__/|_|  \___/ \___/|_|\_\
# wanghaikuo@gmail.com

import os
import logging
import json
import codecs
from xlrd import open_workbook
import lxml.etree



if __name__ == '__main__':
    print 'abc'
    workbook = open_workbook('./测试数据模板-宁泉.xlsx')

    print workbook

    for st in workbook.sheets():
        print st.name
