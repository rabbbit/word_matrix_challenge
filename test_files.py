import time
import sys
import marisa_trie

def run():

    words = set()
    words = {}
    words = []

    with open("wordlist.txt") as f:
        for line in f:
            line = line.strip()
            #print "word: %s |" % line
            #words[line] = None
            words.append(line)

    print "Initial length: %s" % len(words)

    words_u = []
    for word in words:
        try:
            u_word = unicode(word)
            words_u += u_word
        except UnicodeDecodeError:
            print 'failed to process %s' % word

    words2 = []
    for i in xrange(10):
        words2 = words2 + words_u
        print "Iteration %d, length %d, size: %s" % (i, len(words2), sys.getsizeof(words2))

    print 'words created'
    words2.sort()
    marisa_trie.Trie(words2).mmap('my_record_trie.marisa')
    print 'trie created'
    del words2
    del words_u

    print "Loaded"

    time.sleep(100)


if __name__ == "__main__":
    run()
