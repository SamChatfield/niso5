import logging
import math

import numpy as np

import individual
import strategy


def _uniform(p1, p2):
    p1_genes = p1.genes
    logging.debug('Parent1 genes:\n%s\n', p1_genes)
    p2_genes = p2.genes
    logging.debug('Parent2 genes:\n%s\n', p2_genes)

    assert len(p1_genes) == len(p2_genes)
    num_genes = len(p1_genes)

    coin_flips = np.random.binomial(1, 0.5, size=num_genes)
    logging.debug('Crossover coin flips:\n%s\n', coin_flips)

    c1_genes = []
    c2_genes = []

    for (c, p1g, p2g) in zip(coin_flips, p1_genes, p2_genes):
        if c == 0:
            # c1 gene <- p1, c2 gene <- p2
            c1_genes.append(p1g)
            c2_genes.append(p2g)
        elif c == 1:
            # c1 gene <- p2, c2 gene <- p1
            c1_genes.append(p2g)
            c2_genes.append(p1g)
        else:
            raise Exception(f'Invalid coin flip value {c} not in [0, 1]')

    logging.debug('Child1 genes:\n%s\n', c1_genes)
    logging.debug('Child2 genes:\n%s\n', c2_genes)

    c1 = individual.from_genes(c1_genes)
    c2 = individual.from_genes(c2_genes)

    return (c1, c2)


def crossover(parents, method='uniform'):
    logging.debug('Crossover for parents:\n%s\n', parents)

    num_children = math.floor(parents.size / 2) * 2
    children = np.empty(shape=num_children, dtype=parents.dtype)

    if method == 'uniform':
        for i, (p_a, p_b) in enumerate(zip(parents[::2], parents[1::2])):
            logging.debug('Crossover pair %s (%s, %s)', i, p_a, p_b)
            (c_a, c_b) = _uniform(p_a, p_b)
            logging.debug('Child pair (%s, %s)', c_a, c_b)
            children[2*i] = c_a
            children[2*i+1] = c_b
    else:
        raise ValueError(f'Invalid crossover method given: {method}')

    logging.debug('Generated children:\n%s\n', children)
    return children
