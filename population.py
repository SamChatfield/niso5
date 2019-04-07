import logging

import numpy as np


def simulate(gen, population, weeks):
    logging.debug('Simulating population over %s weeks', weeks)
    # Start with the bar not crowded and all individuals in state 0
    crowded = 0
    states = np.zeros(population.size, dtype=int)
    payoffs = np.zeros(population.size, dtype=int)

    for w in range(weeks):
        logging.debug('WEEK %s\n', w)
        # Calculate the decisions and states for each individual for week t+1
        new_decisions = np.empty(population.size, dtype=int)
        new_states = np.empty(population.size, dtype=int)
        for (idx, ind) in enumerate(population):
            (d, s) = ind.simulate_step(states[idx], crowded)
            new_decisions[idx] = d
            new_states[idx] = s
        logging.debug('New decisions:\n%s\n', new_decisions)
        logging.debug('New states:\n%s\n', new_states)

        # Is the bar crowded?
        d_sum = new_decisions.sum()
        new_crowded = int(d_sum >= 0.6 * population.size)
        logging.debug('New crowded: %s', new_crowded)

        # Set payoffs
        for (idx, ind) in enumerate(population):
            d = new_decisions[idx]
            if (
                (d == 1 and new_crowded == 0) or
                (d == 0 and new_crowded == 1)
            ):
                logging.debug('Ind %s, d=%s, c=%s => payoff += 1', idx, d, new_crowded)
                payoffs[idx] += 1
            else:
                logging.debug('Ind %s, d=%s, c=%s => no payoff', idx, d, new_crowded)
        logging.debug('Payoffs:\n%s\n', payoffs)
        new_decisions_str = '\t'.join([str(d) for d in new_decisions])
        print(f'{w}\t{gen}\t{d_sum}\t{new_crowded}\t{new_decisions_str}')

        # Update crowded flag and states array for next week
        crowded = new_crowded
        states = new_states

    return payoffs


def sort_by_fitness(population):
    pass
