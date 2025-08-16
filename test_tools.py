import unittest
from tools import ddgs_search

class TestTools(unittest.TestCase):
    def test_ddgs_search(self):
        results = ddgs_search('python')
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)
        self.assertTrue(all(isinstance(r, str) for r in results))

if __name__ == '__main__':
    unittest.main()
