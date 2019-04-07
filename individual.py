import logging

import numpy as np

import strategy

class Individual:
    def __init__(self, strategy_obj):
        assert isinstance(strategy_obj, strategy.Strategy)
        self._strategy = strategy_obj
        self._fitness = None

    def simulate_step(self, state, crowded):
        logging.debug('Simulate step of ind where state=%s, crowded=%s', state, crowded)
        (decision, state) = self._strategy.simulate_step(state, crowded).flatten()
        return (decision, state)
