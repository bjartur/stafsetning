#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv, editdistance, time
from itertools import chain
import train
max_change_context = 1
max_change_optical = 2
treshold_common = 0.005
treshold_rare   = 0.001

def read_in_test_data(word_count, word_frequency, following_word):
    def exists(word):
        return following_word.get(word)

    def skipta(word, i, becomes):
        return word[:i] + becomes + word[i+1:]

    def ocr_correction(word, confusing, similar, level=1):
        for c in confusing:
            for i, letter in enumerate(word):
                if letter == c:
                    for alternative in similar[letter]:
                        new = skipta(word, i, alternative)
                        if exists(new):
                            return new
                        elif level < max_change_optical:
                            new = ocr_correction(word, confusing, similar, level+1)
                            if exists(new):
                                return new

    def count_seen_wordpair(previous_word, current_word):
        return following_word[previous_word].get(current_word) or 0

    def seen(prev_word, word):
        if count_seen_wordpair(prev_word, word):
            return True

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
                guess = word
                #uess = word
                #print("pg, pw, w: ", prev_guess, prev_word, word)
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

    confusing, similar = train.characterwise(range(82,83))
    with open('althingi_errors/084.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        prev_word = ""
        prev_guess = ""
        unnoticed_errors = 0
        wrong_guesses = 0
        false_errors = 0
        total_words = 0
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
                correct_word = row['CorrectWord']
                if guess != correct_word:
                    if word == guess:
                        print("unnoticed error: guess: ", guess, " correct word", correct_word, " word:", word, " prev_word:", repr(prev_word))
                        unnoticed_errors += 1
                    else:
                        if word == correct_word:
                            print("false error: guess: ", guess, " correct word", correct_word, " word:", word, " prev_word:", repr(prev_word))
                            false_errors += 1
                        else:
                            print("wrong guess: guess: ", guess, " correct word", correct_word, " word:", word, " prev_word:", repr(prev_word))
                            wrong_guesses += 1
                total_words += 1
                prev_guess = guess
                prev_word = word
        wrong_guesses_percent = wrong_guesses/total_words*100
        false_errors_percent = false_errors/total_words*100
        unnoticed_errors_percent = unnoticed_errors/total_words*100
        print("Wrong guesses:", wrong_guesses_percent)
        print("False errors:", false_errors_percent)
        print("Unnoticed errors:", unnoticed_errors_percent)
        print("Total error:", wrong_guesses_percent + false_errors_percent + unnoticed_errors_percent)
        print()
        print("Duration:", time.process_time() - before)
        return wrong_guesses_percent, false_errors_percent, unnoticed_errors_percent
