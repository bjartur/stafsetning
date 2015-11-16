#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

word_frequency = {}
following_word = {}
word_count = 0
rare_word_treshold = 4


def missing(i):
    if i in [83, 98, 109, 111]:
        return True
    else:
        return False


def read_files():
    for i in range(79,81):
        if not missing(i):
            prefix = 'althingi_tagged/'
            if i < 100:
                filename = prefix + '0' + str(i) + '.csv'
            else:
                filename = prefix + str(i) + '.csv'
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                print("Creating dict from althingi tagged nr: ", i)
                prev_word = ""
                for row in reader:
                    prev_word = create_dicts(prev_word, row['Word'])


def create_dicts(prev_word, cur_word):
    if cur_word == ",":
        return prev_word
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
    return prev_word

read_files()
print("Press <Enter> to start correcting.")
while input() == "":
    from correct import read_in_test_data
    read_in_test_data(word_count, word_frequency, following_word)
