import logging

import numpy as np

import strategy

class Individual:
    def __init__(self, strategy_obj):
        assert isinstance(strategy_obj, strategy.Strategy)
        self._strategy = strategy_obj
        self._genes = self._compute_genes()

    @property
    def h(self):
        return self._strategy.h

    @property
    def genes(self):
        # The list of genes is the concatenation of P, A and B
        # Each element in p is a gene, and each row in A and B are genes
        return self._genes

    def _compute_genes(self):
        p = self._strategy.p.copy()
        p_genes = np.reshape(p, (p.size, 1))
        a_genes = self._strategy.a.copy()
        b_genes = self._strategy.b.copy()
        return list(p_genes) + list(a_genes) + list(b_genes)

    def simulate_step(self, state, crowded):
        logging.debug('Simulate step of ind where state=%s, crowded=%s', state, crowded)
        (decision, state) = self._strategy.simulate_step(state, crowded).flatten()
        return (decision, state)


def from_genes(genes):
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

    return Individual(strategy.Strategy((h, p, a, b)))
