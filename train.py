import csv
from pprint import pprint

min_err_freq = 8

character_freq = {}

def clean(correction):
    return { k: v for k, v in correction.items() if v >= min_err_freq }

def dictsum(d):
    s = 0
    for v in d.values():
        s += v
    return s

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
    similarity = {}
    for i in csvs:
        if i not in missing:
            prefix = 'althingi_errors/'
            if i < 100:
                filename = prefix + '0' + str(i) + '.csv'
            else:
                filename = prefix + str(i) + '.csv'
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                print("Finding similarity characters in althingi error nr: ", i)
                prev_word = ""
                for row in reader:
                    result = diff(row['Word'], row['CorrectWord'])
                    if result is not None: #if neither equal nor too different
                        mistake, correction = result
                        if mistake not in similarity:
                            similarity[mistake] = dict()
                        if correction not in similarity[mistake]:
                            similarity[mistake][correction] = 0
                        similarity[mistake][correction] += 1                 # e.g.

    # Filter out uncommon errors
    similarity = { k: clean(v) for k, v in similarity.items() if clean(v) }    # { 'l': { 'i': 255, '1': 50 }, ',': {'.':200} }
    

    # Sort letters by how similar they are to other letters in general
    confusingness = { k: sum(v.values()) for k, v in similarity.items() }      # { 'l': 305 }
    confusing = sorted(confusingness, key=confusingness.get, reverse=True)           # [ 'l', ',' ]

    similar = { k: sorted(v, key=v.get, reverse=True) for k, v in similarity.items() } # { 'l': ['i','1'] }

    return confusing, similar

if __name__ == '__main__':
    pprint(characterwise([79,80]))
