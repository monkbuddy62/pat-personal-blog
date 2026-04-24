#!/bin/bash
set -e
python build.py
git add -A
git commit -m "${1:-update posts}"
git push
