import logging

import numpy as np

import util


class Strategy:
    def __init__(self, strategy):
        if type(strategy) == str:
            logging.debug('Strategy from str')
            (h, p, a, b) = Strategy._parse_str(strategy)
        elif (
            type(strategy) == tuple and
            len(strategy) == 4 and
            tuple(map(type, strategy)) == (int, np.ndarray, np.ndarray, np.ndarray)
        ):
            logging.debug('Strategy from tuple')
            (h, p, a, b) = strategy
        else:
            raise ValueError('Invalid strategy format, must be str or (h, p, a, b) tuple')

        self._h = h
        self._p = p
        self._a = a
        self._b = b
        logging.debug('H:\n%s\n', self._h)
        logging.debug('P:\n%s\n', self._p)
        logging.debug('A:\n%s\n', self._a)
        logging.debug('B:\n%s\n', self._b)

    @staticmethod
    def _parse_str(strategy_str):
        logging.debug('Strat Str: %s', strategy_str)
        strategy_parts = strategy_str.split()
        logging.debug('Strat Parts: %s', strategy_parts)

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

        return (h, np.array(p), np.array(a), np.array(b))

    @property
    def h(self):
        return self._h

    @property
    def p(self):
        return self._p

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    def _prob_for_state(self, state, crowded):
        # Bar crowded
        if crowded == 1:
            return self._a[state]
        # Bar not crowded
        elif crowded == 0:
            return self._b[state]
        # Invalid crowded value
        else:
            raise TypeError(f'Invalid argument crowded={crowded}')

    def _decision_for_state(self, state):
        r = np.random.uniform()
        p = self._p[state]
        return r < p

    def simulate_step(self, state, crowded, repetitions=1):
        # Find the probability distribution
        state_prob = self._prob_for_state(state, crowded)

        # Sample a state for
        states = util.sample(state_prob, repetitions)
        logging.debug('States:\n%s\n', states)

        decisions = np.fromiter((self._decision_for_state(s) for s in states), dtype=int)
        logging.debug('Decisions:\n%s\n', decisions)

        return np.column_stack((decisions, states))
