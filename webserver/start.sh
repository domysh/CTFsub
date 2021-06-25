#!/bin/sh
#https://schedule.readthedocs.io/en/stable/
uwsgi --http 0.0.0.0:9999 --thunder-lock --static-map /static=/execute/static --enable-threads -w app:app 