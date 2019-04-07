import logging
import math

import numpy as np

import crossover
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
            (payoffs, mean_attendance) = population.simulate(gen, self._population, self._weeks)
            logging.info('Payoffs for gen %s:\n%s', gen, payoffs)
            logging.info('Attendance for gen %s:\n%s\n', gen, mean_attendance)

            # Select parents
            parents = selection.truncation(self._num_parents, self._population, payoffs)

            # Generate children by crossover
            children = crossover.crossover(parents)

            new_pop = population.sorted_by_payoffs(self._population, payoffs)
            logging.debug('POP BEFORE:\n%s\n', new_pop)
            new_pop[-children.size:] = children
            logging.debug('POP AFTER:\n%s\n', new_pop)

            self._population = new_pop

            assert self._population.size == self._lambda
