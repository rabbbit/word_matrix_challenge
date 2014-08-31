import unittest
import solver

from util.rectangle import Rectangle
from util.ordered_set import OrderedSet

class TestDictParsing(unittest.TestCase):

	def test_empty(self):
		dicts = solver.get_dicts(iterable=[], sort=False)

		self.assertEquals(dicts, {})

	def test_empty_sort(self):
		dicts = solver.get_dicts(iterable=[], sort=True)

		self.assertEquals(dicts, {})

	def test_simple(self):

		to_test = (
			(
				('a', 'aaa', 'aaaaa'),
				{1 : set(['a']), 3: set(['aaa']), 5: set(['aaaaa'])}
			),
		)

		for iterable, result in to_test:
			self.assertEquals(
				solver.get_dicts(iterable=iterable, sort=False),
				result,
			)

	def test_sorting(self):

		to_test = (
			(
				('zza', 'aaa', 'zzz'), 3, ['zzz', 'zza', 'aaa'],
			),
		)

		for iterable, length, result in to_test:
			self.assertEquals(
				list(solver.get_dicts(iterable=iterable, sort=True)[length]),
				result,
			)


class TestRectangleSizes(unittest.TestCase):

	def test_sorting(self):

		to_test = (
			((), []),
			((1,), [(1,1)]),
			((1, 2), [(2,2), (2,1), (1,1)]),
			((2, 1), [(2,2), (2,1), (1,1)]),
			((3, 1), [(3,3), (3,1), (1,1)]),
			(
				(11, 5, 4, 1),
				[(11,11), (11,5), (11,4), (5,5), (5,4), (4,4), (11, 1), 
					(5,1), (4,1), (1,1)], 
			),
			(
				(100, 99, 2, 1),
				[(100,100), (100,99), (99,99), (100,2), (99,2), (100, 1),
					(99, 1), (2,2), (2,1), (1,1), 
				]
			),
		)

		for word_lengths, sizes in to_test:

			self.assertEquals(
				solver.get_rectangle_sizes(word_lengths),
				sizes,
			)

class TestRectangleObject(unittest.TestCase):

	def test_empty(self):

		r = Rectangle(1, [])

		with self.assertRaises(StopIteration):
			r.get_next()

	def test_one_level(self):

		r = Rectangle(1, ['1', '2', '3'])

		self.assertEquals(
			r.get_next(),
			'1',
		)

		self.assertEquals(
			r.get_next(),
			'2',
		)

		self.assertEquals(
			r.get_next(),
			'3',
		)

		with self.assertRaises(StopIteration):
			r.get_next()


	def test_more_levels(self):

		r = Rectangle(1, ['1', '2', '3'])

		self.assertEquals(
			r.get_next(),
			'1',
		)

		r.lower()
		self.assertEquals(
			r.get_next(),
			'1',
		)

		r.lower()
		self.assertEquals(
			r.get_next(),
			'1',
		)

		for item in ['2', '3', '2', '3', '2', '3']:
			self.assertEquals(
				r.get_next(),
				item,
			)

		with self.assertRaises(StopIteration):
			r.get_next()



	def test_columns_one_level(self):
		
		r = Rectangle(3, ['123'])
		
		self.assertEquals(
			r.get_next(),
			'123',
		)

		self.assertEquals(
			list(r.get_cols()),
			[u'1', u'2', '3'],
		)

	def test_columns_more_levels(self):

		r = Rectangle(3, ['123', '456', '789'])

		r.get_next()
		r.lower()
		r.get_next()
		r.lower()
		r.get_next()

		self.assertEquals(
			list(r.get_cols()),
			[u'111', u'222', u'333'],
		)

		r.get_next()

		self.assertEquals(
			list(r.get_cols()),
			[u'114', u'225', u'336'],
		)

	def test_comparison_simple(self):

		r0 = Rectangle(1, ['1', '2', '3'])
		r1 = Rectangle(3, ['111', '222', '333'])
		r2 = Rectangle(3, ['111', '999', '999'])
		r3 = Rectangle(3, ['112', '111', '111'])

		for r in (r1, r2, r3):
			r.get_next()
			r.lower()
			r.get_next()
			r.lower()
			r.get_next()
			r.lower()

		self.assertGreater(r1, r0)
		self.assertEquals(r1, r2)
		self.assertGreater(r3, r2)

class TestIndividualSolutions(unittest.TestCase):

	def test_simple(self):

		size = (1,1)
		dicts = {1 : set('1')}

		r = solver.find_solution(size, dicts)

		self.assertIsNotNone(r)

	def test_example_from_doc(self):

		size = (2,2)
		dicts = {2 : set(['am', 'ma', 'pa'])}

		r = solver.find_solution(size, dicts)

		self.assertIsNotNone(r)


	def test_example_from_doc_sorted(self):

		size = (2,2)
		dicts = {2 : OrderedSet(['pa', 'am', 'zz', 'ma'])}

		r = solver.find_solution(size, dicts)

		self.assertIsNotNone(r)

		self.assertEquals(
			'paam',
			r.get_string(),
		)


		


if __name__ == '__main__':
	unittest.main()
