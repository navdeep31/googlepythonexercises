#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import ssl

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  file = open(filename, 'r')
  server_name = re.search(r'_(\S*)', filename).group(1)
  urls = []
  for line in file:
    match = re.search(r'GET (\S*puzzle\S*) HTTP', line)
    if match and (server_name + match.group(1)) not in urls:
      urls.append(server_name + match.group(1))
  for url in urls:
    match = re.search(r'\S*-(\w+)-(\w+).jpg', url)
    if match:
      urls = sorted(urls,key=sortUrl)
    else:
	  urls.sort()
  return urls

def sortUrl(key):
  return re.search(r'\S*-(\w+)-(\w+).jpg',key).group(2)


def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary."""
  # +++your code here+++

  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
  i=0
  html_file= open(os.path.join(dest_dir,"index.html"),"w+")
  html_file.write("<verbatim>\n<html>\n<body>\n")

  for img_url in img_urls:
    print "retrieving img"+ str(i) + " from " + img_url
    #print os.path.dirname(img_url)
    #print os.path.join(dest_dir,"img"+str(i))
    urllib.urlretrieve('http://'+img_url, os.path.join(dest_dir,"img"+str(i)))
    html_file.write('<img src="img'+str(i)+'">')
    i+=1
  html_file.write("\n</body>\n</html>")

def main():
  args = sys.argv[1:]
  ssl._create_default_https_context = ssl._create_unverified_context

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
