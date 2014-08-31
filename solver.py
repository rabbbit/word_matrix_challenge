"""
    BigWords problem as per documents in "docs".

    Comments:
    - it's slow, but I am not going to multiprocess, sorry :]
    - I am using marisa_trie:
        - I know it exploded for 500k keys per Trie - I ignored it for now
            (I createa a trie per word length)
        - Installation
            - checked on Docker
            - rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
            - yum install gcc
            - yum install gcc-c++
            - yum install python-pip
            - yum install python-devel
            - pip install marisa_trie
    - also:
        yum install argparse
        - 

    Assumptions:
    - Aaa != aaa
    - given dictionary "aa" -> answer
            "
                2x2
                a a
                a a
            "
        is valid

    - marise_trie explodes on 500 000 000 keys - I am going to ignore it,
        if the data is bigger it should be relatively easy to split it.
    - text said asci characters, but there were some non-asci ones in the file
        I'm simply ignoring those words
    - I'm not going to do multiprocess things, sorry :]
"""

import argparse
import logging
import time
from itertools import combinations_with_replacement

from util.ordered_set import OrderedSet
from util.rectangle import Rectangle
from util import trie_util


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

    if dicts.get(0):
        del dicts[0]

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

    sizes = sorted(
        combinations_with_replacement(word_lengths, 2),
        key = lambda x: x[0]*x[1],
        reverse = True,
    )

    logging.debug('Sizes to check: %s', sizes)

    return sizes

def find_solution(size, dicts):

    rectangle_width = size[0]
    rectangle_height = size[0]

    words = dicts[rectangle_width]
    trie = trie_util.get_trie(rectangle_width, dicts)

    r = Rectangle(rectangle_width, words)

    try:
        while True:
            r.get_next()
            
            if all(trie.has_keys_with_prefix(col) for col in r.get_cols()):

                if rectangle_height == r.get_height():
                    return r
                else:
                    r.lower()
    except StopIteration:
        return None

    raise Exception('This should not happend')


def print_answer(answers):
    pass

def do_work(dict_location, really_big):

    logging.info('Starting work with dict: %s, really_big=%s', dict_location, really_big)

    answers = []

    dicts = get_dicts_from_file(dict_location, really_big)

    sizes = get_rectangle_sizes(dicts.keys())

    prev_time = start_time = time.time()

    for index, size in enumerate(sizes, 1):

        time_now = time.time()

        logging.debug('Checking size: %s (%d/%d) (prev step: %f, total: %f)',
            size, index, len(sizes), time_now - prev_time, time_now - start_time,
        )

        prev_time = time_now

        answer = find_solution(size, dicts)

        if answer is not None:
            answers.append(answer)

        # even if we find an answer, we might have to go to the next step
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

        trie_util.check_unused_tries(size)


    print_answer(answers)

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
