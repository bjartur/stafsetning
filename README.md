#Stafsetjari fyrir íslensk Alþingisskjöl

##Gögn
Forritið þarfnast skjölin 'althingi_errors/079.csv' og 'althingi_errors/080.csv'


## Install editdistance
    sudo pip3 install editdistance

## Leiðrétta villur í gögnum með því að keyra skipun
    make known_errors.csv
    
## Slóð á skjali sem skal villuleita
Slóðina skal skrifa í aðra línu í parameters.py

## Keyra forrit
    python3 spell.py
    
## Niðurstöður
Forritið býr til skjal sem heitir results.csv sem inniheldur leiðréttingar