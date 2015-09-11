import unittest
from rebalance import *

TESTING_DIRECTORY = 'test_files/'


class TestRebalanceModule(unittest.TestCase):
    def test_instructions(self):
        # Test to verify the example portfolio generates correct instructions
        portfolio = load_portfolio(TESTING_DIRECTORY + 'portfolio.csv')
        instructions = portfolio.rebalance()
        self.assertEqual(instructions[0], Instruction(ticker='GOOG', instruction='Buy 9 shares of GOOG'))
        self.assertEqual(instructions[1], Instruction(ticker='AAPL', instruction='No transaction necessary for AAPL'))
        self.assertEqual(instructions[2], Instruction(ticker='TSLA', instruction='Sell 114 shares of TSLA'))

        # Test to verify a portfolio with zero initial shares generates correct instructions
        portfolio = load_portfolio(TESTING_DIRECTORY + 'portfolio_no_shares.csv')
        instructions = portfolio.rebalance()
        self.assertEqual(instructions[0], Instruction(ticker='GOOG', instruction='Sell 11 shares of GOOG'))
        self.assertEqual(instructions[1], Instruction(ticker='AAPL', instruction='No transaction necessary for AAPL'))
        self.assertEqual(instructions[2], Instruction(ticker='TSLA', instruction='Sell 114 shares of TSLA'))
        self.assertEqual(instructions[3], Instruction(ticker='FOO', instruction='Buy 40 shares of FOO'))
        self.assertEqual(instructions[4], Instruction(ticker='BAR', instruction='Buy 148 shares of BAR'))

    # Test to verify exception raised for invalid target allocation
    def test_invalid_target(self):
        with self.assertRaises(ValueError) as cm:
            load_portfolio(TESTING_DIRECTORY + 'invalid_target_portfolio.csv')
        self.assertEqual(str(cm.exception), 'Target allocations must sum to 100%.')

    # Test to verify warning raised for invalid actual allocation
    def test_invalid_actual(self):
        with self.assertWarns(UserWarning) as cm:
            load_portfolio(TESTING_DIRECTORY + 'invalid_actual_portfolio.csv')
        self.assertEqual(str(cm.warning), 'Actual allocations do not sum to 100%.')

    # Test to verify warning raised if a target allocation is missing
    def test_missing_target(self):
        with self.assertRaises(ValueError) as cm:
            load_portfolio(TESTING_DIRECTORY + 'missing_target_portfolio.csv')
        self.assertEqual(str(cm.exception), 'Target allocation of position AAPL required.')

    # Test to verify there are no zero prices
    def test_zero_price(self):
        with self.assertRaises(ValueError) as cm:
            load_portfolio(TESTING_DIRECTORY + 'missing_price_portfolio.csv')
        self.assertEqual(str(cm.exception), 'Price of position GOOG must be greater than 0.')

    # Test to verify a portfolio with duplicated tickers throws an exception
    def test_duplicate_tickers(self):
        with self.assertRaises(ValueError) as cm:
            load_portfolio(TESTING_DIRECTORY + 'duplicate_tickers_portfolio.csv')
        self.assertEqual(str(cm.exception), "Duplicate tickers in position list")


if __name__ == '__main__':
    unittest.main()
