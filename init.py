import logging

import numpy as np

import individual
import strategy


def _random_strategy(h):
    # Create random p vector
    p = np.random.uniform(size=h)
    logging.debug('P:\n%s\n', p)

    # Create random A transition matrix where rows sum to 1.0
    a = np.random.dirichlet(np.ones(h), size=h)
    logging.debug('A (sum=%s):\n%s\n', a.sum(axis=1), a)
    assert np.allclose(a.sum(axis=1), np.ones(h))

    # Create random B transition matrix where rows sum to 1.0
    b = np.random.dirichlet(np.ones(h), size=h)
    logging.debug('B (sum=%s):\n%s\n', b.sum(axis=1), b)
    assert np.allclose(b.sum(axis=1), np.ones(h))

    return strategy.Strategy((h, p, a, b))

def initialise(lambda_, h):
    logging.debug('Initialise population with lambda=%s, h=%s', lambda_, h)

    population = np.empty(lambda_, dtype=object)
    for i in range(lambda_):
        logging.debug('Individual %s', i)
        population[i] = individual.Individual(_random_strategy(h))

    logging.debug('Generated pop:\n%s\n', population)
    assert population.size == lambda_

    return population
