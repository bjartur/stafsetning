#Stafsetjari fyrir íslensk Alþingisskjöl

## Install editdistance
    sudo pip3 install editdistance

## Leiðrétta villur
Nokkrar villur voru í skjölunum sem þarf að leiðrétta með eftirfarandi skipun

    make known_errors.csv

## Keyra forrit
    python3 spell.py filename.csv
    
## Niðurstöður
Niðurstöður eru í skjalinu 'filename_corrected.csv'