# -*- coding: utf8 -*-
import urllib2, shutil
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

def extract(inFile):
  try:
    outFile = inFile.replace('.gz', '')
    log("Extracting file %s to %s" % (inFile, outFile))
    gz = gzip.GzipFile(inFile, 'rb')
    s = gz.read()
    gz.close()
    with file(outFile, 'wb') as out:
      out.write(s)
    return outFile
  except Exception, er:
    log(er)
    return False

def zip(inFile, outFile):
  with open(inFile, 'rb') as f_in, gzip.open(outFile, 'wb') as f_out:
    shutil.copyfileobj(f_in, f_out)  

def download(epgUrl, outFile):
  try:
    log("Downloading EPG from URL %s" % (epgUrl))
    response = urllib2.urlopen(epgUrl)
    log("Server returned %s" % response.getcode())
    with open(outFile, "wb") as c:
      c.write(response.read())
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
  
def parse(fileName, idsFromChannelName = False, SHORTEN_DESC = 512):
  global n, ids, root
  local_n = n
  _ids = ids[:] #copy by value not by reference
  tree = ET.parse(fileName)
  log('Parsing file: %s' % fileName)
  if not os.path.isfile(fileName): 
    log("Input file not found %s " % fileName)
    return 0
  w = open(fileName.replace('.xml', '-names.txt'), 'w')
  idsMap = {}
  
  for elem in tree.iter():
    if elem.tag == 'channel':
      id = elem.attrib["id"].encode('utf-8')
      channelName = elem.find('display-name').text.encode('utf-8')
      if idsFromChannelName: #Create a list of IDs matching the channel names
        #log("id %s" % id)
        idsMap[id] = channelName
        #log(idsMap[id])
        id = channelName
        elem.attrib["id"] = channelName.decode('utf-8')
        
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
        
        try: 
          log("Added channel %s, removed from further search" % channelName)
          ids.remove(channelName) #remove id so it is skipped when checking the next file
        except Exception, er:
          log(er)
    
    #log("idsMap %s" % len(idsMap))
    #print idsMap
    #return 0
    if elem.tag == 'programme':
      id = elem.attrib["channel"].encode('utf-8')
      if idsFromChannelName:
        id = idsMap[id]
        
      if id in _ids:
        elem.attrib["channel"] = id.decode('utf-8')
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

