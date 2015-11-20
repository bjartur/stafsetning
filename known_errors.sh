#!/bin/sh
cat althingi_errors/079.csv althingi_errors/080.csv >known_errors.csv
patch known_errors.csv <known_errors.diff
