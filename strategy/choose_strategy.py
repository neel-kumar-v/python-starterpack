from strategy.random_strategy import RandomStrategy
from strategy.strategy import Strategy


def choose_strategy() -> Strategy:
    # Modify what is returned here to select the strategy your bot will use

    return RandomStrategy()
