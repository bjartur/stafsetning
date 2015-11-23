# Put the name of your input file in line below
filename = 'althingi_errors/095.csv' # <- OVER HERE!


max_change_context = 1
max_change_optical = 2
treshold_common = 0.005
treshold_rare   = 0.001
min_err_freq = 2

# File for training data for populating word_frequency and following_word
training_data = "known_errors.csv"
# Files used in creating character specific training data
print_all_errors = True
# When developing we can see the error rate from previously corrected data
dev_mode = True
# All words who accure and their frequency
word_frequency = {}
# All words and a list of words that follow and how often
following_word = {}
# Counter for total words in text
word_count = 0
# Files missing in althingi error data
missing = [83, 86, 87, 88, 98, 104, 109]

# Parameters used in dev mode for estimating accuracy
