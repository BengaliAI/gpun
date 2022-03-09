#!/bin/sh
DATA_DIR="/backup/Oscar/corpus/"
# execution
python download.py $DATA_DIR 
python words.py $DATA_DIR
# finish
echo succeded