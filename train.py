import csv
from pprint import pprint

min_err_freq = 8

character_freq = {}

def clean(correction):
    return {k: v for k, v in correction.items() if v >= min_err_freq}


def count(character):
        if character not in character_freq:
            character_freq[character] = 0
        character_freq[character] += 1

def diff(typeds, corrects):
    n_err = 0
    correction = None
    if len(typeds) != len(corrects):
        return None
    for typed, correct in zip(typeds,corrects):
        count(typed); count(correct)
        if correct != typed:
            if n_err > 0:
                return None
            else:
                n_err += 1
                correction = (typed, correct)
    return correction

missing = [83, 86, 87, 88, 98, 104, 109]

def characterwise(csvs):
    similar = {}
    for i in csvs:
        if i not in missing:
            prefix = 'althingi_errors/'
            if i < 100:
                filename = prefix + '0' + str(i) + '.csv'
            else:
                filename = prefix + str(i) + '.csv'
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                print("Finding similar characters in althingi error nr: ", i)
                prev_word = ""
                for row in reader:
                    result = diff(row['Word'], row['CorrectWord'])
                    if result is not None: #if neither equal nor too different
                        mistake, correction = result
                        if mistake not in similar:
                            similar[mistake] = dict()
                        if correction not in similar[mistake]:
                            similar[mistake][correction] = 0
                        similar[mistake][correction] += 1
    similar = {k: clean(v) for k, v in similar.items() if clean(v)}
    return similar

if __name__ == '__main__':
    pprint(characterwise([79,80]))
