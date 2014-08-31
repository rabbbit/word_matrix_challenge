"""
    BigWords problem as per documents in "docs".

    Assumptions:
    - Aaa != aaa
    - given dictionary "aa" -> answer
            "
                2x2
                a a
                a a
            "
        is valid

    - marise_trie explodes on 500 000 000 keys.
"""

import argparse
import logging
import time
from itertools import combinations_with_replacement

from util.ordered_set import OrderedSet


def get_dicts(iterable, sort):
    """
        Iterable contains words/strings to be put into dictionaries.
        Split words in iterable by word length into sets.
        Return dictionary {word length, words}
        Optionally sort words (and return SortedSet)
    """

    start = time.time()
    dicts = {}

    for word in (word.strip() for word in iterable):
        dicts.setdefault(len(word), set()).add(word)

    if sort:
        # OrderedSet will guarantee that the first found word is the biggest
        for length, words in dicts.iteritems():
            dicts[length] = OrderedSet(sorted(words, reverse=True))

    logging.info('Successfully created dicts in %f', time.time() - start)
    logging.debug('Dict stats: len vs no_occurentes' + ''.join(
        '%2s: %d ' % (key, len(dicts[key])) for key in sorted(dicts.iterkeys()))
    )

    return dicts

def get_dicts_from_file(dict_location, really_big):

    with open(dict_location) as f:
        dicts = get_dicts(iterable=f, sort=really_big)

    return dicts

def get_rectangle_sizes(word_lengths):
    """
        Return possible rectangle sizes, sorted- biggest firs
    """

    #go guarantee consistency in combinations = first elem >= second_elem
    #TODO fixme - test what happens to performance if I switch it 
    word_lengths = sorted(word_lengths, reverse=True)

    return sorted(
        combinations_with_replacement(word_lengths, 2),
        key = lambda x: x[0]*x[1],
        reverse = True,
    )

def do_work(dict_location, really_big):

    logging.info('Starting work with dict: %s, really_big=%s', dict_location, really_big)

    dicts = get_dicts_from_file(dict_location, really_big)
    time.sleep(100)

    #print dicts

def run():

    parser = argparse.ArgumentParser(description='Find big words for Sanoma')
    parser.add_argument(
        '--file',
        help='dictionary location',
        required=True,
    )
    parser.add_argument(
        '--really-big',
        help='find biggest lexicographically',
        action='store_true',
    )
    parser.add_argument(
        '--debug',
        help='print logging',
        action='store_true',
    )

    args = parser.parse_args()
    
    if args.debug:
        logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)8s %(message)s')
    
    do_work(dict_location=args.file, really_big=args.really_big)

if __name__ == '__main__':
    run()
