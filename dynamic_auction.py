from copy import copy
from typing import Optional, Tuple


class BadFormatException(Exception):
    pass


class Bid(object):
    """
    A bid refers to a bid amount (euros), and a buyer (index)
    """

    def __init__(self,
                 buyer_id: int,
                 bid_value: float):
        """
        Constructor.
        Check parameters' format and raise BadFormatException accordingly.

        :param buyer_id: int, index of the buyer
        :param bid_value: float, amount of the bid
        """
        if buyer_id < 0 or not isinstance(buyer_id, int):
            raise BadFormatException(
                "buyer_id should be a strictly positive int.")
        if bid_value < 0 or not isinstance(bid_value, float):
            raise BadFormatException(
                "bid_value should be a positive float.")

        self.buyer_id = buyer_id
        self.bid_value = bid_value


class DynamicAuction(object):
    """
    TODO: add unit tests for this section

    Class representing the dynamic auction:
        - the reserve price for the object
        - the number of potential buyers
        - the highest bid that has been made in the auction to date
        - the second highest bid that has been made in the auction to date from
        a non-winning buyer
    """

    def __init__(self,
                 reserve_price: float,
                 nb_buyers: int):
        """
        Constructor.
        Check parameters' format and raise BadFormatException accordingly.

        :param reserve_price: float, reserve price of the object
        :param nb_buyers: int, total number of buyers in the auction
        """
        if reserve_price < 0 or not isinstance(reserve_price, float):
            raise BadFormatException(
                "reserve_price should be a positive float.")
        if nb_buyers <= 0 or not isinstance(nb_buyers, int):
            raise BadFormatException(
                "nb_buyers should be a strictly positive integer.")

        self.reserve_price = reserve_price
        self.nb_buyers = nb_buyers
        # Init state
        self.current_highest_bid: Bid = Bid(0, 0.0)
        self.current_second_highest_bid: Bid = Bid(0, 0.0)

    def add_bid(self, bid: Bid) -> None:
        """
        Place a bid (update the state of the auction)

        :param bid: Bid
        :return:
        """
        if bid.buyer_id < self.nb_buyers:
            self.update_state(bid)

    def update_state(self, bid: Bid) -> None:
        """
        [NOT TESTED] Update the state of the auction.

        :param bid: Bid
        :return:
        """
        if bid.bid_value >= self.current_highest_bid.bid_value:
            if bid.buyer_id == self.current_highest_bid.buyer_id:
                self.current_highest_bid = copy(bid)
            else:
                self.current_second_highest_bid = copy(self.current_highest_bid)
                self.current_highest_bid = copy(bid)
        elif bid.bid_value >= self.current_second_highest_bid.bid_value:
            if bid.buyer_id == self.current_highest_bid.buyer_id:
                # do nothing
                pass
            else:
                self.current_second_highest_bid = copy(bid)

    def get_winner_buyer(self) -> Optional[int]:
        """
        Return the current winner buyer of the auction by retrieving the current
        highest bid buyer stored in state.

        :return: Optional[int]
        """
        winner_buyer = None
        if isinstance(self.current_highest_bid, Bid):
            winner_buyer = self.current_highest_bid.buyer_id
        return winner_buyer

    def get_winner_price(self) -> Optional[float]:
        """
        Return the current winner price of the auction by retrieving the current
        second highest bid from non-winner stored in state.

        :return: Optional[float]
        """
        winner_price = None
        if self.get_winner_buyer() is not None:
            winner_price = self.reserve_price
        if isinstance(self.current_second_highest_bid, Bid):
            winner_price = max(self.reserve_price,
                               self.current_second_highest_bid.bid_value)
        return winner_price

    def get_winners(self) -> Tuple[Optional[int], Optional[float]]:
        """
        Return the tuple (winner buyer, winner price) based on the current
        state of the auction.

        :return: Tuple[Optional[int], Optional[float]]
        """
        return self.get_winner_buyer(), self.get_winner_price()
