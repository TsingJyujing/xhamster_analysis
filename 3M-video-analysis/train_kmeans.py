from utils import load_compressed_json, save_compressed_json
from utils.sparse_kmeans import SparseMatrixKMeans as KMeansImplement
import numpy
from scipy.sparse import load_npz


def main():
    # data = load_compressed_json("temp/kmeans_data.json.gz")
    data = load_npz("temp/sparse_matrix.npz")
    label_list = load_compressed_json("temp/index_list.json.gz")
    sp_k_means = KMeansImplement(data, len(label_list), 200)
    sp_k_means.fit(300, 10)
    labels = sp_k_means.current_labels
    centers = sp_k_means.current_centers
    numpy.savez_compressed("temp/kmeans_centers.npz", centers=centers)
    save_compressed_json(labels.tolist(), "temp/kmeans_result.json.gz")


if __name__ == "__main__":
    main()
