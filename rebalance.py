import sys
import csv
from decimal import *
from collections import namedtuple
import warnings

# Named tuple to hold instructions. This could be extended to hold more detailed machine readable
# data ie; transaction type, number of shares etc.
Instruction = namedtuple('Instruction', 'ticker instruction')


class Position:
    """Class for each position"""

    def __init__(self, *, ticker, shares, price, act_allocation, target_allocation):
        """Constructor assumes all fields are passed in as strings and the allocations in percentages"""
        self.ticker = ticker

        # If shares field is none or whitespace, assume 0 shares
        if not shares or not shares.strip():
            self.shares = 0
        else:
            self.shares = int(shares.strip())

        if not price or not price.strip():
            raise ValueError('Price of position {} must be greater than 0.'.format(ticker))

        self.price = Decimal(price.strip()[1:])
        if self.price <= 0:
            raise ValueError('Price of position {} must be greater than 0.'.format(ticker))

        # Assign 0 to act_allocation if none is provided (allow for initializing a portfolio and generating
        # first trade instructions
        if not act_allocation.strip():
            self.act_allocation = Decimal(0)
        else:
            self.act_allocation = Decimal(act_allocation[:-1]) / 100

        if not target_allocation.strip():
            raise ValueError('Target allocation of position {} required.'.format(ticker))
        self.target_allocation = Decimal(target_allocation[:-1]) / 100

    def __repr__(self):
        return "Ticker: {} Shares: {} Price: ${:.2f} Target Allocation: {:.2%} Actual Allocation: {:.2%}\n".format(
            self.ticker, self.shares, self.price, self.target_allocation, self.act_allocation)


class Portfolio:
    """Class for holding portfolios and performing rebalancing"""

    def __init__(self, positions):
        """Initialized with list of positions"""

        # Validate allocations
        if round(sum(position.target_allocation for position in positions), 2) != 1:
            raise ValueError("Target allocations must sum to 100%.")

        # Validate no duplicate symbols
        tickers = set(position.ticker for position in positions)
        if len(tickers) != len([position.ticker for position in positions]):
            raise ValueError("Duplicate tickers in position list")

        # Warn if actual allocations don't sum to 100% as they are not necessary to perform the rebalancing
        # Use this as a signal if input data is internally inconsistent
        if round(sum(position.act_allocation for position in positions), 2) != 1:
            warnings.warn("Actual allocations do not sum to 100%.")

        self.positions = positions
        self.value = Decimal(sum(position.price * position.shares for position in self.positions))

    def __repr__(self):
        return "Portfolio Value: ${:.2f} Positions: ".format(self.value) + str([position for position in
                                                                                self.positions])

    def rebalance(self):
        """Return a list of ticker names with sell/buy instructions"""

        # Loop through every position in the portfolio, compare actual value to target value.
        # Divide difference in value between the two by share price to get the number of shares needed to sell/buy
        # Round to the nearest share and append to list of instructions
        instructions = []

        # Note: There is not logic for making sure the set of transactions does not result in a net negative cash change
        for position in self.positions:
            # act_allocation isn't used here - in practical terms it isn't necessary to even import it
            # but I do so for completeness and the raising of errors may serve as a useful check to validate data
            actual_value = position.price * position.shares
            target_value = position.target_allocation * self.value

            shares_change = round((target_value - actual_value) / position.price, 0)
            if shares_change < 0:
                instructions.append(Instruction(position.ticker, "Sell {} shares of {}".format(-shares_change,
                                                                                               position.ticker)))
            elif shares_change > 0:
                instructions.append(Instruction(position.ticker, "Buy {} shares of {}".format(shares_change,
                                                                                              position.ticker)))
            else:
                instructions.append(Instruction(position.ticker, "No transaction necessary for {}".format(
                    position.ticker)))

        return instructions


def load_portfolio(csv_filename):
    """Function to load a portfolio csv file and return a portfolio object"""
    try:
        with open(csv_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            positions = []
            for row in reader:
                # This is messy, but gives the opportunity to quickly rewrite if we want a different csv file format
                positions.append(Position(ticker=row['Ticker'].strip(), shares=row['Shares owned'].strip(),
                                          price=row['Share price'],
                                          act_allocation=row['Actual allocation'],
                                          target_allocation=row['Target allocation'].strip()))

    except IOError:
        print("File not found")
        return None

    return Portfolio(positions)


# Script: opens target file, prints out the newly created portfolio then runs rebalance on the portfolio and prints
#  the list of instructions which will complete the rebalancing.
if __name__ == '__main__':
    port = load_portfolio(sys.argv[1])
    print('\n')
    print(port)
    print(port.rebalance())
