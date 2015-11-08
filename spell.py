#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, collections, csv

word_frequency = {}

previous_words = {}

# def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
#     csv_reader = csv.DictReader(utf8_data, dialect=dialect, **kwargs)
#     for row in csv_reader:
#         yield [unicode(cell, 'utf-8') for cell in row]



with open('althingi_tagged/079.csv') as csvfile:
    print csvfile
    reader = csv.DictReader(csvfile)
    prev_word = ""
    for row in reader:
        if not word_frequency.get(row['Word']):
            word_frequency[row['Word']] = 1
            previous_words[row['Word']] = {}
            previous_words[row['Word']][prev_word] = 1
        else:
            word_frequency[row['Word']] += 1
            if previous_words[row['Word']].get(prev_word):
                previous_words[row['Word']][prev_word] += 1
            else:
                previous_words[row['Word']][prev_word] = 1
        prev_word = row['Word']

# for key, value in previous_words.iteritems():
#     print "word", key, value

for key, value in word_frequency.iteritems():
    print "word", key, value


def words(text): return re.findall('[a-z]+', text.lower())


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('althingi_text/079.txt').read()))

#alphabet = 'aábcdeéfghiíjklmnoópqrstuúvwxyzþæö'
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)


def known(words): return set(w for w in words if w in NWORDS)


def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
