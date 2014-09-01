# README #

## Quick summary ##
	
Interview task for Sanoma

## Full summary ##

 A Big Word consists of a matrix filled with ASCII characters such that when
 we read each row we find a complete word which exists in the dictionary and
 when we read each column we also find a complete word which is in the dic-
 tionary. Additionally, sometimes we are interested in really big words, as indi-
 cated by the above flag. A really big word is a word which is lexicographically
 the largest among valid big words. We use row-major order to uniquely define
 the lexiographic relation.

## Algorithm description ##

Algorithm takes three parameters:

1. **file** => file containing dictionary to be used
2. **really**_big option => see above
3. **debug** option -> debug output will be printed on python2.7

First, the dictionary is parsed and split into buckets (sets), per word length

 * if really_big option is words within each bucket are ordered and set OrderedSet is used rather than Set - this guarantees that if a solution is found it is the maximum possible within the bucket
 * check TODO below, this should change
 * based on those set/buckets, later on, tries per word length are created lazily.

Once we have the buckets, we also know which words lengths we're dealing with. Based on this, we can build all the possible rectangle sizes, sorted by the biggest first. For example, for word_lengths=(5,4,1) we'd get [(5,5), (5,4), (4,4), (5,1), (4,1), (1,1)]

Then, we go by size by size and try to build a valid rectangle. We do it by picking a word, setting it within the rectangle horizontally, and then check, for each of the column, if a word exists in a dictionary with that prefix. If not, we pick next word, if yes, we add a new horizontal level and check all columns again. Example:

size = 3x2

words = [cat, cu, bit, bu, it, tu]

1. - pick word of length 3 => "cat"
2. - check if word starting with c exists => True (cu) => continue
3. - check if word starting with a exists => False  => pick next word at current level
4. - pick next word of length 3 => "bit"
5. - check for word starting with b => True (bu) => continue
6. - check for word starting with i => True (it) => continue
7. - check for word starting with t => True (tu) => continue
8. - we have a valid solution for size 3x2

Tries are using to check for existence of words with a given prefix.

If no valid solution is found, we move to a next size.
If a valid solution is found:
- if really-big is not set, we can just return
- -f really-big is set, we have to check for other sizes that might be bigger, for example: if we find a solution in (4,1), we still have to check (2,2) because (2,2) will have same length, and might have bigger lexicographical order.

This might mean having more than 1 result -> we pick the biggest and display it to the user.

* TODO:
	- not sure what the format of dictionary is: docs says one thing, example dict says something else
	- OrderedSet is not necessary at all, we could have a simple list since we're only using it for iterating
	- OrderedSet/list might not be necessary - we could iterate over keys from the trie. Have to check ordering/performance

### How do I get set up? ###

* Configuration
	- ./solver --file quarter_wordlist --really-big --debug
	- ./solver2.7 --file quarter_wordlist --really-big --debug

* Dependencies
Python 2.6 is required.

	- on new CentOS:

	- rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
	- yum install gcc
	- yum install gcc-c++
	- yum install python-pip
	- yum install python-devel
	- pip install marisa_trie
	- pip install argparse


* How to run tests
	- nosetest
	- python tests.py

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact