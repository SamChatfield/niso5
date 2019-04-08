import logging

import numpy as np

import individual


def _random_gene(h, size):
    if size == 1:
        p_gene = np.random.uniform(size=1)
        logging.debug('New random P gene: %s', p_gene)
        return p_gene
    elif size == h:
        ab_gene = np.random.dirichlet(np.ones(h))
        logging.debug('New random A/B gene: %s', ab_gene)
        return ab_gene
    else:
        raise Exception(f'Invalid gene size: {size}')


def _gene_replacement(ind, mutation_rate):
    ind_genes = ind.genes
    logging.debug('Ind genes:\n%s\n', ind_genes)

    num_genes = len(ind_genes)
    assert num_genes % 3 == 0
    h = int(num_genes / 3)

    probs = np.random.uniform(size=num_genes)
    logging.debug('Mutation probabilities:\n%s\n', probs)

    new_ind_genes = []

    for (p, ind_gene) in zip(probs, ind_genes):
        if p < mutation_rate:
            # Mutate gene
            new_ind_genes.append(_random_gene(h, ind_gene.size))
        else:
            # Copy gene
            new_ind_genes.append(ind_gene)

    logging.debug('New ind genes:\n%s\n', new_ind_genes)

    return individual.from_genes(new_ind_genes)


def mutation(individuals, mutation_chance, mutation_rate, method='gene_replacement'):
    new_individuals = individuals.copy()
    logging.debug('Mutation for individuals:\n%s\n', new_individuals)

    if method == 'gene_replacement':
        for idx, ind in enumerate(new_individuals):
            if np.random.uniform() < mutation_chance:
                logging.debug('Mutate ind %s (%s)', idx, ind)
                new_ind = _gene_replacement(ind, mutation_rate)
                logging.debug('Mutated to: %s', new_ind)
                new_individuals[idx] = new_ind
            else:
                logging.debug('Skip ind %s (%s', idx, ind)
    else:
        raise ValueError(f'Invalid crossover method given: {method}')

    return new_individuals