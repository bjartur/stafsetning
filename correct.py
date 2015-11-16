import csv, editdistance
max_word_change = 1


def read_in_test_data(word_frequency, following_word, word_count, common_words, rare_words):
    def exists(word):
        return following_word.get(word)

    def count_seen_wordpair(previous_word, current_word):
        # print previous_word, current_word, "(" + str(following_word[previous_word].get(current_word)) + ")", "times"
        return following_word[previous_word].get(current_word) or 0

    def best_guess(previous_word, current_word):
    	least_distance = max_word_change 
    	guess = ""
    	if not exists(previous_word):
    		possibilities = word_frequency
    	else:
    		possibilities = following_word[previous_word]
    	for possibility, freq in possibilities.items():
    		edit_distance = editdistance.eval(possibility, current_word)
    		if edit_distance < least_distance:
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
            word = row['Word']
            if word == ",":
                continue
            if (word in common_words or prev_word in common_words) and (word in rare_words or prev_word in rare_words):
                guess = word
            elif exists(prev_word) and count_seen_wordpair(prev_word, word) > 0:
                guess = word
            elif prev_guess != prev_word and count_seen_wordpair(prev_guess, word) > 0:
                guess = word
            else: # assert exists(prev_guess):
                guess = best_guess(prev_guess, word)
            if not prev_word:
                guess.capitalize()
                #print("Best guess: ", guess )
                #print("Correct word: ", correct_word)
            #elif word != correct_word:
                #print("Not a real word error: ", word )
                #print("Correct word: ", correct_word )
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
        print("wrong guesses: ", wrong_guesses_percent)
        print("false errors: ", false_errors_percent)
        print("unnoticed errors", unnoticed_errors_percent)
        return wrong_guesses_percent, false_errors_percent, unnoticed_errors_percent
