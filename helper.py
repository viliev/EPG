# -*- coding: utf8 -*-
import urllib2
import os, StringIO, gzip, urllib2
import xml.etree.ElementTree as ET
from ids import *


def log(msg):
  print "### %s" % msg
  logFile.write("%s\n" % msg)
  
logFile = open("log.txt", "w")

n = 0
xmltv = ET.Element('tv')
xmltv.set('version', '1.0')
xmltv.append(ET.Comment('Automatically generated for Kodibg.org. Used EPGs from epg.kodibg.org, github.com/txt3rob/kodi-sky-epg/,  epg.serbianforum.org'))

def extract(outFile):
  try:
    gz = gzip.GzipFile(outFile, 'rb')
    s = gz.read()
    gz.close()
    with file(outFile.replace('.tar.gz', ''), 'wb') as out:
      out.write(s)
  except Exception, er:
    log(er)

def download(epgUrl, outFile):
  try:
    if isExpired(outFile):
      log("Downloading EPG from URL %s" % (epgUrl))
      response = urllib2.urlopen(epgUrl)
      log("Server returned %s" % response.getcode())
      with open(outFile, "wb") as c:
        c.write(response.read())
    else:
      log("%s is new, download skipped!" % outFile)
  except Exception, er:
    log(er)

def isExpired(file):
  try:
    from datetime import datetime, timedelta
    if os.path.isfile(file):
      treshold = datetime.now() - timedelta(hours=24)
      modified = datetime.fromtimestamp(os.path.getmtime(file))
      if modified < treshold: #file is more than a day old
        return True
      return False
    else: #file does not exist, perhaps first run
      return True
  except Exception, er:
    log(er)
    return True
  
def parse(file_name, SHORTEN_DESC = 512):
  global n, ids, root
  local_n = n
  _ids = ids[:] #copy by value not by reference
  tree = ET.parse(file_name)
  log('Parsing file: %s' % file_name)
  w = open(file_name.replace('.xml', '-names.txt'), 'w')
  for elem in tree.iter():
    if elem.tag == 'channel':
      id = elem.attrib["id"].encode('utf-8')
      w.write(id + "\n")
      if id in _ids:
        #remove url tag to save space
        try: 
          url = elem.find('url')
          if url is not None:
            elem.remove(url)
        except Exception, er:
          log('Unable to remove <url>')
          log(er)
          
        xmltv.append(elem)
        n += 1
        ids.remove(id) #remove id so it is skipped when checking the next file
    
    if elem.tag == 'programme':
      id = elem.attrib["channel"].encode('utf-8')
      if id in _ids:
        if SHORTEN_DESC:
          desc = elem.find('desc')
          if desc is not None and desc.text is not None:
            size = len(desc.text)
            if size > SHORTEN_DESC:
              substringed = desc.text[:SHORTEN_DESC] + "..."
              desc.text = substringed
              size = len(substringed)
              
        xmltv.append(elem)
  w.close()
  d = (n - local_n)
  return d

def convert_bytes(num):
  for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
    if num < 1024.0:
      return "%3.1f %s" % (num, x)
    num /= 1024.0

