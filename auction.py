from typing import List, Tuple, Optional

from utils import is_valid_list_list_float


class BadFormatException(Exception):
    pass


class Auction(object):
    """
    Class representing the auction:
        - the reserve price for the object
        - the list of buyers, each buyer is represented by the list of its bids
    """
    EXCEPTION_BAD_FORMAT_RESERVE_PRICE = "Reserve should be a positive float!"
    EXCEPTION_BAD_FORMAT_LIST = "list_buyers_bids does not match expected " \
                                "format: List[List[float]]!"

    def __init__(self, reserve_price: float,
                 list_buyers_bids: List[List[float]]):
        """
        Constructor.
        Check parameters' format and raise BadFormatException accordingly.

        :param reserve_price: float
        :param list_buyers_bids: list of list of float,
        """
        if Auction.is_reserve_price_valid(reserve_price):
            self.reserve_price = reserve_price
        else:
            raise BadFormatException(Auction.EXCEPTION_BAD_FORMAT_RESERVE_PRICE)
        if Auction.is_list_buyers_bids_valid(list_buyers_bids):
            self.list_buyers_bids = list_buyers_bids
        else:
            raise BadFormatException(Auction.EXCEPTION_BAD_FORMAT_LIST)

    @staticmethod
    def is_reserve_price_valid(reserve_price) -> bool:
        """
        Return True if reserve price verifies:
            - not None
            - float type
            - greater or equal to zero
        :return: bool
        """
        return (
                reserve_price is not None
                and isinstance(reserve_price, float)
                and reserve_price >= 0
        )

    @staticmethod
    def is_list_buyers_bids_valid(list_buyers_bids) -> bool:
        """
        Check list_buyers_bids format and validity:
            - not None
            - list type
            - float type for all bids
        :return: bool
        """
        return is_valid_list_list_float(list_buyers_bids)

    def get_flat_list_tuples(self) -> List[Tuple[int, float]]:
        """
        Flatten the list_buyers_bids into a list:
            [
                (buyer 1, bid 1 of buyer 1 ),
                (buyer 1, bid 2 of buyer 1),
                ...
                (buyer i, bid j of buyer i),
                ...
                (buyer n, bid n of buyer n)
            ]

        self.list_buyers_bids has type list due to constraints applied in
        __init__.

        :return: List[Tuple[int, float]]
        """
        list_tuples = []
        for ind, sublist_bids in enumerate(self.list_buyers_bids):
            list_tuples.extend([
                (ind, bid) for bid in sublist_bids
            ])
        return list_tuples

    def get_sorted_flat_list_tuples(self) -> List[Tuple[int, float]]:
        """
        Return the sorted list of tuples with respect to the second element
        (the bid) in ascending order.
        The index is also sorted to ensure consistency on indices in case of
        equality.

        :return: List[Tuple[int, float]]
        """
        return sorted(self.get_flat_list_tuples(),
                      key=lambda t: (t[1], t[0]))

    @staticmethod
    def get_winning_buyer(reserve_price: float,
                          sorted_flat_list_tuples: List[Tuple[int, float]]) -> \
            Optional[int]:
        """
        Compute the winning buyer based on the sorted list of all (buyer, bid)
        tuples.
        Returns the index of the buyer that has the highest bid, i.e. the last
        element of the list.
        Defaults to None in following cases:
            - if the input sorted list is empty
            - if the highest bid < reserve price

        :param reserve_price: float
        :param sorted_flat_list_tuples: List[Tuple[int, float]]
        :return: Optional[int], index of the winner buyer
        """
        w_buyer_index = None
        if len(sorted_flat_list_tuples) > 0:
            highest_bid_tuple = sorted_flat_list_tuples[-1]
            if highest_bid_tuple[1] >= reserve_price:
                w_buyer_index = highest_bid_tuple[0]
        return w_buyer_index

    @staticmethod
    def get_winning_price(reserve_price: float,
                          sorted_flat_list_tuples: List[Tuple[int, float]],
                          winning_buyer: Optional[int]) -> Optional[float]:
        """
        Returns the winning price of the auction, being the highest bid
        in the sorted list of tuples (or the reserve price if lower), where
        winner bids are filtered out.
        Defaults to None in following cases:
            - winning_buyer is None

        :param reserve_price: float
        :param sorted_flat_list_tuples: List[Tuple[int, float]]
        :param winning_buyer: Optional[int]
        :return: Optional[float], the winning price of the auction
        """
        winning_price = None

        if winning_buyer is not None:

            # There is a winner, so reserve_price at least will be applied
            winning_price = reserve_price

            # filter out winner bids from the sorted list to get highest bid
            # price from a non-winning buyer
            list_non_winner_bids = [
                tup for tup in sorted_flat_list_tuples
                if (tup[0] != winning_buyer)
            ]
            # The list is still sorted
            if len(list_non_winner_bids) > 0:
                # Get the last element (highest bid)
                highest_non_winner_bid = list_non_winner_bids[-1]
                winning_price = max(reserve_price,
                                    highest_non_winner_bid[1])

        return winning_price

    def get_winners(self) -> Tuple[Optional[int], Optional[float]]:
        """
        Return the winning buyer and price for the auction.

        :return: Tuple[Optional[int], Optional[float]], index of the winner and
        winning price
        """
        sorted_list = self.get_sorted_flat_list_tuples()
        winning_buyer = Auction.get_winning_buyer(self.reserve_price,
                                                  sorted_list)
        winning_price = Auction.get_winning_price(self.reserve_price,
                                                  sorted_list, winning_buyer)

        return winning_buyer, winning_price
