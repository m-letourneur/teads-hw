from auction import Auction
from dynamic_auction import DynamicAuction, Bid

if __name__ == '__main__':
    print("""\nStatic implementation: compute the result at the end of the auction based on the entire description of the auction.""")
    auction = Auction(
        100.0,
        [
            [110.0, 130.0],
            [],
            [125.0],
            [105.0, 115.0, 90.0],
            [132.0, 135.0, 140.0]
        ])

    # Compute winners: buyer and price
    winning_buyer, winning_price = auction.get_winners()
    print(
        ">> Buyer #{} won the auction "
        "with the price {} "
        "(reserve price is {})\n".format(
            winning_buyer,
            winning_price,
            auction.reserve_price
        ))

    print("""\n\nDynamic implementation of the auction""")
    # Init the auction
    dynamic_auction = DynamicAuction(
        100.0,
        5
    )

    # Place bids dynamically
    dynamic_auction.add_bid(Bid(4, 132.0))
    dynamic_auction.add_bid(Bid(3, 105.0))
    dynamic_auction.add_bid(Bid(2, 125.0))
    dynamic_auction.add_bid(Bid(0, 130.0))
    dynamic_auction.add_bid(Bid(0, 110.0))
    dynamic_auction.add_bid(Bid(3, 115.0))
    dynamic_auction.add_bid(Bid(4, 135.0))
    dynamic_auction.add_bid(Bid(3, 90.0))
    dynamic_auction.add_bid(Bid(4, 140.0))

    winning_buyer, winning_price = dynamic_auction.get_winners()
    print(
        ">> Buyer #{} won the dynamic auction "
        "with the price {} "
        "(reserve price is {})\n".format(
            winning_buyer,
            winning_price,
            auction.reserve_price
        ))
