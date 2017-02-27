#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
quarkball2017: tests for base classes
"""

# ======================================================================
# :: Imports
from __future__ import (
    division, absolute_import, print_function, unicode_literals)

import os
import datetime
import shutil
import multiprocessing

import numpy as np

from quarkball.utils import Network, Caching
import quarkball.fill_caching as fill

DIRPATH = 'data'
IN_DIRPATH = os.path.join(DIRPATH, 'input')
OUT_DIRPATH = os.path.join(DIRPATH, 'output')
SOURCES = (
    'kittens', 'me_at_the_zoo', 'trending_today', 'videos_worth_spreading',)


# ======================================================================
def test_network_input(
        in_dirpath=IN_DIRPATH,
        sources=SOURCES):
    for source in sources:
        in_filepath = os.path.join(in_dirpath, source + '.in')
        network = Network.load(in_filepath)
        print(network)


# ======================================================================
def test_caching_output(
        in_dirpath=OUT_DIRPATH,
        source='example'):
    in_filepath = os.path.join(in_dirpath, source + '.out')
    caching = Caching.load(in_filepath)
    print(caching)
    out_filepath = os.path.join(in_dirpath, 'test_' + source)
    caching.save(out_filepath)


# ======================================================================
def test_score(
        in_dirpath=IN_DIRPATH,
        out_dirpath=OUT_DIRPATH,
        source='example'):
    in_filepath = os.path.join(in_dirpath, source + '.in')
    network = Network.load(in_filepath)
    print(network)
    out_filepath = os.path.join(out_dirpath, source + '.out')
    caching = Caching.load(out_filepath)
    print(caching.score(network))


# ======================================================================
def test_fill(
        in_dirpath=IN_DIRPATH,
        out_dirpath=OUT_DIRPATH,
        source='example'):
    in_filepath = os.path.join(in_dirpath, source + '.in')
    network = Network.load(in_filepath)
    out_filepath = os.path.join(out_dirpath, source + '.out')
    caching = fill.CachingRandom(network.num_caches)
    caching.fill(network)
    print(repr(caching))
    print('Random Caching - Score: {}'.format(caching.score(network)))


# ======================================================================
def test_method(
        in_dirpath=IN_DIRPATH,
        out_dirpath=OUT_DIRPATH,
        source='example',
        caching_method=Caching,
        *fill_args,
        **fill_kws):
    if not os.path.isdir(out_dirpath):
        os.makedirs(out_dirpath)
    in_filepath = os.path.join(in_dirpath, source + '.in')
    network = Network.load(in_filepath)
    out_filepath = os.path.join(out_dirpath, source + '.out')
    caching = caching_method(network.num_caches)
    caching.fill(network, *fill_args, **fill_kws)
    caching.save(out_filepath)
    score = caching.score(network)
    print('{:20s} final score: {}'.format(source, score), flush=True)
    return score


# ======================================================================
def test_method_seq(
        in_dirpath=IN_DIRPATH,
        out_dirpath=OUT_DIRPATH,
        sources=SOURCES,
        caching_method=Caching,
        *fill_args,
        **fill_kws):
    if not os.path.isdir(out_dirpath):
        os.makedirs(out_dirpath)
    tot_score = 0
    for source in sources:
        in_filepath = os.path.join(in_dirpath, source + '.in')
        network = Network.load(in_filepath)
        out_filepath = os.path.join(out_dirpath, source + '.out')
        caching = caching_method(network.num_caches)
        caching.fill(network, *fill_args, **fill_kws)
        caching.save(out_filepath)
        score = caching.score(network)
        tot_score += score
        print('{:40s} score: {}'.format(source, score))
    print('\nTOTAL SCORE: {}\n'.format(tot_score))


# ======================================================================
def test_method_par(
        in_dirpath=IN_DIRPATH,
        out_dirpath=OUT_DIRPATH,
        sources=SOURCES,
        caching_method=Caching,
        *fill_args,
        **fill_kws):
    if not os.path.isdir(out_dirpath):
        os.makedirs(out_dirpath)
    tot_score = 0
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    results = []
    for source in sources:
        result = pool.apply_async(
            test_method,
            (in_dirpath, out_dirpath, source, caching_method,) + fill_args,
            fill_kws)
        results.append(result)
    for result in results:
        tot_score += result.get()
    print('\nTOTAL SCORE: {}\n'.format(tot_score))


# ======================================================================
def pseudo_monte_carlo(
        in_dirpath=IN_DIRPATH,
        out_dirpath=os.path.join(OUT_DIRPATH, 'pseudo_monte_carlo'),
        best_subpath='best',
        sources=SOURCES,
        caching_method=fill.CachingRandom,
        max_iter=int(1e8 - 1),
        min_score=2652000):
    print('Pseudo Monte Carlo simulation')
    best_dirpath = os.path.join(out_dirpath, best_subpath)
    if not os.path.isdir(best_dirpath):
        os.makedirs(best_dirpath)

    # read all networks
    print('Reading input...')
    networks = {}
    for source in sources:
        in_filepath = os.path.join(in_dirpath, source + '.in')
        networks[source] = Network.load(in_filepath)

    # find out the best score from previous iterations
    print('Reading best score...')
    max_scores = {}
    for source in sources:
        network = networks[source]
        best_filepath = os.path.join(best_dirpath, source + '.out')
        caching = Caching.load(best_filepath)
        max_scores[source] = caching.score(network)
        print('{}: {:>6d}'.format(source[:1], max_scores[source]), end=', ',
              flush=True)
    max_tot_score = sum(max_scores.values())
    print('T: {:>7d}'.format(max_tot_score))

    # explore the solution subspace randomly, saving best results
    print('Optimization [max_iter={}]...'.format(max_iter))
    j = 0
    batch_scores = []
    while j < max_iter and max_tot_score < min_score:
        print('{:>{}d} - '.format(j, int(np.log10(max_iter)) + 1),
              end='', flush=True)
        scores = {}
        for source in sources:
            network = networks[source]
            out_filepath = os.path.join(out_dirpath, source + '.out')
            caching = caching_method(network.num_caches)
            caching.fill(network)
            caching.save(out_filepath)
            scores[source] = caching.score(network)
            print('{}: {:>6d}'.format(source[:1], scores[source]), end=', ',
                  flush=True)
        tot_score = sum(scores.values())
        max_tot_score = sum(max_scores.values())
        print('T: {:7>d} ({:7>d})'.format(tot_score, max_tot_score))
        for source in sources:
            if scores[source] > max_scores[source]:
                src = os.path.join(out_dirpath, source + '.out')
                dst = os.path.join(best_dirpath, source + '.out')
                if os.path.isfile(dst):
                    os.remove(dst)
                shutil.copy(src, dst)
                print('{}: new max score found: {:>6d} ({:>6d})'.format(
                    source[:1], scores[source], max_scores[source]))
                max_scores[source] = scores[source]
        batch_scores.append(tot_score)
        j += 1

    print('\nStatistics (of current batch):')
    batch_scores = np.array(batch_scores)
    for f in ('min', 'max', 'mean', 'std', 'median'):
        print('{:>7s} = {}'.format(f, getattr(np, f)(batch_scores)))


# ======================================================================
def bruteforce(
        in_dirpath=IN_DIRPATH,
        out_dirpath=os.path.join(OUT_DIRPATH, 'bruteforce'),
        sources=SOURCES):
    print('Bruteforce')
    if not os.path.isdir(out_dirpath):
        os.makedirs(out_dirpath)
    tot_score = 0
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    results = []
    for source in sources:
        out_filepath = os.path.join(out_dirpath, source + '.out')
        results.append(pool.apply_async(
            test_method,
            (in_dirpath, out_dirpath, source, fill.CachingBruteForce,
             out_filepath)))
    for result in results:
        tot_score += result.get()
    print('\nTOTAL SCORE: {}\n'.format(tot_score))


# ======================================================================
def montecarlo(
        in_dirpath=IN_DIRPATH,
        out_dirpath=os.path.join(OUT_DIRPATH, 'montecarlo'),
        sources=SOURCES,
        max_iter=int(1e8 - 1)):
    print('Montecarlo')
    if not os.path.isdir(out_dirpath):
        os.makedirs(out_dirpath)
    tot_score = 0
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    results = []
    for source in sources:
        out_filepath = os.path.join(out_dirpath, source + '.out')
        results.append(pool.apply_async(
            test_method,
            (in_dirpath, out_dirpath, source, fill.CachingMonteCarlo,
             out_filepath, max_iter)))
    for result in results:
        tot_score += result.get()
    print('\nTOTAL SCORE: {}\n'.format(tot_score))


# ======================================================================
def evolution(
        in_dirpath=IN_DIRPATH,
        out_dirpath=os.path.join(OUT_DIRPATH, 'evolution'),
        sources=SOURCES,
        max_generations=int(1e8 - 1),
        pool_size=200,
        selection=0.5,
        crossover=0.6,
        mutation_rate=0.05,
        mutation=0.1,
        elitism=0.005):
    print('Evolution')
    if not os.path.isdir(out_dirpath):
        os.makedirs(out_dirpath)
    tot_score = 0
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    results = []
    for source in sources:
        out_filepath = os.path.join(out_dirpath, source + '.out')
        results.append(pool.apply_async(
            test_method,
            (in_dirpath, out_dirpath, source, fill.CachingEvolution,
             out_filepath, max_generations, pool_size,
             selection, crossover, mutation_rate, mutation, elitism)))
    for result in results:
        tot_score += result.get()
    print('\nTOTAL SCORE: {}\n'.format(tot_score))


# ======================================================================
def main():
    print(__doc__)
    begin_time = datetime.datetime.now()

    # test_network_input()
    # test_caching_output()
    # test_score()
    # test_fill()
    # pseudo_monte_carlo()
    # bruteforce()
    # montecarlo(sources=(SOURCES[3],))
    evolution(sources=(SOURCES[1],))

    end_time = datetime.datetime.now()
    print('\nExecTime: {}'.format(end_time - begin_time))


# ======================================================================
if __name__ == '__main__':
    main()