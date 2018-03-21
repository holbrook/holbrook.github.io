#!/usr/bin/python
#  _   _       _ _                     _    
# | | | | ___ | | |__  _ __ ___   ___ | | __
# | |_| |/ _ \| | '_ \| '__/ _ \ / _ \| |/ /
# |  _  | (_) | | |_) | | | (_) | (_) |   < 
# |_| |_|\___/|_|_.__/|_|  \___/ \___/|_|\_\
# wanghaikuo@gmail.com


from optparse import OptionParser

from sys import argv, path
import os

def get_repositories(svn_root):


def main(args):
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",                 
                  help="write report to FILE", metavar="FILE")
	parser.add_option("-q", "--quiet",                 
                  action="store_false", dest="verbose", default=True,  help="don't print status messages to stdout")
	(options, args) = parser.parse_args()



if __name__ == "__main__":
	main()
