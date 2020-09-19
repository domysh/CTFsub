#!/bin/sh
if test -f "stop.sh"; then
	./stop.sh
fi
rm -r g_var.json settings.json attacks/ logs/ utils/__pycache__/
