import time
from parameters import *


# Development purposes, prints types of errors
def print_errors_and_type(word, correct_word, guess, prev_word):
    if guess != correct_word:
        if word == guess:
            if Parameters.print_all_errors:
                print("unnoticed error: guess: ", guess, " correct word", correct_word, " word:", word,
                      " prev_word:", repr(prev_word))
            Parameters.unnoticed_errors += 1
        else:
            if word == correct_word:
                if Parameters.print_all_errors:
                    print("false error: guess: ", guess, " correct word", correct_word, " word:", word,
                          " prev_word:", repr(prev_word))
                Parameters.false_errors += 1
            else:
                if Parameters.print_all_errors:
                    print("wrong guess: guess: ", guess, " correct word", correct_word, " word:", word,
                          " prev_word:", repr(prev_word))
                Parameters.wrong_guesses += 1
    Parameters.total_words += 1


# Development purposes, print total error estimation
def print_error_estimation():
    wrong_guesses_percent = Parameters.wrong_guesses/Parameters.total_words*100
    false_errors_percent = Parameters.false_errors/Parameters.total_words*100
    unnoticed_errors_percent = Parameters.unnoticed_errors/Parameters.total_words*100
    print("Wrong guesses:", wrong_guesses_percent)
    print("False errors:", false_errors_percent)
    print("Unnoticed errors:", unnoticed_errors_percent)
    print("Total error:", wrong_guesses_percent + false_errors_percent + unnoticed_errors_percent)
    print()
    print("Duration:", time.process_time() - Parameters.before)