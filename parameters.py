class Parameters:
    filename = ''
    max_change_context = 1
    max_change_optical = 2
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

    # Error counters for development proposes
    unnoticed_errors = 0
    wrong_guesses = 0
    false_errors = 0
    total_words = 0

    # Timing
    Before = 0
    