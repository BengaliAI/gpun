#!/bin/sh
DATA_DIR="/backup2/Oscar/corpus/"
# execution
python download.py $DATA_DIR 
python words.py $DATA_DIR
# finish
echo succeded