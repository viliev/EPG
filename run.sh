#!/bin/bash -e

cd /home/hgenev/EPG/

git pull

./generate.py

git add -A
git commit -m "Regular EPG update"
git push
