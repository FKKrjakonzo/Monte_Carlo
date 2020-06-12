#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

SIZE_X = 20
SIZE_Y = 18

"""
Creation of map [SIZE_X, SIZE_Y]

"""
def create_map(count=10):
    map_array = []
    for i in range(SIZE_X):
        for u in range(SIZE_Y):
            if i == 0 or i == SIZE_X - 1 or u == 0 or u == SIZE_Y - 1:
                map_array.append([i, u])
    for i in range(count):
        x = np.random.randint(0, SIZE_X - 2)
        y = np.random.randint(0, SIZE_Y - 2)

        while [x, y] in map_array or [x + 1, y + 1] in map_array or [x
                + 1, y] in map_array or [x, y + 1] in map_array or x \
            == 0 and y == 9 or x == 17 and y == 9:

            x = np.random.randint(0, SIZE_X - 2)
            y = np.random.randint(0, SIZE_Y - 2)
        map_array.append([x, y])
        map_array.append([x + 1, y])
        map_array.append([x, y + 1])
        map_array.append([x + 1, y + 1])
    while path_len(map_array) == 0:
        map_array = create_map(count)

    return map_array


def pathfind(blocks, less=False):
    matrix = np.ones((SIZE_X, SIZE_Y))
    for i in blocks:
        matrix[i[0]][i[1]] = 0

    matrix[0][10] = 1
    matrix[0][9] = 1
    matrix[19][10] = 1
    matrix[19][9] = 1

    grid = Grid(matrix=matrix)
    start = grid.node(10, 0)
    end = grid.node(10, 19)
    if less:
        finder = AStarFinder(diagonal_movement=1)
    else:
        finder = AStarFinder(diagonal_movement=2)
    (path, runs) = finder.find_path(start, end, grid)

    return path


def path_len(blocks, less=False):
    return len(pathfind(blocks, less))


def free(blocks):
    matrix = np.ones((SIZE_X, SIZE_Y))
    new_list = []
    for i in blocks:
        matrix[i[0]][i[1]] = 0
    for i in range(1, SIZE_X - 1):
        for u in range(1, SIZE_Y - 1):

            if matrix[i][u] == 1 and matrix[i + 1][u] == 1 \
                and matrix[i][u + 1] == 1 and matrix[i + 1][u + 1] == 1:
                new_list.append([i, u])
    return new_list


def free_test(blocks):
    matrix = np.ones((SIZE_X, SIZE_Y))
    new_list = []
    for i in blocks:
        matrix[i[0]][i[1]] = 0
    for i in range(1, SIZE_X - 1):
        for u in range(1, SIZE_Y - 1):

            if matrix[i][u] == 1 and matrix[i + 1][u] == 1 \
                and matrix[i][u + 1] == 1 and matrix[i + 1][u + 1] == 1:
                new_list.append([i, u])
    test = pathfind(blocks)
    for i in new_list:
        if i not in test:
            new_list.remove(i)
    return new_list


def free_1(blocks):
    matrix = np.ones((SIZE_X, SIZE_Y))
    new_list = []
    for i in blocks:
        matrix[i[0]][i[1]] = 0
    pocet = 0
    for i in range(1, SIZE_X - 1):
        for u in range(1, SIZE_Y - 1):
            pocet += 1
            if matrix[i][u] == 1 and matrix[i + 1][u] == 1 \
                and matrix[i][u + 1] == 1 and matrix[i + 1][u + 1] == 1:
                new_list.append(pocet)
    return new_list


def flat(new_list):
    m = 1
    for i in new_list:
        m = m + i[0]
    m = int(m)
    return m


def action(value):
    m = 0
    for i in range(1, SIZE_X - 1):
        for u in range(1, SIZE_Y - 1):
            if m == value:
                return [i, u]
            m += 1
    return [17, 15]
