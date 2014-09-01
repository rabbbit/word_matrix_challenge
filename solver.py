"""
    BigWords problem as per documents in "docs".

    Comments:
    - it's slow = for full dictionary it takes hours. Only ~50 seconds for 100k
        long one though.

    Assumptions:
    - Aaa != aaa
    - given dictionary "aa" -> answer
            "
                2x2
                a a
                a a
            "
        is valid
    - ignore words with non-ascii characters
    - marisa_trie might explode on 500m keys - maximum trie I need
        currently has 50k elements.

"""

import argparse
import logging
import time

#from itertools import combinations_with_replacement
from util.itertools27 import combinations_with_replacement
from util.rectangle import Rectangle
from util.trie_util import get_trie, check_unused_tries


def get_dicts(iterable, sort):
    """
        Turns iterable into a dict of lists of all available words,
        keyed by word_length.
        :param iterable: iterable to find words in
        :param sort: does data have to be sorted,
            if yes, dictionary will contain OrderedSets
        :returns: dictionary for sets, keyed by word length
    """

    start = time.time()
    dicts = {}

    for word in (word.strip() for word in iterable):
        try:
            dicts.setdefault(len(word), list()).append(unicode(word))
        except UnicodeDecodeError:
            logging.warning('Failed to convert %s, skipping', word)

    if dicts.get(0):
        del dicts[0]

    if sort:
        # sorted order will guarantee that the first found word is the biggest
        for words in dicts.itervalues():
            words.sort(reverse=True)

    logging.info('Successfully created dicts in %f', time.time() - start)
    logging.debug('Dict stats: len vs no_occurentes' + ''.join(
        '%2s: %d ' % (key, len(dicts[key])) for key in sorted(dicts.iterkeys()))
    )

    return dicts

def get_dicts_from_file(dict_location, really_big):
    """
        Like above, but from file
    """

    with open(dict_location) as f:
        dicts = get_dicts(iterable=f, sort=really_big)

    return dicts

def get_rectangle_sizes(word_lengths):
    """
        Return possible rectangle sizes, sorted- biggest firs
        :param word_lengths: iterable of all word lengths present in dictionary
    """

    #go guarantee consistency in combinations = first elem >= second_elem
    word_lengths = sorted(word_lengths, reverse=True)

    sizes = sorted(
        combinations_with_replacement(word_lengths, 2),
        key = lambda x: x[0]*x[1],
        reverse = True,
    )

    return sizes

def find_solution_for_size(size, dicts):
    """
        Finds a solution for a given size
        :param size: a tuple of required size
        :param dicts: dictionary of lists of all available words, per word_length
        :returns: a solution (Rectangle object) or None
    """

    rectangle_width = size[0]
    rectangle_height = size[1]

    words = dicts[rectangle_width]
    trie = get_trie(rectangle_width, dicts)

    r = Rectangle(rectangle_width, words)

    try:
        while True:
            r.get_next()

            #if the rectangle is valid so far, exit or go lower
            if all(trie.has_keys_with_prefix(col) for col in r.get_cols()):

                if rectangle_height == r.curr_height:
                    logging.info('Found a solution: %s - %s', size, r)
                    return r
                else:
                    r.lower()

    except StopIteration:
        return None

    raise Exception('This should not happend')


def print_best_answer(answers, start_time):
    """
        Prints best answer of the ones given
        :param answers: list of Rectangle objects
        :param start_time: linux timestamp
    """

    logging.info('Found answer in %f', time.time() - start_time)
    best = max(answers)

    best.print_final()


def do_work_from_file(dict_location, really_big):
    """
        Entry point for data contained in a file
        :param dict_location: path to file
        :param really_big: true/false flag
    """

    logging.info('Starting work with dict: %s, really_big=%s', dict_location, really_big)

    dicts = get_dicts_from_file(dict_location, really_big)

    do_work(dicts, really_big)

def do_work_from_iterable(iterable, really_big):
    """
        Like above, but accepts iterables.
        Currently used for testing
        :param iterable: dictionary, as iterable of words
        :param really_big: true/false flag
    """

    dicts = get_dicts(iterable, really_big)

    do_work(dicts, really_big)

def do_work(dicts, really_big):
    """
        Where magic happens
        :param dicts: dictionary of lists of words, keyed by word_length
        :param really_big: true/false flag
    """

    #we might have more than one valid answer
    answers = []

    #all possible rectangle sizes, sorted from the biggest
    sizes = get_rectangle_sizes(dicts.keys())
    logging.debug('Sizes to check: %s', sizes)

    prev_time = start_time = time.time()

    for index, size in enumerate(sizes, 1):

        time_now = time.time()

        logging.debug('Checking size: %s (%d/%d) (prev step: %f, total: %f)',
            size, index, len(sizes), time_now - prev_time, time_now - start_time,
        )

        prev_time = time_now

        answer = find_solution_for_size(size, dicts)

        if answer is not None:
            answers.append(answer)

        # even if we find an answer, we might have to go to the next step
        # ex after (4x1), (2x2) might have bigger word
        if answer is not None and (
                not really_big or \
                index == len(sizes) or \
                size[0]*size[1] > sizes[index][0]*sizes[index][1]
            ):
            break

        # if no answer in this iteration, but we have previous ones
        # and we're moving to smaller size, exit
        if answer is None and \
                index == len(sizes) or \
                size[0]*size[1] > sizes[index][0]*sizes[index][1] and \
                len(answers):
            break

        check_unused_tries(size)

    print_best_answer(answers, start_time)

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

    do_work_from_file(dict_location=args.file, really_big=args.really_big)

if __name__ == '__main__':
    run()
