import argparse

import numpy as np


def _prob(prob_str):
    return np.array(list(map(float, prob_str.split(' '))))


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
    )
    parser.add_argument(
        '-debug',
        action='store_true'
    )
    return parser.parse_args()
