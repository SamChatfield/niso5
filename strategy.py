import logging

import numpy as np

import util


class Strategy:
    def __init__(self, strategy_str):
        logging.warning('Strat Str: %s', strategy_str)
        strategy_parts = strategy_str.split()
        logging.warning('Strat Parts: %s', strategy_parts)

        # H - number of states
        h = int(strategy_parts[0])

        # P - attendance probability vector
        row_step = h * 2 + 1
        p = list(map(float, strategy_parts[1::row_step]))

        # A and B state transition matrices
        # Build up the A and B matrices one row at a time over [0, h)
        a, b = [], []
        for i in range(h):
            # Find the start (incl.) and end (excl.) points for A_i
            a_i_start = 2 + i * row_step
            a_i_stop = 2 + i * row_step + h
            # Extract A_i and add to A
            a_i = list(map(float, strategy_parts[a_i_start : a_i_stop]))
            a.append(a_i)

            # Find the start (incl.) and end (excl.) points for B_i
            b_i_start = 2 + h + i * row_step
            b_i_stop = 2 + h + i * row_step + h
            # Extract B_i and add to B
            b_i = list(map(float, strategy_parts[b_i_start : b_i_stop]))
            b.append(b_i)

        self._h = h
        self._p = np.array(p)
        self._a = np.array(a)
        self._b = np.array(b)

        logging.warning('H:\n%s\n', self._h)
        logging.warning('P:\n%s\n', self._p)
        logging.warning('A:\n%s\n', self._a)
        logging.warning('B:\n%s\n', self._b)

    def prob_for_state(self, state, crowded):
        # Bar crowded
        if crowded == 1:
            return self._a[state]
        # Bar not crowded
        elif crowded == 0:
            return self._b[state]
        # Invalid crowded value
        else:
            raise TypeError(f'Invalid argument crowded={crowded}')

    def decision_for_state(self, state):
        return np.random.uniform() < self._p[state]

    def simulate_step(self, state, crowded, repetitions=1):
        # Find the probability distribution
        state_prob = self.prob_for_state(state, crowded)
        logging.debug('prob for state=%s, crowded=%s:\n%s\n', state, crowded, state_prob)

        # Sample a state for
        states = util.sample(state_prob, repetitions)
        logging.debug('states:\n%s\n', states)

        decisions = np.fromiter((self.decision_for_state(s) for s in states), dtype=int)
        logging.debug('decisions:\n%s\n', decisions)

        return np.column_stack((decisions, states))
