#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, sys
import importlib, correct
from parameters import *

if len(sys.argv) > 1:
    fi = sys.argv[1]
    filename.append(fi)


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
            words.add(word)
            populate_following_word(prev_word, word)
            global word_count
            word_count += 1
            prev_word = word


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

if __name__ == '__main__':
    correct.read_in_test_data(word_count)
