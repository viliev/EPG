#!/bin/bash -e
arg=""
if [[ $@ == "-f" ]]; then echo "Forced download!"; arg="-f"; fi

cd ~/EPG/
#pull recent updates
git pull

#Run the collector
cd ~/epg-collector/
echo "Using argument=$arg"
./generate.py ${arg}

cp ./epg.xml ~/EPG/
cd ~/EPG/

gzip < epg.xml > epg.xml.gz
gzip < epg.xml > alltv-guide.xml.gz

#cp ./epg.xml.gz ~/EPG/
#cp ./epg.xml.gz ~/EPG/alltv-guide.xml.gz


#commit EPG update
git add -A
git commit -m "Regular EPG update"
git push
