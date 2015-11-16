import csv, editdistance, time
max_word_change = 1
treshold_common = 0.005
treshold_rare   = 0.001


def read_in_test_data(word_count, word_frequency, following_word):
    #print("Yay!")
    def exists(word):
        return following_word.get(word)

    # Assuming word exists
    def common(word):
        return word_frequency[word] > treshold_common/word_count

    # Assuming word exists
    def rare(word):
        return word_frequency[word] < treshold_rare/word_count

    def count_seen_wordpair(previous_word, current_word):
        return following_word[previous_word].get(current_word) or 0
	
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
        for row in reader:
            before = time.process_time()
            word = row['Word']
            if word == ",":
                continue
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
            correct_word = row['CorrectWord']
            if guess != correct_word:
                if word == guess:
                    unnoticed_errors += 1
                else:
                    if word == correct_word:
                        false_errors += 1
                    else:
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
        print()
        print("Duration:", time.process_time() - before)
        return wrong_guesses_percent, false_errors_percent, unnoticed_errors_percent
