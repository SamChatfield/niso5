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
                 parent_proportion=0.25,
                 mutation_chance=0.5, mutation_rate=None):
        logging.debug('Create EA object with lambda=%s, h=%s, weeks=%s', lambda_, h, weeks)
        self._lambda = lambda_
        self._h = h
        self._weeks = weeks

        self._mutation_chance = mutation_chance
        # Default mutation rate of 1 / num_genes (where num_genes = 3h)
        self._mutation_rate = 1 / (3 * h) if mutation_rate is None else mutation_rate

        self._num_parents = max(2, math.floor(lambda_ * parent_proportion))

        # Initialise population
        self._population = init.initialise(lambda_, h)

    def run(self, generations):
        logging.debug('Running for %s generations', generations)

        # Compute initial payoffs (fitness evaluation)
        gen = 0
        logging.debug('GEN %s', gen)
        (payoffs, mean_attendance) = population.simulate(gen, self._population, self._weeks)
        logging.info('Payoffs for gen %s:\n%s', gen, payoffs)
        logging.info('Attendance for gen %s:\n%.4f\n', gen, (mean_attendance / self._lambda))

        # Sort the initial population by payoffs
        self._population = population.sorted_by_payoffs(self._population, payoffs)

        for gen in range(1, generations):
            logging.debug('GEN %s', gen)
            new_pop = self._population.copy()

            # Select parents
            parents = selection.truncation(self._num_parents, new_pop)

            # Generate children by crossover
            children = crossover.crossover(parents)
            # Replace worst solutions in the population with children
            new_pop[-children.size:] = children

            # Mutation considering all individuals except the best
            new_pop[1:] = mutation.mutation(new_pop[1:], self._mutation_chance, self._mutation_rate)

            # Compute payoffs of new population
            (payoffs, mean_attendance) = population.simulate(gen, new_pop, self._weeks)
            logging.info('Payoffs for gen %s:\n%s', gen, payoffs)
            logging.info('Attendance for gen %s:\n%.4f\n', gen, (mean_attendance / self._lambda))

            # Sort the new population by payoffs
            sorted_pop = population.sorted_by_payoffs(new_pop, payoffs)

            self._population = sorted_pop
            assert self._population.size == self._lambda

        return mean_attendance
