import logging
import marisa_trie

TRIES = {}

def get_trie(word_length, dicts):
    """
        Lazy load tries
    """
     
    if word_length not in TRIES:

        u_words = []

        for word in dicts[word_length]:
            try:
                u_words.append(unicode(word))
            except UnicodeDecodeError:
                logging.warning('Failed to convert %s, skipping', word)

        TRIES[word_length] = marisa_trie.Trie(u_words)

    return TRIES[word_length]

def check_unused_tries(size):
    """
        Removes tries we won't need anymore
    """
    pass
