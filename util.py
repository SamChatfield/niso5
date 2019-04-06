import logging

import numpy as np


def sample(prob, repetitions=1):
    logging.debug('Sample with %s reps from:\n%s\n', repetitions, prob)
    return np.random.choice(len(prob), size=repetitions, replace=True, p=prob)
