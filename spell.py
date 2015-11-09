#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, collections, csv, editdistance

word_frequency = {}
following_word = {}

# def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
#     csv_reader = csv.DictReader(utf8_data, dialect=dialect, **kwargs)
#     for row in csv_reader:
#         yield [unicode(cell, 'utf-8') for cell in row]

def missing(i):
    if i in [83, 98, 109, 111]:
        return True
    else:
        return False


def create_dicts():
    #for i in range(79,136):
    for j in range(79,80):
        i = 79
        if not missing(i):
            prefix = 'althingi_errors/'
            if i < 100:
                filename = prefix + '0' + str(i) + '.csv'
            else:
                filename = prefix + str(i) + '.csv'
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                prev_word = ""
                for row in reader:
                    cur_word = row['CorrectWord']
                    if cur_word == ",":
                        continue
                    if not prev_word:
                        cur_word = cur_word.lower()
                    if not word_frequency.get(cur_word):
                        word_frequency[cur_word] = 1
                    else:
                        word_frequency[cur_word] += 1
                    if not following_word.get(prev_word):
                        following_word[prev_word] = {}
                        following_word[prev_word][cur_word] = 1
                    elif not following_word[prev_word].get(cur_word):
                        following_word[prev_word][cur_word] = 1
                    else:
                        following_word[prev_word][cur_word] += 1
                    prev_word = cur_word

def exists(word):
    return following_word.get(word)


def count_seen_wordpair(previous_word, current_word):
    # print previous_word, current_word, "(" + str(following_word[previous_word].get(current_word)) + ")", "times"
    return following_word[previous_word].get(current_word)


def best_guess_if_rwe(previous_word, current_word):
    min_error_count = float('inf')
    min_error_word = ""
    for key, value in following_word[previous_word].items():
        edit_distance = editdistance.eval(key, current_word)
        if edit_distance < min_error_count:
            min_error_count = edit_distance
            min_error_word = key
    return min_error_word


def read_in_test_data():
    with open('althingi_errors/079.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        prev_word = ""
        for row in reader:
            word = row['Word']
            if word == ",":
                continue
            guess = word
            correct_word = row['CorrectWord']
            if not exists(prev_word):
                continue
            print("Count: ", count_seen_wordpair(prev_word, word))
            if not count_seen_wordpair(prev_word, word):
                print("Pair with error: ", prev_word, word)
                guess = best_guess_if_rwe(prev_word, word)
                print("Best guess: ", guess )
                print("Correct word: ", correct_word)
            elif word != correct_word:
                print("Not a real word error: ", word )
                print("Correct word: ", correct_word )
            prev_word = guess

create_dicts()
print("Should return a positive number", count_seen_wordpair('en', 'rétt'))
print(following_word['en'].get('sósíalismi'))
read_in_test_data()
# print "Should return True", check_real_word_error('horfinn', 'ef')
# print "Should return False", check_real_word_error('fresti', 'sem')
# print "Should return Vegna", best_guess_if_rwe('sæti', 'vega')

# for key, value in following_word.items():
#     print "word", key, value

# for key, value in word_frequency.items():
#     print "word", key, value


def words(text): return re.findall('[a-z]+', text.lower())


def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

# NWORDS = train(words(file('althingi_text/079.txt').read()))

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
