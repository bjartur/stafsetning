#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, editdistance

word_frequency = {}
following_word = {}
word_count = 0
common_words = set()
rare_words = set()
rare_word_treshold = 4


# def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
#     csv_reader = csv.DictReader(utf8_data, dialect=dialect, **kwargs)
#     for row in csv_reader:
#         yield [unicode(cell, 'utf-8') for cell in row]

def missing(i):
    if i in [83, 98, 109, 111]:
        return True
    else:
        return False


def create_dicts(frequency_treshold=0.006):
    #for i in range(79,136):
    for i in range(79,80):
        if not missing(i):
            prefix = 'althingi_tagged/'
            if i < 100:
                filename = prefix + '0' + str(i) + '.csv'
            else:
                filename = prefix + str(i) + '.csv'
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                prev_word = ""
                for row in reader:
                    cur_word = row['Word']
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
                    global word_count
                    word_count += 1
    for key, value in word_frequency.items():
        if value / word_count > frequency_treshold:
            common_words.add(key)
            print("Common word added: ", key)
        if value <= rare_word_treshold:
            rare_words.add(key)
            print("Rare word: ", key, value)




# def correctness(frequency_treshold = 0.006):
#     return 100 - sum(read_in_test_data(frequency_treshold))

create_dicts()
print("Press <Enter> to start correcting.")
while(input() == ""):
	from correct import read_in_test_data
	read_in_test_data(word_frequency, following_word, word_count, common_words, rare_words)
# print("Should return a positive number", count_seen_wordpair('en', 'rétt'))
# print(following_word['en'].get('sósíalismi'))

# frequency_treshold = 0.06
# while(correctness < 95):
#     print("Testing frequency treshold", frequency_treshold)
#     cre




# print "Should return True", check_real_word_error('horfinn', 'ef')
# print "Should return False", check_real_word_error('fresti', 'sem')
# print "Should return Vegna", best_guess_if_rwe('sæti', 'vega')

# for key, value in following_word.items():
#     print "word", key, value

# for key, value in word_frequency.items():
#     print "word", key, value


# def words(text): return re.findall('[a-z]+', text.lower())
#
#
# def train(features):
#     model = collections.defaultdict(lambda: 1)
#     for f in features:
#         model[f] += 1
#     return model

# NWORDS = train(words(file('althingi_text/079.txt').read()))

#alphabet = 'aábcdeéfghiíjklmnoópqrstuúvwxyzþæö'
# alphabet = 'abcdefghijklmnopqrstuvwxyz'
#
# def edits1(word):
#    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
#    deletes    = [a + b[1:] for a, b in splits if b]
#    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
#    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
#    inserts    = [a + c + b     for a, b in splits for c in alphabet]
#    return set(deletes + transposes + replaces + inserts)
#
#
# def known_edits2(word):
#     return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)
#
#
# def known(words): return set(w for w in words if w in NWORDS)
#
#
# def correct(word):
#     candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
#     return max(candidates, key=NWORDS.get)
