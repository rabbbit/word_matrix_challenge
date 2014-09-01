import logging
import marisa_trie
import time

TRIES = {}

def get_trie(word_length, dicts):
    """
        Lazy load tries for a given word_length from dicts
    """
     
    if word_length not in TRIES:

        u_words = []

        start = time.time()

        for word in dicts[word_length]:
            u_words.append(unicode(word))

        TRIES[word_length] = marisa_trie.Trie(u_words)
        logging.debug('Created new trie for length %d in %f',
			word_length,
			time.time() - start
		)

    return TRIES[word_length]

def check_unused_tries(size):
    """
        Removes tries we won't need anymore - since we're always iterating
		downwards, its easy to know we don't need them anymore
		:param size: current size of rectangle we're looking for
    """

    max_key = size[0]*size[1]
    for key in sorted(TRIES.keys(), reverse=True):
       if key > max_key:
		   logging.debug('Removing unused trie for length: %d', key)
		   del TRIES[key]
