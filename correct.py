#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv, editdistance, time
import train
from parameters import *


def read_in_test_data(word_count, word_frequency, following_word):

    confusing, similar = train.characterwise()
    unnoticed_errors = 0
    wrong_guesses = 0
    false_errors = 0
    total_words = 0

    def exists(word):
        return following_word.get(word)

    def skipta(word, i, becomes):
        return word[:i] + becomes + word[i+1:]

    # þær stafarunur sem eru einni stafavíxlun frá word
    def fikta(word):
        for c in confusing:
            for i, letter in enumerate(word):
                if letter == c:
                    for alternative in similar[letter]:
                        yield skipta(word, i, alternative)


    def ocr_correction(word, confusing, similar):
        for m in fikta(word):
            if exists(m):
                return m
        if 2 <= max_change_optical:
            for m in fikta(word):
                for n in fikta(m):
                    if exists(n):
                        return n
        if 2 < max_change_optical:
            raise NotImplementedError

    def make_guess(confusing, similar, prev_word, prev_guess, word):
        if word.find('--') == 0:
            guess = '---'
        elif word.find('--') > 0:
            guess = word.replace('---', '-').replace('--', '-')
        elif exists(word) or word in [":", "(", ")", ";", ".", ","]:
            guess = word
        else:
            guess = ocr_correction(word, confusing, similar)
            if guess is None:
                if exists(prev_word):
                    guess = best_guess(prev_word, word)
                else:
                    guess = best_guess(prev_guess, word)
            if not guess:
                guess = best_guess(None, word)

            if prev_word == ".":
                # The first word in a sentence.
                guess = guess.capitalize()
                i = guess.find('-')
                if i > 0:
                    former = guess[:i+1]
                    latter = guess[i+1:].capitalize()
                    guess = former + latter
        return guess


    # Assuming previous_word exists
    def best_guess(previous_word, current_word):
        least_distance = max_change_context
        guess = ""
        if not exists(previous_word):
            possibilities = word_frequency
        else:
            possibilities = following_word[previous_word]
        for possibility, freq in possibilities.items():
            edit_distance = editdistance.eval(possibility, current_word)
            if edit_distance <= least_distance:
                least_distance = edit_distance
                guess = possibility
        return guess or current_word

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        prev_word = ""
        prev_guess = ""
        before = time.process_time()
        with open('result.csv', 'w', newline='') as csvresultfile:
            writer = csv.writer(csvresultfile)
            writer.writerow(['Word', 'Tag', 'Lemma', 'CorrectWord'])
            for row in reader:
                word = row['Word']
                if word in [",", ""]:
                    continue
                guess = make_guess(confusing, similar, prev_word, prev_guess, word)
                writer.writerow([row['Word'], row['Tag'],row['Lemma'],guess])

                # Only for accuracy estimation during development phase
                if dev_mode:
                    correct_word = row['CorrectWord']
                    if guess != correct_word:
                        if word == guess:
                            if print_all_errors:
                                print("unnoticed error: guess: ", guess, " correct word", correct_word, " word:", word,
                                      " prev_word:", repr(prev_word))
                            unnoticed_errors += 1
                        else:
                            if word == correct_word:
                                if print_all_errors:
                                    print("false error: guess: ", guess, " correct word", correct_word, " word:", word,
                                          " prev_word:", repr(prev_word))
                                false_errors += 1
                            else:
                                if print_all_errors:
                                    print("wrong guess: guess: ", guess, " correct word", correct_word, " word:", word,
                                          " prev_word:", repr(prev_word))
                                wrong_guesses += 1
                    total_words += 1

                # Updating varibles
                prev_guess = guess
                prev_word = word

        # Only for accuracy estimation during development phase
        if dev_mode:
            wrong_guesses_percent = wrong_guesses/total_words*100
            false_errors_percent = false_errors/total_words*100
            unnoticed_errors_percent = unnoticed_errors/total_words*100
            print("Wrong guesses:", wrong_guesses_percent)
            print("False errors:", false_errors_percent)
            print("Unnoticed errors:", unnoticed_errors_percent)
            print("Total error:", wrong_guesses_percent + false_errors_percent + unnoticed_errors_percent)
            print()
            print("Duration:", time.process_time() - before)
