from typing import Dict, List, Set, Tuple
from scipy import sparse
import numpy as np
from config import url_prefix, duration_limit
from utils.connection import MongoDBConnection


def static_all_set() -> Dict[str, int]:
    labels_static: Dict[str, int] = dict()
    with MongoDBConnection() as mgconn:
        coll = mgconn.get_database("spider").get_collection("xhamster_storage")
        for doc in coll.find({"duration":{"$gte":duration_limit}}, {"label": 1}): 
            for label in doc["label"]:
                if label in labels_static:
                    labels_static[label] += 1
                else:
                    labels_static[label] = 1
    return labels_static


def get_index_dict(static_dict: List[str]) -> Dict[str, int]:
    return {label: index for index, label in enumerate(static_dict)}


def get_sparse_matrix(label_index: Dict[str, int]):
    urls_key = list()
    i: List[int] = list()
    j: List[int] = list()
    with MongoDBConnection() as mgconn:
        coll = mgconn.get_database("spider").get_collection("xhamster_storage")
        for index, doc in enumerate(coll.find({"duration":{"$gte":duration_limit}}, {"label": 1, "_id": 1})):
            urls_key.append(doc["_id"].replace(url_prefix, ""))
            for label in doc["label"]:
                i.append(index)
                j.append(label_index[label])
    i = np.asarray(i)
    j = np.asarray(j)
    sparse_matrix = sparse.coo_matrix((i * 0 + 1, (i, j)), dtype=np.float)
    return urls_key, sparse_matrix


def get_sparse_data(label_index: Dict[str, int]) -> Tuple[list, List[Set[int]]]:
    urls_key = list()
    data: List[Set[int]] = list()
    with MongoDBConnection() as mgconn:
        coll = mgconn.get_database("spider").get_collection("xhamster_storage")
        for index, doc in enumerate(coll.find({"label": {"$ne": None},"duration":{"$gte":duration_limit}}, {"label": 1, "_id": 1})):
            urls_key.append(doc["_id"].replace(url_prefix, ""))
            data.append(label_index[label] for label in doc["label"])
    return urls_key, data
