class Parameters:
    # Name of piped in file for error searching
    filename = ''
    # The allowed edit distance between words in context search
    max_change_context = 1
    # The allowed edit distance between words in context free search
    max_change_optical = 2
    # The necessary occurrence of an correct letter substitute to be relevant
    min_err_freq = 2

    # File for training data for populating word_frequency and following_word
    training_data = "known_errors.csv"
    # Files used in creating character specific training data
    print_all_errors = True
    # When developing we can see the error rate from previously corrected data
    dev_mode = True
    # All words who accure and their frequency
    words = set()
    # All words and a list of words that follow and how often
    following_word = {}
    # Counter for total words in text
    word_count = 0
    # Files missing in althingi error data
    missing = [83, 86, 87, 88, 98, 104, 109]

    #
    # Errors our program did not find
    unnoticed_errors = 0
    # Spelling was wrong but so was the correction
    wrong_guesses = 0
    # Word was spelled correctly but we thought it was a spelling mistake
    false_errors = 0
    # Total amount of words in document
    total_words = 0
    # Timing
    Before = 0
