import unittest
import solver

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




if __name__ == '__main__':
	unittest.main()
