#Stafsetjari fyrir íslensk Alþingisskjöl

##Gögn
Forritið þarfnast skjölin 'althingi_errors/079.csv' og 'althingi_errors/080.csv'


## Install editdistance
    sudo pip3 install editdistance

## Leiðrétta villur í gögnum með því að keyra skipun
    make known_errors.csv

## Keyra forrit
    python3 spell.py filename.csv
    
## Niðurstöður
Niðurstöður eru í skjalinu filename_corrected.csv