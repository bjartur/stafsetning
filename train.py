import csv
#from pprint import pprint
from parameters import *


# skilar þeim lyklagildispörum þar sem gildið er a.m.k. min_err_freq
def clean(correction):
    return { k: v for k, v in correction.items() if v >= Parameters.min_err_freq }

# skilar summu allra gilda í d
def dictsum(d):
    s = 0
    for v in d.values():
        s += v
    return s


def diff(typeds, corrects):
    n_err = 0
    correction = None
    if len(typeds) != len(corrects):
        return None
    for typed, correct in zip(typeds,corrects):
        if correct != typed:
            if n_err > Parameters.max_change_optical:
                return None
            else:
                n_err += 1
                correction = (typed, correct)
    return correction


def characterwise():
    similarity = {}
    with open(Parameters.training_data, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print("Finding similarity characters in:", Parameters.training_data)
        for row in reader:
            result = diff(row['Word'], row['CorrectWord'])
            if result is not None: #if neither equal nor too different
                mistake, correction = result
                if mistake not in similarity:
                    similarity[mistake] = dict()
                if correction not in similarity[mistake]:
                    similarity[mistake][correction] = 0
                similarity[mistake][correction] += 1

    # Filter out uncommon errors
    similarity = { k: clean(v) for k, v in similarity.items() if clean(v) }

    # Sort letters by how similar they are to other letters in general
    confusingness = { k: sum(v.values()) for k, v in similarity.items() }
    confusing = sorted(confusingness, key=confusingness.get, reverse=True)

    similar = { k: sorted(v, key=v.get, reverse=True) for k, v in similarity.items() }

    return confusing, similar

# if __name__ == '__main__':
#     pprint(characterwise([79,80]))
