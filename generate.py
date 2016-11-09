#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import xml.etree.ElementTree as ET
from ids import *
from helper import *

### OPTIONS
SHORTEN_DESC = 512             # Set False to disable
OUTPUT_XML = 'alltv-guide.xml' # Output XML name

### URLs and output files
epgs = [
  {"url":"http://epg.serbianforum.org/epg.xml.gz", "outFile":"serbian-guide.xml.gz"},
  {"url":"http://epg.kodibg.org/dl.php", "outFile":"bulgarian-guide.xml.gz"},
  #{"url":"https://dl.dropboxusercontent.com/s/xg6c7av61p1jdoq/epg.xml.gz", "outFile":"bulgarian-guide.xml.gz"},
  {"url":"http://www.teleguide.info/download/new3/xmltv.xml.gz", "outFile":"russian-guide.xml.gz"},
]

epgFiles = []

### Logic
try:
  # Download EPGs
  for e in epgs:
    out = e["outFile"]
    
    if isExpired(out):
      download(e["url"], out)
    else:
      log("%s is new, download skipped!" % out)
    xmlName = extractName(out)
    if xmlName:
      epgFiles.append(xmlName)
  #Build EPG files 
  log("\n### Parsing started for %s files!" % len(epgFiles))
  n = 0
  for f in epgFiles:
    if 'russian' in f: #Get ids from <channel-name> tag in XMLTV
      d = parse(f, True) 
    else:
      d = parse(f)
    log("Extracted %s channels" % d)
    n += d
  
  #zip epg file
  log("Zipping XML file to %s" % OUTPUT_XML + ".gz")
  zip(OUTPUT_XML, OUTPUT_XML + ".gz")
  
except KeyboardInterrupt:
  log('EPG generation interrupted by user!')
except Exception, er:
  import traceback
  log(traceback.print_exc())

### Save the new EPG
tree = ET.ElementTree(xmltv)
tree.write(OUTPUT_XML, encoding="UTF-8", xml_declaration=True)

file_info = os.stat(OUTPUT_XML)
log("%s channels saved in file %s (%s)" % (n, OUTPUT_XML, convert_bytes(file_info.st_size)))
logFile.close()
