#!/usr/bin/env python3

"""
Python script that provides some stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def print_nginx_logs(db_collection):
    """
    Print the statistics of nginx logs.

    Args:
      db_collection: The MongoDB collection containing the nginx logs.

    Returns:
      None

    Prints the total number of logs in the collection,
    followed by the count of each HTTP method used in the logs.
    Additionally, it prints the count of status checks made
    to the "/status" path.

    Example:
      >>> print_nginx_logs(db_collection)
      1000 logs
      Methods:
        method GET: 500
        method POST: 200
        method PUT: 100
        method PATCH: 50
        method DELETE: 150
      10 status check
    """
    print("{} logs".format(db_collection.count_documents({})))
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        req_count = len(list(db_collection.find({"method": method})))
        print("\tmethod {}: {}".format(method, req_count))

    status_checks_count = len(
        list(db_collection.find({"method": "GET", "path": "/status"}))
    )
    print("{} status check".format(status_checks_count))


def run():
    """
    This function connects to a MongoDB server and prints the nginx logs.

    Parameters:
      None

    Returns:
      None
    """

    client = MongoClient("mongodb://127.0.0.1:27017")
    print_nginx_logs(client.logs.nginx)


if __name__ == "__main__":
    run()
