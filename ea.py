import logging
import math

import numpy as np

import crossover
import init
import mutation
import population
import selection


class EA:
    def __init__(self, lambda_, h, weeks,
                 mutation_chance=0.5, mutation_rate=None):
        logging.debug('Create EA object with lambda=%s, h=%s, weeks=%s', lambda_, h, weeks)
        self._lambda = lambda_
        self._h = h
        self._weeks = weeks

        self._mutation_chance = mutation_chance
        if mutation_rate is None:
            # Default mutation rate to 1 / num_genes, where num_genes is 3h
            self._mutation_rate = 1 / (3 * h)
        else:
            self._mutation_rate = mutation_rate

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
            logging.info('Attendance for gen %s:\n%.4f\n', gen, (mean_attendance / self._lambda))

            # Sort the population by payoffs
            sorted_pop = population.sorted_by_payoffs(self._population, payoffs)

            # Select parents
            parents = selection.truncation(self._num_parents, sorted_pop)

            # Generate children by crossover
            children = crossover.crossover(parents)

            logging.debug('POP BEFORE:\n%s\n', sorted_pop)
            sorted_pop[-children.size:] = children
            logging.debug('POP AFTER:\n%s\n', sorted_pop)

            # Mutation considering all individuals except the best
            logging.debug('POP BEFORE:\n%s\n', sorted_pop)
            sorted_pop[1:] = mutation.mutation(sorted_pop[1:], self._mutation_chance, self._mutation_rate)
            logging.debug('POP AFTER:\n%s\n', sorted_pop)

            self._population = sorted_pop

            assert self._population.size == self._lambda
