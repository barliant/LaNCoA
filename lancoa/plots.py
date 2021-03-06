#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Tanja Miličić <tanyamilicic@gmail.com>

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

import measures
import matplotlib.pyplot as plt
import networkx as nx

__author__ = "Tanja Miličić"
__email__ = "tanyamilicic@gmail.com"
__copyright__ = "Copyright 2015, Tanja Miličić"
__license__ = "GPL"


def draw_rank_plot(name, networks, d="undirected", m="selectivity"):
    """Draws rank plot of specified measure for
    one or more given networks.


    Parameters
    ----------
    name : string
        name of file that will be created
    networks : edge list or array of edge lists
    d : in, out or undirected
        direction that will be used in calculating
        node measure
    m : selectivity, degree or strength
        network measure that will be plotted
    """
    figname = str(name)
    colors = ["blue", "red", "green", "cyan", "magenta", "yellow"]
    markers = ["o", "v", "^", "s", "*", "p"]
    idx = 0

    is_array = lambda var: isinstance(var, (list, tuple))

    if is_array(networks):
        for net in networks:
            measure = measure_dict(net, m, d)
            measure_sequence = sorted(measure.values(), reverse=True)
            plt.loglog(measure_sequence, 'b-', color=colors[idx],
                       lw=3, alpha=0.7, marker=markers[idx],
                       label=net.rsplit(".", 1)[0])
            plt.savefig(figname)
            idx += 1
    else:
        measure = measure_dict(networks, m, d)
        measure_sequence = sorted(measure.values(), reverse=True)
        plt.loglog(measure_sequence, 'b-', color=colors[0],
                   lw=3, alpha=0.7, marker=markers[0],
                   label=networks.rsplit(".", 1)[0])
        plt.savefig(figname)

    plt.xlabel("rank")
    if d != "undirected":
        plt.ylabel(d + "-" + m)
    else:
        plt.ylabel(m)
    plt.legend(loc=1, shadow=True)
    plt.savefig(figname)
    plt.clf()


def draw_histogram(name, network, d="undirected", m="selectivity"):
    """Draws histogram of specified measure for given network.

    Parameters
    ----------
    name : string
        name of file that will be created
    networks : network edge list
    d : in, out or undirected
        direction that will be used in calculating
        node measure
    m : selectivity, degree or strength
        network measure that will be plotted
    """
    figname = str(name)
    measure_sequence = measure_dict(network, m, d).values()
    plt.hist(measure_sequence, facecolor="blue",
             alpha=0.75, label=network.rsplit(".", 1)[0])

    plt.ylabel("nodes")
    if d != "undirected":
        plt.xlabel(d + "-" + m)
    else:
        plt.xlabel(m)
    plt.legend(loc=1, shadow=True)
    plt.savefig(figname)
    plt.clf()

def draw_scatterplot(name, networks, d="undirected", xm="selectivity", ym="strength"):
    """Draws scatter plot of specified measures for
    one or more given networks.

    Parameters
    ----------
    name : string
        name of file that will be created
    networks : edge list or array of edge lists
    d : in, out or undirected
        direction that will be used in calculating
        node measure
    xm : selectivity, degree or strength
        network measure for x axis
    ym : selectivity, degree or strength
        network measure for y axis
    """
    figname = str(name)
    colors = ["blue", "red", "green", "cyan", "magenta", "yellow"]
    area = 30
    idx = 0

    is_array = lambda var: isinstance(var, (list, tuple))

    if is_array(networks):
        for net in networks:
            x = measure_dict(net, xm, d).values()
            y = measure_dict(net, ym, d).values()
            plt.scatter(x, y, s=area, c=colors[idx], alpha=0.7,
                        label=net.rsplit(".", 1)[0])
            plt.savefig(figname)
            idx += 1
    else:
        x = measure_dict(networks, xm, d).values()
        y = measure_dict(networks, ym, d).values()
        plt.scatter(x, y, s=area, c=colors[0], alpha=0.7,
                    label=networks.rsplit(".", 1)[0])
        plt.savefig(figname)

    if d != "undirected":
        plt.ylabel(d + "-" + ym)
        plt.xlabel(d + "-" + xm)
    else:
        plt.ylabel(ym)
        plt.xlabel(xm)
    plt.legend(loc=1, shadow=True)
    plt.savefig(figname)
    plt.clf()


def measure_dict(net, m="selectivity", d="undirected"):
    if d == "out":
        if m == "selectivity":
            measure = measures.out_selectivity(net)
        elif m == "degree":
            g = nx.read_weighted_edgelist(net, create_using=nx.DiGraph())
            measure = g.out_degree()
        elif m == "strength":
            g = nx.read_weighted_edgelist(net, create_using=nx.DiGraph())
            measure = g.out_degree(weight='weight')

    elif d == "in":
        if m == "selectivity":
            measure = measures.in_selectivity(net)
        elif m == "degree":
            g = nx.read_weighted_edgelist(net, create_using=nx.DiGraph())
            measure = g.in_degree()
        elif m == "strength":
            g = nx.read_weighted_edgelist(net, create_using=nx.DiGraph())
            measure = g.in_degree(weight='weight')

    elif d == "undirected":
        if m == "selectivity":
            measure = measures.selectivity(net)
        elif m == "degree":
            g = nx.read_weighted_edgelist(net)
            measure = g.degree()
        elif m == "strength":
            g = nx.read_weighted_edgelist(net)
            measure = g.degree(weight='weight')

    return measure
