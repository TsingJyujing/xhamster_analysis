import numpy
from typing import Set, List
import time
from utils import save_compressed_json
import scipy.sparse
import os


class SparseKMeans:
    def __init__(self, data: List[Set[int]], dim: int, center_count: int = 6):
        self.__dim = dim
        self.__k = center_count
        self.data = data
        self.current_centers = numpy.random.rand(self.k, self.dim)
        self.current_labels = None
        self.diff_counts = len(data)
        print("Sparse K-Means initialized.")

    @property
    def k(self):
        return self.__k

    @property
    def dim(self):
        return self.__dim

    def fit(self, max_iter: int = 100, break_diff: int = 2):
        sum_break = 0
        for i in range(max_iter):
            if sum_break <= break_diff:
                start_tick = time.time()
                self.__update()
                numpy.savez_compressed("temp/kmeans_centers.npz",
                                       centers=self.current_centers,
                                       labels=self.current_labels
                                       )
                passed_time = time.time() - start_tick
                print("Ran 1 iter in {}s,difference count: {}".format(passed_time, self.diff_counts))
                if self.diff_counts == 0:
                    sum_break += 1
            else:
                break

    def __update(self):
        norms = [numpy.linalg.norm(vec) for vec in self.current_centers]
        point_count = numpy.zeros((self.k,), dtype=numpy.int)
        new_centers = numpy.zeros((self.k, self.dim), dtype=numpy.float)
        new_labels = numpy.zeros((len(self.data),), dtype=numpy.int)
        start = time.time()
        for index, data_unit in enumerate(self.data):
            # Calc distance to each center
            if index % 10000 == 9999:
                tps = (time.time() - start) * 1000.0 / index
                print("TPmS:{}".format(tps))
            squared_distances = [
                norms[i] + (
                    len(data_unit) - 2 * self.current_centers[i][data_unit].sum()
                )
                for i in range(self.k)
            ]
            # Decision which center to use
            center = squared_distances.index(min(squared_distances))
            new_labels[index] = center
            point_count[center] += 1
            for tag_index in data_unit:
                new_centers[center][tag_index] += 1
        for i in range(self.k):
            new_centers[i] /= (point_count[i] * 1.0)
        if self.current_labels is not None:
            self.diff_counts = sum((1 for a, b in zip(new_labels, self.current_labels) if a != b))
        self.current_labels = new_labels
        self.current_centers = new_centers


class SparseMatrixKMeans:
    def __init__(self, data: scipy.sparse.spmatrix, dim: int, center_count: int = 6):
        self.__dim = dim
        self.__k = center_count
        self.data = data.tocsc()
        self.__k_means_plus()
        self.current_labels = None
        self.diff_counts = data.shape[0]
        print("Sparse matrix K-Means initialized.")

    @property
    def k(self):
        return self.__k

    @property
    def dim(self):
        return self.__dim

    def __get_distance_to_data(self, points: numpy.ndarray):
        k, dim = points.shape
        N = self.data.shape[0]
        assert dim == self.dim, "Dim is not match."
        D = numpy.array(self.data.multiply(self.data).sum(axis=1)).repeat(k, axis=1)
        D += numpy.matrix((points * points).sum(axis=1)).repeat(N, axis=0)
        D -= 2 * self.data.dot(points.transpose())
        return D

    def __k_means_plus(self):
        self.current_centers = numpy.zeros(shape=(self.k, self.dim))
        print("K-means ++ initializing...")
        if os.path.exists("temp/kmeans_plus_initialized.npz"):
            self.current_centers = numpy.load("temp/kmeans_plus_initialized.npz")["initial_points"]
            return
        for k in range(self.k):
            if k == 0:
                self.current_centers[k] = self.data[0].toarray()
            else:
                min_distance = numpy.min(
                    self.__get_distance_to_data(
                        self.current_centers[range(k)]
                    ), axis=1)
                self.current_centers[k] = self.data[min_distance.argmax()].toarray()
            print("K-Means++ : {}/{} centers initialized.".format(k + 1, self.k))
        numpy.savez_compressed("temp/kmeans_plus_initialized.npz", initial_points=self.current_centers)
        print("K-means ++ initialized.")

    def fit(self, max_iter: int = 100, break_diff: int = 2):
        sum_break = 0
        for i in range(max_iter):
            if sum_break <= break_diff:
                start_tick = time.time()
                self.__update()
                passed_time = time.time() - start_tick
                print("Ran 1 iter in {}s,difference count: {}".format(passed_time, self.diff_counts))
                numpy.savez_compressed("temp/kmeans_centers.npz",
                                       centers=self.current_centers,
                                       labels=self.current_labels
                                       )
                if self.diff_counts == 0:
                    sum_break += 1
            else:
                break

    def __update(self):

        distance_matrix = self.__get_distance_to_data(self.current_centers)
        center_select_result = numpy.argmin(distance_matrix, axis=0)
        classes = numpy.unique(center_select_result)
        new_k = len(classes)
        new_centers = numpy.zeros((new_k, self.dim), dtype=numpy.float)
        if self.k < new_k:
            print("K from {} shrinked to {}".format(self.k, new_k))
        self.__k = new_k
        for ik in range(new_k):
            new_centers[ik] = numpy.mean(self.data[numpy.where(center_select_result == classes[ik])], axis=0)

        if self.current_labels is not None:
            print("self.current_labels: Shape={},Data type={}".format(self.current_labels.shape,self.current_labels.dtype))
            print("center_select_result: Shape={},Data type={}".format(center_select_result.shape,
                                                                       center_select_result.dtype))
            self.diff_counts = numpy.logical_and(self.current_labels, center_select_result).sum()
        self.current_labels = center_select_result
        self.current_centers = new_centers
