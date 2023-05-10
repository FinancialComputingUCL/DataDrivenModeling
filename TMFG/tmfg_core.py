import copy
from itertools import combinations, chain
from numpy.linalg import inv

from TMFG.utils import *

import pandas as pd

class Fast_TMFG:
    def __init__(self):
        pass

    def fit(self, c_matrix, cov_matrix, logo=False):
        '''
        The `fit` method is a member of the `Fast_TMFG` class. It is used to fit the model to the input matrix `c_matrix`.

        The method does the following:

        - It sets the instance variable `W` to the input matrix `c_matrix` (a correlation matrix).
        - It creates a copy of `c_matrix` and sets it to the instance variable `original_W`.
        - It sets the instance variable `N` to the number of columns in `c_matrix`.
        - It initializes the instance variable `P` to an NxN matrix of zeros.
        - It initializes the instance variable `max_clique_gains` to an array of zeros with length (3 * N) - 6.
        - It initializes the instance variable `best_vertex` to an array of -1s with length (3 * N) - 6.
        - It initializes the instance variables `cliques`, `separators`, and `triangles` to empty lists.
        - It initializes the instance variables `vertex_list`, `peo`, and `JS` to None.
        
        After this method is called, the instance variables will be set and the model will be ready to compute the Triangulated Maximal Filtered Graph (TMFG).
        '''

        self.W = c_matrix
        self.original_W = copy.copy(c_matrix)
        self.cov_matrix = cov_matrix
        self.logo = logo

        self.N = self.W.shape[1]
        self.P = np.zeros((self.N, self.N))
        self.max_clique_gains = np.zeros(((3 * self.N) - 6))
        self.best_vertex = np.array([-1] * ((3 * self.N) - 6))

        self.cliques = []
        self.separators = []
        self.triangles = []

        self.vertex_list = None
        self.peo = None
        self.JS = None

        self.cliques, self.separators, self.JS = self.__compute_TMFG()

    def transform(self):
        return self.cliques, self.separators, self.JS

    def fit_transform(self, c_matrix, cov_matrix, logo=False):
        self.fit(c_matrix, cov_matrix, logo)
        return self.cliques, self.separators, self.JS

    def __compute_TMFG(self):
        '''
        The `__compute_TMFG` method is a helper method of the `Fast_TMFG` class that computes the Triangulated Maximal Filtered Graph (TMFG) based on the input matrix.

        The method does the following:

        - It computes the maximum clique of the input matrix and appends it to the list of cliques.
        - It creates a list of vertices that are not in the maximum clique and sets it to the `vertex_list` instance variable.
        - It creates four triangles based on the vertices in the maximum clique and appends them to the `triangles` list.
        - It sets the `peo` instance variable to a copy of the maximum clique.
        - It sets the main diagonal of the `W` matrix to zeros.
        - It creates a list of all combinations of two vertices from the maximum clique and sets it to `peo_combinations_list`.
        - It sets the elements in the `P` matrix to the corresponding elements in the `W` matrix for each combination in `peo_combinations_list`.
        - It iterates through each triangle in the `triangles` list and computes the best gain and best vertex for each one. It sets the best gain and best vertex for each triangle to the corresponding element in the `max_clique_gains` and `best_vertex` arrays, respectively.
        - It iterates through each vertex in the `vertex_list` and performs the following actions:
            . It selects the triangle with the highest maximum clique gain.
            . It selects the best vertex for that triangle.
            . It adds the best vertex to the `peo` list.
            . It creates a thetraedron with the best vertex and the vertices in the selected triangle.
            . It appends the thetraedron to the `cliques` list.
            . It sets the `newsep` variable to the selected triangle.
            . It creates a list of all combinations of two vertices from the thetraedron and sets it to `peo_combinations_list`.
            . It sets the elements in the `P` matrix to the corresponding elements in the `W` matrix for each combination in `peo_combinations_list`.
            . It adds the `newsep` variable to the separators list.
            . It updates the selected triangle by replacing one of its vertices with the best vertex and adding two new triangles with the remaining two vertices and the best vertex.
            . It removes the best vertex from the `vertex_list`.
            . It creates a list of vertices that are not in the `vertex_list` and sets it to `no_vertex_list`.
            . It finds the indices of the triangles in the `triangles` list that contain the best vertex.
            . It iterates through each index and performs the following actions:
                * It computes the best gain and best vertex for the triangle at that index.
                * It sets the best gain and best vertex for the triangle to the corresponding element in the `max_clique_gains` and `best_vertex` arrays, respectively.
        '''


        self.cliques.append(list(max_clique(self.W)))
        self.vertex_list = np.setdiff1d(range(self.N), self.cliques[0])

        self.triangles.append(list(pd.Series(self.cliques[0])[[0, 1, 2]]))
        self.triangles.append(list(pd.Series(self.cliques[0])[[0, 1, 3]]))
        self.triangles.append(list(pd.Series(self.cliques[0])[[0, 2, 3]]))
        self.triangles.append(list(pd.Series(self.cliques[0])[[1, 2, 3]]))

        self.peo = copy.copy(self.cliques[0])
        self.W = np.array(self.W)
        self.W[np.diag_indices_from(self.W)] = 0

        peo_combinations_list = []
        for n in range(len(self.cliques[0]) + 1):
            two_d_lists = len(list(combinations(self.cliques[0], n))[0])
            if two_d_lists == 2:
                peo_combinations_list += list(combinations(self.cliques[0], n))

        for i in peo_combinations_list:
            self.P[int(i[0]), int(i[1])] = self.W[int(i[0]), int(i[1])]

        for t in range(0, 4):
            index_max, max_element = get_best_gain(self.N, self.vertex_list, self.triangles[t], self.W, None)
            self.max_clique_gains[t] = max_element
            self.best_vertex[t] = index_max

        for u in range(0, (self.N - 4)):
            nt = np.argmax(self.max_clique_gains)
            nv = self.best_vertex[nt]
            self.peo.append(nv)

            thetraedron = [nv] + self.triangles[nt]
            self.cliques.append(thetraedron)
            newsep = self.triangles[nt]

            peo_combinations_list = []
            thetraedron_tbc = [nv] + newsep
            for n in range(len(thetraedron_tbc) + 1):
                two_d_lists = len(list(combinations(thetraedron_tbc, n))[0])
                if two_d_lists == 2:
                    peo_combinations_list += list(combinations(thetraedron_tbc, n))

            for i in peo_combinations_list:
                self.P[int(i[0]), int(i[1])] = self.W[int(i[0]), int(i[1])]

            self.separators.append(newsep)
            self.triangles[nt] = [newsep[0], newsep[1], nv]
            self.triangles.append([newsep[0], newsep[2], nv])
            self.triangles.append([newsep[1], newsep[2], nv])
            self.vertex_list = np.setdiff1d(self.vertex_list, nv)

            no_vertex_list = np.setdiff1d(range(self.N), self.vertex_list)

            if len(self.vertex_list) > 0:
                indices_of_interest = np.argwhere(self.best_vertex == nv)
                indices_of_interest = list(chain(*indices_of_interest))

                for t in indices_of_interest:
                    index_max, max_element = get_best_gain(self.N, self.vertex_list, self.triangles[t], self.W, no_vertex_list)
                    self.max_clique_gains[t] = max_element
                    self.best_vertex[t] = index_max

            self.max_clique_gains[nt] = 0
            ct = len(self.triangles) - 1
            if len(self.vertex_list) > 0:
                for t in [nt, (ct - 1), ct]:
                    index_max, max_element = get_best_gain(self.N, self.vertex_list, self.triangles[t], self.W, no_vertex_list)
                    self.max_clique_gains[t] = max_element
                    self.best_vertex[t] = index_max

        if self.logo:
            self.__logo()
        else:
            self.__unweighted_tmfg()
        return self.cliques, self.separators, self.JS

    def __unweighted_tmfg(self):
        '''
        The `__unweighted_tmfg` method is a helper method of the `Fast_TMFG` class that initializes the instance variable `JS` to an NxN matrix of zeros, where `N` is the number of rows in the `original_W` matrix. Then it iterates through the list of cliques and sets the elements in the `JS` matrix corresponding to the vertices in each clique to 1. Finally, it sets the main diagonal of the `JS` matrix to 0.

        This code is creating a matrix representation of the Triangulated Maximal Filtered Graph (TMFG). The resulting `JS` matrix will have a value of 1 for each pair of vertices that are connected in the TMFG and a value of 0 for each pair that are disconnected.
        '''
        self.JS = np.zeros((self.original_W.shape[0], self.original_W.shape[0]))
        for c in self.cliques:
            self.JS[np.ix_(c, c)] = np.array(self.original_W)[np.ix_(c, c)]#1

        np.fill_diagonal(self.JS, 0)

    def __logo(self):
        self.JS = np.zeros((self.original_W.shape[0], self.original_W.shape[0]))
        W = self.cov_matrix.to_numpy()

        for c in self.cliques:
            self.JS[np.ix_(c, c)] = self.JS[np.ix_(c, c)] + inv(W[np.ix_(c, c)])

        for s in self.separators:
            self.JS[np.ix_(s, s)] = self.JS[np.ix_(s, s)] - inv(W[np.ix_(s, s)])

        np.fill_diagonal(self.JS, 0)