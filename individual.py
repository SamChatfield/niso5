import logging

import numpy as np

import strategy

class Individual:
    def __init__(self, strategy_obj):
        assert isinstance(strategy_obj, strategy.Strategy)
        self._strategy = strategy_obj
        self._fitness = None

    @property
    def h(self):
        return self._strategy.h

    @property
    def genes(self):
        # The list of genes is the concatenation of P, A and B
        # Each element in p is a gene, and each row in A and B are genes
        p = self._strategy.p.copy()
        p_genes = np.reshape(p, (p.size, 1))
        a_genes = self._strategy.a.copy()
        b_genes = self._strategy.b.copy()
        return list(p_genes) + list(a_genes) + list(b_genes)

    def simulate_step(self, state, crowded):
        logging.debug('Simulate step of ind where state=%s, crowded=%s', state, crowded)
        (decision, state) = self._strategy.simulate_step(state, crowded).flatten()
        return (decision, state)
