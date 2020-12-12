from auction import Auction

if __name__ == '__main__':
    # The auction from the example
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
        "Buyer #{} won the auction "
        "with the price {} "
        "(reserve price is {})\n".format(
            winning_buyer,
            winning_price,
            auction.reserve_price
        ))
