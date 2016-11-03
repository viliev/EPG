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
  {"url":"http://epg.serbianforum.org/epg.xml.gz", "outFile":"serbian-guide.xml.tar.gz"},
  #{"url":"http://epg.kodibg.org/dl.php", "outFile":"bulgarian-guide.xml.tar.gz"},
  {"url":"https://dl.dropboxusercontent.com/s/xg6c7av61p1jdoq/epg.xml.gz", "outFile":"bulgarian-guide.xml.tar.gz"}
]
  
### Logic
try:
  # Download EPGs
  for e in epgs:
    download(e["url"], e["outFile"])
    extract(e["outFile"])
  
  #Build EPG files 
  epg_files = [e["outFile"].replace('.tar.gz', '') for e in epgs]
  log("\n### Parsing started for %s files!" % len(epg_files))
  n = 0
  for f in epg_files:
    d = parse(f, SHORTEN_DESC)
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
