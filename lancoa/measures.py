#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Domagoj Margan <margan.domagoj@gmail.com>

This file is part of LaNCoA.
LaNCoA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LaNCoA is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LaNCoA.  If not, see <http://www.gnu.org/licenses/>.
"""

import networkx as nx
import math

__author__ = "Domagoj Margan"
__email__ = "margan.domagoj@gmail.com"
__copyright__ = "Copyright 2015, Domagoj Margan"
__license__ = "GPL"


def in_selectivity(network):
    """Calculate in-selectivity for each node
    in graph and write results in dictionary.

    Parameters
    ----------
    network : edge list of the network

    Returns
    -------
    selectivity_dict : dict
        a dictionary where keys are graph nodes
        and values are calculated in-selectivity
    """
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())

    selectivity_dict = {}
    for node in g.nodes():
        s = g.in_degree(node, weight='weight')
        k = g.in_degree(node, weight=None)
        if k > 0:
            selectivity = s / k
            selectivity_dict[node] = selectivity
        else:
            selectivity_dict[node] = 0

    return selectivity_dict


def out_selectivity(network):
    """Calculate out-selectivity for each node
    in graph and write results in dictionary.

    Parameters
    ----------
    network : edge list of network

    Returns
    -------
    selectivity_dict : dict
        a dictionary where keys are graph nodes
        and values are calculated out-selectivity
    """
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())

    selectivity_dict = {}
    for node in g.nodes():
        s = g.out_degree(node, weight='weight')
        k = g.out_degree(node, weight=None)
        if k > 0:
            selectivity = s / k
            selectivity_dict[node] = selectivity
        else:
            selectivity_dict[node] = 0

    return selectivity_dict


def selectivity(network):
    """Calculate selectivity for each node
    in graph and write results in dictionary.

    Parameters
    ----------
    network : edge list of network

    Returns
    -------
    selectivity_dict : dict
        a dictionary where keys are graph nodes
        and values are calculated selectivity
    """
    g = nx.read_weighted_edgelist(network)

    selectivity_dict = {}
    for node in g.nodes():
        s = g.degree(node, weight='weight')
        k = g.degree(node, weight=None)
        if k > 0:
            selectivity = s / k
            selectivity_dict[node] = selectivity
        else:
            selectivity_dict[node] = 0

    return selectivity_dict


def in_ipr(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())

    inv_part_dict = {}
    for node in g.nodes():
        s = g.in_degree(node, weight='weight')
        predcessors = g.predecessors(node)
        if len(predcessors) == 0 and s == 0:
            inv_part_dict[node] = 0
        else:
            sum_list = []
            for in_node in predcessors:
                a = g.edge[in_node][node]['weight']
                sum_list.append(math.pow((float(a) / float(s)), 2))
                inv_part_dict[node] = sum(sum_list)

    return inv_part_dict


def out_ipr(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())

    inv_part_dict = {}
    for node in g.nodes():
        s = g.out_degree(node, weight='weight')
        successors = g.successors(node)
        if len(successors) == 0 and s == 0:
            inv_part_dict[node] = 0
        else:
            sum_list = []
            for out_node in successors:
                a = g.edge[node][out_node]['weight']
                sum_list.append(math.pow((float(a) / float(s)), 2))
                inv_part_dict[node] = sum(sum_list)

    return inv_part_dict


def reciprocity(network):
    """Returns reciprocity of the given network.

    Parameters
    ----------
    network : edge list of the network

    Returns
    -------
    r : float
        network reciprocity
    a : float
        the ratio of observed to possible directed links
    ro : float
        Garlaschelli and Loffredo's definition of reciprocity
    """
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())

    self_loops = g.number_of_selfloops()
    r = sum([g.has_edge(e[1], e[0])
                    for e in g.edges_iter()]) / float(g.number_of_edges())

    a = (g.number_of_edges() - self_loops) / (float(g.number_of_nodes()) * float((g.number_of_nodes() - 1)))

    ro = float((r - a)) / float((1 - a))

    return r, a, ro


def entropy(values_dict):
    """Returns entropy of the given measure.

    Parameters
    ----------
    values_dict : dict
        dictionary where keys are graph nodes
        and values are numbers representing some
        measure, e.g. selectivity

    Returns
    -------
    entropy : float
    """
    n = len(values_dict)

    entropy = 0

    values_sum = sum(values_dict.values())

    for k, v in values_dict.iteritems():
        if v > 0:
            entropy += ((v / float(values_sum)) * (math.log(v / float(values_sum))))

    entropy = -entropy / math.log(n)

    return entropy