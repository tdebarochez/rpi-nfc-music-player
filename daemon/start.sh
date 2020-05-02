#!/bin/sh -e

export DISPLAY=:0
. .env/bin/activate
python main.py
