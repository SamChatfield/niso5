import argparse

import numpy as np

import strategy


def _prob(prob_str):
    return np.array(list(map(float, prob_str.split(' '))))


def _strategy(strategy_str):
    return strategy.Strategy(strategy_str)


def parse():
    parser = argparse.ArgumentParser(
        description='NISO Lab 5'
    )
    parser.add_argument(
        '-question',
        type=int,
        required=True
    )
    parser.add_argument(
        '-prob',
        type=_prob
    )
    parser.add_argument(
        '-repetitions',
        type=int
    ),
    parser.add_argument(
        '-strategy',
        type=_strategy
    ),
    parser.add_argument(
        '-state',
        type=int
    ),
    parser.add_argument(
        '-crowded',
        type=int
    ),
    parser.add_argument(
        '-debug',
        action='store_true'
    )
    return parser.parse_args()
