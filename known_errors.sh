#!/bin/sh
cat althingi_errors/079.csv althingi_errors/080.csv >known_errors.csv
patch -u known_errors.csv <known_errors.diff
