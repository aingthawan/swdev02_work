# try to do ngram
# pls help

import nltk
from nltk.util import ngrams

text = "I play pokemon go everyday"

# do bigram
print("bigram")
bigram = ngrams(text.split(), 2)
for grams in bigram:
    print(grams)

# do unigram
print("unigram")
bigram = ngrams(text.split(), 1)
for grams in bigram:
    print(grams)