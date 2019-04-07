import logging
import math

import init
import population
import selection


class EA:
    def __init__(self, lambda_, h, weeks):
        logging.debug('Create EA object with lambda=%s, h=%s, weeks=%s', lambda_, h, weeks)
        self._lambda = lambda_
        self._h = h
        self._weeks = weeks

        self._num_parents = max(2, math.floor(lambda_ * 0.25))

        # Initialise population
        self._population = init.initialise(lambda_, h)


    def run(self, generations):
        logging.debug('Running for %s generations', generations)

        for gen in range(generations):
            logging.debug('GEN %s', gen)

            # Compute payoffs (fitness evaluation)
            payoffs = population.simulate(gen, self._population, self._weeks)

            # Select parents
            parents = selection.truncation(self._num_parents, self._population, payoffs)
