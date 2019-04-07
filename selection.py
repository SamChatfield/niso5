import logging


def truncation(num_parents, population, payoffs):
    sorted_population = population[payoffs.argsort()[::-1]]
    logging.debug('Population:\n%s\nSorted to:\n%s\nBy payoffs:\n%s\n', population, sorted_population, payoffs)
    return sorted_population[:num_parents].copy()
