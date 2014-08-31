class Rectangle(object):
	"""
		Dumb object to iterate over rectangle of given length.
		Given a list of words can return:
			- next word for this or lower level.
			- columns for current rectangle
	"""

	def __init__(self, word_length, words):
		self.word_length = word_length
		self.all_words = words

		self.curr_words = []
		self.curr_height = 0

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

			if self.curr_height == 0:
				raise

			self.curr_height -= 1
			return self.get_next()

	def get_lower(self):
		"""
			Adds another layer to the rectangle.
			Initializes new iterator for that level
		"""
		self.curr_height += 1
		return self.get_next()


	def get_columns(self):
		for index in range(self.word_length):
			yield ''.join(word[index] for word in self.curr_words)
