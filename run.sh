#!/bin/bash -e

cd ~/EPG/
#pull recent updates
git pull

#Run the collector
cd ~/epg-collector/
./generate.py

cp ./alltv-guide.xml ~/EPG/epg.xml
cp ./alltv-guide.xml.gz ~/EPG/epg.xml.gz


#commit EPG update
cd ~/EPG/
git add -A
git commit -m "Regular EPG update"
git push
