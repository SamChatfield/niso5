import logging
import random
import sys

import numpy as np

import arg_parser

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.WARNING)


def _sample(prob, repetitions):
    return np.random.choice(len(prob), size=repetitions, replace=True, p=prob)


def question1(prob, repetitions):
    res = _sample(prob, repetitions)
    logging.debug('For prob=%s, rep=%s, Got: %s, type: %s', prob, repetitions, res, type(res))
    return res


def main():
    args = arg_parser.parse()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.question == 1:
        logging.debug('question 1:')
        # print(question1(args.prob, args.repetitions))
        res = question1(args.prob, args.repetitions)
        for r in res:
            print(r)
    elif args.question == 2:
        logging.debug('question 2')
    elif args.question == 3:
        logging.debug('question 3')
    else:
        logging.error('Invalid question number supplied')
        sys.exit(1)


if __name__ == '__main__':
    main()
