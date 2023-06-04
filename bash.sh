#!/bin/bash

python detect.py --video video.mkv --csv coordinates.csv
python center.py --video video.mkv
python diff.py --video video.mkv

