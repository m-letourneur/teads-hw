import unittest

from auction import Auction


class ExampleTest(unittest.TestCase):
    """
    Test the algorithm on the default example.

    ## Example
    Consider 5 potential buyers (A, B, C, D, E) who compete to acquire an object
    with a reserve price set at 100 euros, bidding as follows:

        A: 2 bids of 110 and 130 euros
        B: 0 bid
        C: 1 bid of 125 euros
        D: 3 bids of 105, 115 and 90 euros
        E: 3 bids of 132, 135 and 140 euros

    The buyer E wins the auction at the price of 130 euros.
    """

    def setUp(self) -> None:
        """Instantiate the example auction"""
        self.auction: Auction = Auction(100.0,
                                        [
                                            [110.0, 130.0],
                                            [],
                                            [125.0],
                                            [105.0, 115.0, 90.0],
                                            [132.0, 135.0, 140.0]
                                        ])

    def test_winners(self):
        """Check winner buyer is the 4th one, with winning price = 130"""
        winning_buyer, winning_price = self.auction.get_winners()

        self.assertEqual(
            winning_buyer,
            4,
            "The winner of the bid should be buyer #4 (E)"
        )

        self.assertEqual(
            winning_price,
            130.0,
            "The winning price should be buyer 130"
        )


if __name__ == '__main__':
    unittest.main()
