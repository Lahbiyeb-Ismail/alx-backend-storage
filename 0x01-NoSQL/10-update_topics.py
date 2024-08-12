#!/usr/bin/env python3


"""
Python function that changes all topics of a school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """
    Update the 'topics' field of a document in the given MongoDB collection.

    Args:
      mongo_collection (pymongo.collection.Collection):
      The MongoDB collection to update.
      name (str): The name of the document to update.
      topics (list): The new list of topics to set for the document.

    Returns:
      None
    """
    mongo_collection.update({"name": name}, {"$set": {"topics": topics}})
