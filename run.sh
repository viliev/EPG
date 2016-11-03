#!/bin/bash -e

cd /home/hgenev/EPG/

./generate.py

git add -A
git commit -m "Regular EPG update"
git push 
