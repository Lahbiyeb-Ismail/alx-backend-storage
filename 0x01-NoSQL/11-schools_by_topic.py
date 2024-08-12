#!/usr/bin/env python3

"""
Python function that returns the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Retrieve a list of schools from the given MongoDB
    collection that match the specified topic.

    Args:
      mongo_collection (pymongo.collection.Collection):
      The MongoDB collection to query.
      topic (str): The topic to filter schools by.

    Returns:
      list: A list of documents representing schools that
      match the specified topic.
    """
    topic_filter = {
        "topics": {
            "$elemMatch": {
                "$eq": topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter)]
