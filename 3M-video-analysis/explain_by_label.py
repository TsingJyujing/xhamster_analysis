from typing import List, Dict, Any
from config import url_prefix
from utils import save_compressed_json, load_compressed_json
from utils.connection import MongoDBConnection
from scipy.io import loadmat


def static_by_result(results: List, keys: List[str]) -> Dict[Any, Dict[str, int]]:
    assert len(results) == len(keys), "List size not same."
    classify_dict = {k: i for k, i in zip(keys, results)}
    static_dict = dict()
    with MongoDBConnection() as mongo_conn:
        coll = mongo_conn.get_database("spider").get_collection("xhamster_storage")
        for doc in coll.find({"duration": {"$gte": 180.0}}, {"label": 1}):
            key = doc["_id"].replace(url_prefix, "")
            if key in classify_dict:
                cls = classify_dict[key]
                if cls in static_dict:
                    for label in set(doc["label"]):
                        if label in static_dict[cls]:
                            static_dict[cls][label] += 1
                        else:
                            static_dict[cls][label] = 1
                    static_dict[cls]["COUNT"] += 1
                else:
                    static_dict[cls] = {label: 1 for label in set(doc["label"])}
                    static_dict[cls]["COUNT"] = 1
        return static_dict


def print_analysis(item_count: int):
    data = load_compressed_json("temp/classfied_static.json.gz")
    for k, v in data.items():
        count = v.pop("COUNT")
        units = sorted(v.items(), key=lambda d: d[1], reverse=True)
        print("TYPE={}".format(k))
        for i in range(item_count):
            print("%s --> %f%%" % (units[i][0], units[i][1] * 100.0 / count))


def static_data():
    url_keys = load_compressed_json("temp/urls_key_sparse.json.gz")
    classfied = [str(i[0]) for i in loadmat("matlab/res127.mat")["res"]]
    save_compressed_json(static_by_result(classfied, url_keys), "temp/classfied_static.json.gz")


if __name__ == "__main__":
    print_analysis(8)
