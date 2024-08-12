#!/usr/bin/env python3

"""
Print statistics about nginx logs.
"""

from pymongo import MongoClient


def print_nginx_logs(db_collection):
    """
    Print statistics about nginx logs.

    Args:
      db_collection (pymongo.collection.Collection):
      The MongoDB collection containing the nginx logs.

    Returns:
      None

    Prints the following statistics:
    - Total number of logs in the collection.
    - Number of logs for each HTTP method (GET, POST, PUT, PATCH, DELETE).
    - Number of status check logs (GET requests to "/status").
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


def print_top_ips(server_collection):
    """
    Print the top 10 IP addresses with the highest number of requests.

    Args:
      server_collection (pymongo.collection.Collection):
      The collection object representing the server logs.

    Returns:
      None

    Raises:
      None
    """
    print("IPs:")

    request_logs = server_collection.aggregate(
        [
            {"$group": {"_id": "$ip", "totalRequests": {"$sum": 1}}},
            {"$sort": {"totalRequests": -1}},
            {"$limit": 10},
        ]
    )

    for request_log in request_logs:
        ip = request_log["_id"]
        ip_requests_count = request_log["totalRequests"]
        print("\t{}: {}".format(ip, ip_requests_count))


def run():
    """
    This function connects to a MongoDB server and performs
    the following operations:
    1. Prints the nginx logs.
    2. Prints the top IPs from the nginx logs.
    """
    client = MongoClient("mongodb://127.0.0.1:27017")
    print_nginx_logs(client.logs.nginx)
    print_top_ips(client.logs.nginx)


if __name__ == "__main__":
    run()
