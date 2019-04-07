import logging
import math

import numpy as np

import individual
import strategy


def _ind_from_genes(genes):
    num_genes = len(genes)
    assert num_genes % 3 == 0
    # H
    h = int(num_genes / 3)
    # P
    p = np.array(genes[:h]).reshape(h)
    # A
    a = np.array(genes[h : 2*h])
    # B
    b = np.array(genes[2*h : 3*h])

    return individual.Individual(strategy.Strategy((h, p, a, b)))


def _uniform(p1, p2):
    p1_genes = p1.genes
    logging.debug('Parent1 genes:\n%s\n', p1_genes)
    p2_genes = p2.genes
    logging.debug('Parent2 genes:\n%s\n', p2_genes)

    assert len(p1_genes) == len(p2_genes)
    num_genes = len(p1_genes)
    assert num_genes % 3 == 0
    h = int(num_genes / 3)

    coin_flips = np.random.uniform(size=num_genes)
    logging.debug('Crossover coin flips:\n%s\n', coin_flips)

    c1_genes = []
    c2_genes = []

    for (c, p1g, p2g) in zip(coin_flips, p1_genes, p2_genes):
        logging.debug('Coin flip %s, p1g %s, p2g %s', c, p1g, p2g)
        if c < 0.5:
            # c1 gene <- p1, c2 gene <- p2
            c1_genes.append(p1g)
            c2_genes.append(p2g)
        else:
            # c1 gene <- p2, c2 gene <- p1
            c1_genes.append(p2g)
            c2_genes.append(p1g)

    logging.debug('Child1 genes:\n%s\n', c1_genes)
    logging.debug('Child2 genes:\n%s\n', c2_genes)

    c1 = _ind_from_genes(c1_genes)
    c2 = _ind_from_genes(c2_genes)

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
