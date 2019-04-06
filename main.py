import logging
import random
import sys

import numpy as np

import arg_parser
import util

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.WARNING)


def question1(prob, repetitions):
    results = util.sample(prob, repetitions)
    logging.debug('For prob=%s, rep=%s, Got: %s, type: %s', prob, repetitions, results, type(results))
    return results


def question2(strategy, state, crowded, repetitions):
    results = strategy.simulate_step(state, crowded, repetitions)
    logging.debug('For strategy=%s, state=%s, crowded=%s, rep=%s\nGot: %s, type: %s', strategy, state, crowded, repetitions, results, type(results))
    return results


def main():
    args = arg_parser.parse()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.question == 1:
        logging.debug('question 1:')
        results = question1(args.prob, args.repetitions)
        for r in results:
            print(r)
    elif args.question == 2:
        logging.debug('question 2')
        results = question2(args.strategy, args.state, args.crowded, args.repetitions)
        for r in results:
            print(f'{r[0]}\t{r[1]}')
    elif args.question == 3:
        logging.debug('question 3')
    else:
        logging.error('Invalid question number supplied')
        sys.exit(1)


if __name__ == '__main__':
    main()
