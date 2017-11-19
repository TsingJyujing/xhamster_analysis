from data.raw_data_reader import *
from scipy.sparse import save_npz
from utils import save_compressed_json

def save_data_as_files():
    label_static = static_all_set()
    save_compressed_json(label_static, "temp/label_static.json.gz")
    index_list = list(label_static.keys())
    save_compressed_json(index_list, "temp/index_list.json.gz")
    index_dict = get_index_dict(index_list)
    urls_key, data = get_sparse_data(index_dict)
    save_compressed_json([list(x) for x in data], "temp/kmeans_data.json.gz")
    save_compressed_json(urls_key, "temp/urls_key.json.gz")
    urls_key, sparse_matrix = get_sparse_matrix(index_dict)
    save_npz("temp/sparse_matrix.npz", sparse_matrix)
    save_compressed_json(urls_key, "temp/urls_key_sparse.json.gz")


if __name__ == "__main__":
    save_data_as_files()
