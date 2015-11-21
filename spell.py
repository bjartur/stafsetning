#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import importlib, correct

word_frequency = {}
following_word = {}
word_count = 0
rare_word_treshold = 4
ordmyndir = []


def missing(i):
    if i in [83, 98, 109, 111]:
        return True
    else:
        return False

def missing_error(num):
    if num in [83, 86, 87, 88, 98, 104, 109]:
        return True
    else:
        return False

def read_files():
    with open("known_errors.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print("Creating dict from known_corrections.csv")
        prev_word = ""
        for row in reader:
            word = row['CorrectWord']
            prev_word = create_dicts(prev_word, word)


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

correct.read_in_test_data(word_count, word_frequency, following_word)

print("Press <Enter> to retry correcting, or type q<Enter> to quit..")
while input() == "":
    importlib.reload(correct)
    correct.read_in_test_data(word_count, word_frequency, following_word)
    print("Press <Enter> to retry correcting, or type q<Enter> to quit..")


# import csv
# with open('eggs.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=' ',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
#     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
