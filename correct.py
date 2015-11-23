#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv, editdistance, time
import train
from parameters import *
from error_estimation import *


def read_in_test_data():

    confusing, similar = train.characterwise()

    def exists(word):
        return Parameters.following_word.get(word)

    def change(word, i, subsitute):
        return word[:i] + subsitute + word[i+1:]

    # þær stafarunur sem eru einni stafavíxlun frá word
    def explore(word):
        for c in confusing:
            for i, letter in enumerate(word):
                if letter == c:
                    for alternative in similar[letter]:
                        yield change(word, i, alternative)

    def ocr_correction(word):
        for m in explore(word):
            if exists(m):
                return m
        if 2 == Parameters.max_change_optical:
            for m in explore(word):
                for n in explore(m):
                    if exists(n):
                        return n
        if 2 < Parameters.max_change_optical:
            raise NotImplementedError

    def make_guess(prev_word, prev_guess, word):
        if word.find('--') == 0:
            guess = '---'
        elif word.find('--') > 0:
            guess = word.replace('---', '-').replace('--', '-')
        elif exists(word) or word in [":", "(", ")", ";", ".", ","]:
            guess = word
        else:
            guess = ocr_correction(word)
            if guess is None:
                guess = best_guess(prev_guess, word)
            if prev_word == ".":
                # The first word in a sentence.
                guess = guess.capitalize()
            i = guess.find('-')
            if i > 0:
                guess = guess.capitalize()
                former = guess[:i+1]
                latter = guess[i+1:].capitalize()
                guess = former + latter
        return guess

    # Assuming previous_word exists
    def best_guess(previous_word, current_word):
        least_distance = Parameters.max_change_context
        guess = ""
        if not exists(previous_word):
            possibilities = Parameters.words
        else:
            possibilities = Parameters.following_word[previous_word]
        for possibility in possibilities:
            edit_distance = editdistance.eval(possibility, current_word)
            if edit_distance <= least_distance:
                least_distance = edit_distance
                guess = possibility
        return guess or current_word

    with open(Parameters.filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        prev_word = ""
        prev_guess = ""
        Parameters.before = time.process_time()
        new_file = Parameters.filename[:-4]+"_corrected.csv"
        with open(new_file, 'w', newline='') as csvresultfile:
            print('Creating corrections from:', Parameters.filename)
            writer = csv.writer(csvresultfile)
            writer.writerow(['Word', 'Tag', 'Lemma', 'CorrectWord'])
            for row in reader:
                word = row['Word']
                if word in [",", ""]:
                    continue
                guess = make_guess(prev_word, prev_guess, word)
                writer.writerow([row['Word'], row['Tag'],row['Lemma'],guess])

                # Only for accuracy estimation during development phase
                if Parameters.dev_mode:
                    correct_word = row['CorrectWord']
                    print_errors_and_type(word, correct_word, guess, prev_word)

                # Updating varibles
                prev_guess = guess
                prev_word = word

        # Only for accuracy estimation during development phase
        if Parameters.dev_mode:
            print_error_estimation()
        print('Correction are in file', new_file)