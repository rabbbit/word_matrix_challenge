#from functools import total_ordering

#@total_ordering
class Rectangle(object):
	"""
		Util class to represent a rectangle of given sizes
		Useful for iterating,
		Given a list of words can return:
			- next word for this or lower level.
			- columns for current rectangle
	"""

	__slots__ = ['word_length', 'all_words', 'curr_words', 'curr_height',
		'iterators'
	]

	def __init__(self, word_length, words):
		self.word_length = word_length
		self.all_words = words

		self.curr_words = []
		self.curr_height = 1

		self.iterators = {}

	def get_next(self):
		"""
			Try to returns next element on this level.
			Move level up if level is exhausted.
			Try to return next element on that level.
			Move level up ..
			Raises StopIteration if all iterators are exhausted
		"""
		
		iterator = self.iterators.get(self.curr_height)

		# we are moving on the same level
		if iterator is not None:
			self.curr_words.pop()
		else:
			iterator = iter(self.all_words)
			self.iterators[self.curr_height] = iterator

		try:
			next_elem = next(iterator)
			self.curr_words.append(next_elem)
			return next_elem
		except StopIteration:

			if self.curr_height == 1:
				raise

			self.curr_height -= 1
			return self.get_next()

	def lower(self):
		"""
			Adds another layer to the rectangle.
			Initializes new iterator for that level
		"""
		self.curr_height += 1
		self.iterators[self.curr_height] = None


	def get_cols(self):
		for index in xrange(self.word_length):
			yield u''.join(word[index] for word in self.curr_words)

	def get_total_length(self):
		return len(self.get_string())

	def get_string(self):
		return u''.join(word for word in self.curr_words)

	def __gt__(self, other):
		return (self.get_total_length() > other.get_total_length()
			or (self.get_total_length() == other.get_total_length() and
				self.get_string() > other.get_string()
			)
		)

	def __eq__(self, other):
		return (self.get_total_length() == other.get_total_length() and
				self.get_string() == other.get_string()
		)

	def __repr__(self):
		return self.get_string()

	def print_final(self):
		print self.get_final_string()

	def get_final_string(self):
		first = "%sx%s\n%s"

		second = first % (
			self.word_length,
			len(self.curr_words),
			(" ".join("%s" for _ in xrange(self.word_length)) + "\n")*len(self.curr_words)
		)

		third = second % tuple(letter for word in self.curr_words for letter in word)

		return third.strip()
