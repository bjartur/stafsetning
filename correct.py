#!/usr/bin/python3
import csv, editdistance, time
max_word_change = 1
treshold_common = 0.005
treshold_rare   = 0.001


def read_in_test_data(word_count, word_frequency, following_word):
    def exists(word):
        return following_word.get(word)

    def common_ocr_errors(word):
        if word == "i":
            return "í"
        if word in [":", "(", ")", ";", ".", ",","-"]:
            return word
        else:
            for i in range(len(word)):
                if word[i] == "i":
                    pre = word[:i]
                    suf = word[i+1:]
                    new_word = pre + "í" + suf
                    if exists(word):
                        return word
                    if exists(new_word):
                        #print("i errors: ", word, new_word)
                        return new_word
                if word[i] == "í":
                    pre = word[:i]
                    suf = word[i+1:]
                    new_word = pre + "i" + suf
                    if exists(word):
                        return word
                    if exists(new_word):
                        #print("í errors: ", word, new_word)
                        return new_word
            return word

    # Assuming word exists
    def common(word):
        return word_frequency[word] > treshold_common/word_count

    # Assuming word exists
    def rare(word):
        return word_frequency[word] < treshold_rare/word_count

    def count_seen_wordpair(previous_word, current_word):
        return following_word[previous_word].get(current_word) or 0

    def create_guess(prev_word, prev_guess, word):
        if exists(word) and exists(prev_word) and (common(word) or common(prev_word)) and (rare(word) or rare(prev_word)):
            guess = word
        elif exists(prev_word) and count_seen_wordpair(prev_word, word) > 0:
            guess = word
        elif prev_guess != prev_word and count_seen_wordpair(prev_guess, word) > 0:
            guess = word
        else:
            # We don't know if prev_word existed.
            # So let's use prev_guess to be safe.
            guess = best_guess(prev_guess, word)
        if not prev_word:
            # The first word in a sentence.
            guess.capitalize()
        return guess


    def error_free(prev_word, word):
        if count_seen_wordpair(prev_word, word):
            return True


    def create_guess_v2(prev_word, prev_guess, word):
        # if (exists(word) and exists(prev_word)) and (common(word) or common(prev_word)) and (rare(word) or rare(prev_word)):
        #     guess = word
        # elif exists(prev_word) and count_seen_wordpair(prev_word, word) > 0:
        #     guess = word
        # elif prev_guess != prev_word and count_seen_wordpair(prev_guess, word) > 0:
        #     guess = word
        guess = ""
        # prev_word = common_ocr_errors(prev_word)
        # prev_guess = common_ocr_errors(prev_guess)
        # word = common_ocr_errors(word)
        if exists(word):
            if exists(prev_word):
                if error_free(prev_word, word):
                    guess = word
        else:
            word = common_ocr_errors(word)
            # We don't know if prev_word existed.
            # So let's use prev_guess to be safe.
            if exists(prev_word):
                guess = best_guess(prev_word, word)
            else:
                guess = best_guess(prev_guess, word)
        if not guess:
            guess = common_ocr_errors(word)
            #uess = word
            #print("pg, pw, w: ", prev_guess, prev_word, word)
        if not prev_word:
            # The first word in a sentence.
            guess = guess.capitalize()
        return guess


    # Assuming previous_word exists
    def best_guess(previous_word, current_word):
        least_distance = max_word_change
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

    with open('althingi_errors/079.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        prev_word = ""
        prev_guess = ""
        unnoticed_errors = 0
        wrong_guesses = 0
        false_errors = 0
        total_words = 0
        before = time.process_time()

        for row in reader:
            word = row['Word']
            if word == "," or "":
                continue
            guess = create_guess_v2(prev_word, prev_guess, word)
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
