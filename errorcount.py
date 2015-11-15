import csv
from sys import argv
from os.path import sep as slash

missing = [83, 86, 87, 88, 98, 104, 109]

# Notkun: hlutfoll = villuhlutfoll(folderpath)
# Fyrir: folderpath er slóðin að althingi_errors möppunni
# Eftir:  hlutfoll er dictionary af hlutfallslegum fjölda villna í althingi_errors skránum.
#       hlutfoll[79] gefur hlutfall villna í 079.csv, hlutfoll[110] gefur hlutfall villna í 110.csv 
#       Meðalfjöldi villna hefur líka verið skrifaður út
#       hlutfall = fjöldi rangra orða / fjöldi orða

def villuhlutfoll(folder, files):
    
    villuhlutfoll = []

    for i in files:

        with open(folder + slash + '0' + str(i) + '.csv', encoding = 'utf-8') as errorfile:
            reader = csv.reader(errorfile)
            nerrors = 0
            nrow = 0
            villuradir = []
            for row in reader:
                # það eru nerrors villur í fyrstu nrow röðunum í errorfile og þær eru í villuradir[0..nerrors]
                if nrow > 0 and (row[0]!=row[3]): # sleppa að telja headerinn
                    nerrors += 1
                    villuradir.append(nrow)
                nrow += 1
            villuhlutfoll.append(nerrors/nrow)

    for i in files:
    
        with open(folder + slash + '0' + str(i) + '.csv', encoding = 'utf-8') as errorfile:
            reader = csv.reader(errorfile)
            nerrors = 0
            nrow = 0
            villuradir = []
            for row in reader:
                # það eru nerrors villur í fyrstu nrow röðunum í errorfile og þær eru í villuradir[0..nerrors]
                if nrow > 0 and (row[0]!=row[3]): # sleppa að telja headerinn
                    nerrors += 1
                    villuradir.append(nrow)
                nrow += 1
            villuhlutfoll.append(nerrors/nrow)

    j = 0
    dicto = dict()

    for i in files:
        dicto[i] = villuhlutfoll[j]
        j += 1
        
    return dicto

if __name__ == '__main__':
	if len(argv) <= 1:
		a = 79
	else:
		a = argv[1]
	if len(argv) <= 2:
		b = 81
	else:
		b = argv[2]
	if len(argv) <= 3:
		foldername = 'althingi_errors'
	else:
		foldername = argv[3]

	files = list(filter(lambda filename: filename not in missing, range(a,b+1)))
	hlutfall = villuhlutfoll(foldername, files) #dict
	hlutfoll = hlutfall.values() #list
	
	for filename in files:
		print("Villutíðni í skrá #{:d}\t{:.2%}".format(filename, hlutfall[filename]), sep='\t')
	print("-"*10)
	print("Villutíðni (meðaltal):\t{:.2%}".format(sum(hlutfoll)/len(hlutfoll)))
