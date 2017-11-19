from pymongo import MongoClient
from urllib.parse import quote_plus  # Python 3.x


class MongoDBConnection:
    def __init__(self, host="127.0.0.1", port=27017, username=None, passwd=None):
        if username is not None or passwd is not None:
            self._connection = MongoClient(
                "mongodb://%s:%s@%s:%d" % (
                    quote_plus(username),
                    quote_plus(passwd),
                    host,
                    port)
            )
        else:
            self._connection = MongoClient(host, port)

    def __enter__(self):
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


if __name__ == "__main__":
    print("from utility import connection")
