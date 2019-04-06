import numpy as np

import strategy

def test_strategy():
    s = strategy.Strategy('2 0.1 0.0 1.0 1.0 0.0 1.0 0.9 0.1 0.9 0.1')

    assert s._h == 2
    assert np.array_equal(s._p, [0.1, 1.0])
    assert np.array_equal(s._a, [
        [0.0, 1.0],
        [0.9, 0.1]
    ])
    assert np.array_equal(s._b, [
        [1.0, 0.0],
        [0.9, 0.1]
    ])

def test_strategy_prob_for_state():
    s = strategy.Strategy('2 0.1 0.0 1.0 1.0 0.0 1.0 0.9 0.1 0.9 0.1')

    assert np.array_equal(
        s.prob_for_state(0, 0),
        [1.0, 0.0]
    )
    assert np.array_equal(
        s.prob_for_state(0, 1),
        [0.0, 1.0]
    )
    assert np.array_equal(
        s.prob_for_state(1, 0),
        [0.9, 0.1]
    )
    assert np.array_equal(
        s.prob_for_state(1, 1),
        [0.9, 0.1]
    )
