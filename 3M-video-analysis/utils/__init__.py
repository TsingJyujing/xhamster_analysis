import json
import gzip

def save_json(obj: object, filename: str):
    with open(filename, "w", encoding="UTF-8") as fp:
        json.dump(obj, fp)
        print("JSON {} saved.".format(filename))

def save_compressed_json(obj: object, filename: str):
    with gzip.GzipFile(mode="wb", compresslevel=9, fileobj=open(filename, "wb")) as fp:
        fp.write(json.dumps(obj).encode("UTF-8"))
        print("JSON(zipped) {} saved.".format(filename))

def load_compressed_json(filename: str):
    with gzip.GzipFile(mode="rb", fileobj=open(filename, "rb")) as fp:
        return json.loads(fp.read().decode("UTF-8"))