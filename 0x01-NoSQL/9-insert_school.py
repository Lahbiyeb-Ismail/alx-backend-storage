#!/usr/bin/env python3

"""
Python function that inserts a new document in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into the specified MongoDB collection.

    Args:
      mongo_collection (pymongo.collection.Collection):
      The MongoDB collection to insert the document into.
      **kwargs: The key-value pairs representing the fields
      and values of the document to be inserted.

    Returns:
      ObjectId: The unique identifier of the inserted document.
    """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
