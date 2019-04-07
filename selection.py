import logging

import population


def truncation(count, pop, payoffs):
    sorted_population = population.sorted_by_payoffs(pop, payoffs)
    return sorted_population[:count].copy()
