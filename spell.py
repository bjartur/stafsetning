#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import importlib, correct
from parameters import *


def read_files():
    with open(training_data, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print("Creating dict from:", training_data)
        prev_word = ""
        for row in reader:
            word = row['CorrectWord']
            if word == ",":
                continue
            if not prev_word:
                word = word.lower()
            populate_word_frequency(word)
            populate_following_word(prev_word, word)
            global word_count
            word_count += 1
            prev_word = word


# Populates a dictionary of all words and how common they are
def populate_word_frequency(word):
    if not word_frequency.get(word):
        word_frequency[word] = 1
    else:
        word_frequency[word] += 1


# Populates a dictionary of following words and their occurrences
def populate_following_word(prev_word, cur_word):
    if not following_word.get(prev_word):
        following_word[prev_word] = {}
        following_word[prev_word][cur_word] = 1
    elif not following_word[prev_word].get(cur_word):
        following_word[prev_word][cur_word] = 1
    else:
        following_word[prev_word][cur_word] += 1


read_files()

correct.read_in_test_data(word_count, word_frequency, following_word)

print("Press <Enter> to retry correcting, or type q<Enter> to quit..")
while input() == "":
    importlib.reload(correct)
    correct.read_in_test_data(word_count, word_frequency, following_word)
    print("Press <Enter> to retry correcting, or type q<Enter> to quit..")
