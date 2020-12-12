# Teads - development test

## Problem statement

Let's consider a second-price, sealed-bid auction:
An object is for sale with a reserve price.
We have several potential buyers, each one being able to place one or more bids.
The buyer winning the auction is the one with the highest bid above or equal to the reserve price.
The winning price is the highest bid price from a non-winning buyer above the reserve price (or the reserve price if none applies)

## Example
Consider 5 potential buyers (A, B, C, D, E) who compete to acquire an object with a reserve price set at 100 euros, bidding as follows:

```
    A: 2 bids of 110 and 130 euros
    B: 0 bid
    C: 1 bid of 125 euros
    D: 3 bids of 105, 115 and 90 euros
    E: 3 bids of 132, 135 and 140 euros
```

The buyer E wins the auction at the price of 130 euros.

## Goal
The goal is to implement an algorithm for finding the winner and the winning price. Please implement the solution in the language of your choice. Tests should be separated from your algorithm. We should be able to build and run your solution locally.

Send a zip file with your code to technical-test@teads.tv with the following subject: "HR Test: <position> <firstname>".
Ex: "HR Test: Backend Bob"

## Solution

### Auction parameters

The auction is described with the following parameters:

- a reserve price for the object to sell
- a list of buyers, and for each buyer, the list of bids

This object is represented by the `Auction` class defined in `./auction.py`

### Discovering the winning buyer and price

We use the following flattened list of `(buyer #i, bid #j)` tuples:

	[
	    (buyer 1, bid 1 of buyer 1 ),
	    (buyer 1, bid 2 of buyer 1),
	    ...
	    (buyer i, bid j of buyer i),
	    ...
	    (buyer n, bid n of buyer n)
	]

We propose the following steps to solve the problem:

- create the list of all `(buyer #i, bid #j)` tuples from the auction parameters;
- sort the list in ascending order of the `bid` (and underlying ascending order of the buyer index)
- the last element of this list gives the winning buyer index if related bid verifies `bid >= reserve price`;
- then, filter out the winning buyer from the list. The list is still sorted in ascending order of the `bid` (and underlying ascending order of the buyer index)
- if the list is not empty, the last element of the list gives the winning price, precisely we return `max(bid, reserve price)`. Else, we return the reserve price as the winning price.

#### Remarks:

- if 2 buyers have equal highest bids, then the highest buyer index is the winner (convention). Alternatively, we could randomly select the winner among the candidates;
- if a winner buyer is not found (None), the following steps are skipped;
- sorting is the most computationally greedy step;


### Code structure

- `./README.md`: the current markdown document;
- `./teads-hw.py`: the main of the repo;
- `./auction.py`: defines the `Auction` class;
- `./utils.py`: tooling methods for the problem;
- `./tests`: tests directory.

### Run the code

#### Prerequisites:

 - a Python 3.7 interpreter

#### Run tests

```
cd path/to/teads-hw
python3.7 -m unittest tests/*.py
```

#### Run the algorithm

Alter the auction parameters, in `./teads-hw.py`, to fit the auction to test.
Parameters defaults to the auction given as an example:

```
auction = Auction(
    100.0,
    [
        [110.0, 130.0],
        [0.0],
        [125.0],
        [105.0, 115.0, 90.0],
        [132.0, 135.0, 140.0]
    ])
```

Then, in your terminal:

```
cd path/to/teads-hw
python3.7 teads-hw.py
```


