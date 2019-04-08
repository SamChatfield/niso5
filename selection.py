import logging

import population


def truncation(count, sorted_pop):
    return sorted_pop[:count].copy()
