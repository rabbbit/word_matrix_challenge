import time
import sys

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

    words2 = []
    for i in xrange(50):
        words2 = words2 + words
        print "Iteration %d, length %d, size: %s" % (i, len(words2), sys.getsizeof(words2))


    print "Loaded"

    time.sleep(100)


if __name__ == "__main__":
    run()
