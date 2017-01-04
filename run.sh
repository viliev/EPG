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

./validate.py

cp ./epg.xml ~/EPG/
cp ./validation.json ~/EPG/
cd ~/EPG/

gzip < epg.xml > epg.xml.gz
gzip < epg.xml > alltv-guide.xml.gz


#md5sum epg.xml > checksum.txt
cut -d ' ' -f 1 <<< `md5sum epg.xml` > checksum.txt

#cp ./epg.xml.gz ~/EPG/
#cp ./epg.xml.gz ~/EPG/alltv-guide.xml.gz


#commit EPG update
echo "Commiting changes to GIT server"
git add -A
git commit -m "Regular EPG update"
echo "Pushing changes to GIT server"
git push
