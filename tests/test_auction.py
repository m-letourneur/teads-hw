import unittest

from auction import Auction, BadFormatException


class AuctionTest(unittest.TestCase):
    """
    Test suite for the Auction class.
    """

    def test_is_reserve_price_valid(self):
        """Assert whether validity check is consistent for reserve_price"""
        # reserve price is None
        self.assertFalse(Auction.is_reserve_price_valid(None),
                         "Reserve price should be invalid")

        # reserve price is an Int
        self.assertFalse(Auction.is_reserve_price_valid(1),
                         "Reserve price should be invalid")

        # reserve price is negative
        self.assertFalse(Auction.is_reserve_price_valid(-1.0),
                         "Reserve price should be invalid")

        # reserve price is a valid positive float
        self.assertTrue(Auction.is_reserve_price_valid(1.0),
                        "Reserve price should be valid")

    def test_is_list_buyers_bids_valid(self):
        """Assert whether validity check is consistent for list_buyers_bids"""
        # list_buyers_bids is None
        self.assertFalse(Auction.is_list_buyers_bids_valid(None),
                         "List should be invalid")

        # list_buyers_bids is a dict
        self.assertFalse(Auction.is_list_buyers_bids_valid({}),
                         "List should be invalid")

        # list_buyers_bids is a List[List[Int]]
        self.assertFalse(Auction.is_list_buyers_bids_valid([[1], [2]]),
                         "List should be invalid")

        # list_buyers_bids is a valid empty list
        self.assertTrue(Auction.is_list_buyers_bids_valid([]),
                        "List should be valid")

        # list_buyers_bids is a valid List[List[Float]]
        self.assertTrue(Auction.is_list_buyers_bids_valid([[1.0, 2.0], [2.0]]),
                        "List should be invalid")

    def test_constructor(self):
        """Check instanciation works with valid parameters"""
        auction = Auction(1.0, [[1.0], [2.0]])
        self.assertEqual(
            auction.reserve_price,
            1.0,
            "Reserve price is not set"
        )
        self.assertEqual(
            auction.list_buyers_bids,
            [[1.0], [2.0]],
            "List buyers-bids is not set"
        )

    def test_constructor_raises_exceptions(self):
        """Check exceptions are raised when at least one parameter is invalid"""
        with self.assertRaises(BadFormatException) as e:
            Auction(-1.0, [])
        self.assertEqual(e.exception.args[0],
                         Auction.EXCEPTION_BAD_FORMAT_RESERVE_PRICE)

        with self.assertRaises(BadFormatException) as e:
            Auction(1.0, [[1], [2]])
        self.assertEqual(e.exception.args[0],
                         Auction.EXCEPTION_BAD_FORMAT_LIST)

        with self.assertRaises(BadFormatException) as e:
            Auction(-1.0, [[1], [2]])
        self.assertEqual(e.exception.args[0],
                         Auction.EXCEPTION_BAD_FORMAT_RESERVE_PRICE)

    def test_get_flat_list_tuples(self):
        """Check consistency of the flatten list"""
        auction = Auction(1.0, [
            [10.0, 11.0],
            [12.0, 13.0]
        ])
        self.assertEqual(
            auction.get_flat_list_tuples(),
            [(0, 10.0), (0, 11.0), (1, 12.0), (1, 13.0)],
            "Flatten list of tuples is not consistent"
        )

        # With an empty sublist
        auction = Auction(1.0, [
            [10.0, 11.0],
            [],
            [12.0]

        ])
        self.assertEqual(
            auction.get_flat_list_tuples(),
            [(0, 10.0), (0, 11.0), (2, 12.0)],
            "Flatten list of tuples is not consistent"
        )

    def test_get_sorted_flat_list_tuples(self):
        """
        Test method that sorts the buyer-bid tuple list.
        """
        auction = Auction(1.0, [
            [3.0],
            [1.0, 5.0],
            [1.0, 2.0]
        ])
        self.assertEqual(
            auction.get_sorted_flat_list_tuples(),
            [(1, 1.0), (2, 1.0), (2, 2.0), (0, 3.0), (1, 5.0)],
            "Bid-sorting is not valid"
        )

        # With an empty sublist
        auction = Auction(1.0, [
            [],
            [1.0, 5.0],
            [1.0, 2.0]
        ])
        self.assertEqual(
            auction.get_sorted_flat_list_tuples(),
            [(1, 1.0), (2, 1.0), (2, 2.0), (1, 5.0)],
            "Bid-sorting is not valid"
        )

    def test_get_sorted_flat_list_tuples_with_equality(self):
        """
        Check that sorting guarantees ascending order for the buyer index in
        case of bid equality.
        """
        auction = Auction(1.0, [
            [1.0, 5.0],
            [1.0, 5.0],
            [1.0, 2.0]
        ])
        self.assertEqual(
            auction.get_sorted_flat_list_tuples(),
            [(0, 1.0), (1, 1.0), (2, 1.0), (2, 2.0), (0, 5.0), (1, 5.0)],
            "Bid-sorting does not keep buyer index ordered."
        )

    def test_get_winning_buyer(self):
        """Check winning buyer consistency"""
        auction = Auction(2.0, [
            [3.0],
            [1.0, 5.0],
            [1.0, 2.0]
        ])
        self.assertEqual(
            Auction.get_winning_buyer(auction.reserve_price,
                                      auction.get_sorted_flat_list_tuples()),
            1,
            "Winner buyer should be index 1"
        )

    def test_get_winning_buyer_for_bids_equality(self):
        """Check winning buyer is the one with highest index in case of highest
        bid equality"""
        auction = Auction(2.0, [
            [5.0],
            [1.0, 5.0],
            [2.0],
            [1.0, 5.0],
            [3.0]
        ])
        self.assertEqual(
            Auction.get_winning_buyer(
                auction.reserve_price,
                auction.get_sorted_flat_list_tuples()),
            3,
            "Winner buyer should be index 3"
        )

    def test_get_winning_buyer_none(self):
        """Check winning buyer defaults to None in following cases:
            - if the input sorted list is empty
            - if the highest bid < reserve price
        """
        auction = Auction(2.0, [
            [1.0],
            [1.0, 1.4],
        ])

        self.assertIsNone(
            Auction.get_winning_buyer(auction.reserve_price, []),
            "Winner buyer should be None with empty sorted list"
        )

        self.assertIsNone(
            Auction.get_winning_buyer(
                auction.reserve_price,
                auction.get_sorted_flat_list_tuples()),
            "Winner buyer should be None"
        )

    def test_get_winning_price(self):
        """Check winning price consistency"""
        auction = Auction(2.0, [
            [3.0],
            [1.0, 5.0],
            [1.0, 1.5]
        ])

        self.assertEqual(
            Auction.get_winning_price(
                auction.reserve_price,
                auction.get_sorted_flat_list_tuples(),
                1),
            3.0,
            "Winner price should be 3.0"
        )

        self.assertEqual(
            auction.get_winning_price(
                auction.reserve_price,
                [(1, 1.0), (2, 1.0), (2, 1.5), (1, 5.0)],
                1),
            auction.reserve_price,
            "Winner price should default to reserve price"
        )


        self.assertEqual(
            Auction.get_winning_price(2.0, [(1, 5.0)], 1),
            2.0,
            "Winner price should default to reserve price"
        )

    def test_get_winning_price_none(self):
        """Check winning price defaults to None in following cases:
            - winning_buyer is None
        """
        self.assertIsNone(
            Auction.get_winning_price(2.0, [], None),
            "Winner price should be None with None winner"
        )

if __name__ == '__main__':
    unittest.main()
