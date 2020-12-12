import unittest

from utils import is_valid_list_list_float


class UtilsTest(unittest.TestCase):
    def test_is_valid_list_list_float(self):
        """Test utils method is_valid_list_list_float"""
        # list is None
        self.assertFalse(is_valid_list_list_float(None),
                         "List should be invalid")

        # list is a dict
        self.assertFalse(is_valid_list_list_float({}),
                         "List should be invalid")

        # list is a List[List[Int]]
        self.assertFalse(is_valid_list_list_float([[1], [2]]),
                         "List should be invalid")

        # list is a valid empty list
        self.assertTrue(is_valid_list_list_float([]),
                        "List should be valid")

        # list is a valid List[List[Float]]
        self.assertTrue(is_valid_list_list_float([[1.0, 2.0], [2.0]]),
                        "List should be invalid")


if __name__ == '__main__':
    unittest.main()
