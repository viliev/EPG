#!/bin/bash -e
arg=""
if [[ $@ == "-f" ]]; then echo "Forced download!"; arg="-f"; fi

cd ~/EPG/
#pull recent updates
#git pull

#Run the collector
cd ~/epg-collector/
echo "Using argument=$arg"
./generate.py ${arg}

cp ./alltv-guide.xml ~/EPG/
cp ./alltv-guide.xml ~/EPG/epg.xml
cp ./alltv-guide.xml.gz ~/EPG/
cp ./alltv-guide.xml.gz ~/EPG/epg.xml.gz


#commit EPG update
cd ~/EPG/
git add -A
git commit -m "Regular EPG update"
git push
