#!/usr/bin/env python3

"""
Python function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    Retrieves the top students from a MongoDB collection
    based on their average score.

    Args:
      mongo_collection (pymongo.collection.Collection):
      The MongoDB collection to query.

    Returns:
      pymongo.command_cursor.CommandCursor: A cursor
      object containing the top students.

    Raises:
      None.
    """
    students = mongo_collection.aggregate(
        [
            {
                "$project": {
                    "_id": 1,
                    "name": 1,
                    "averageScore": {
                        "$avg": {
                            "$avg": "$topics.score",
                        },
                    },
                    "topics": 1,
                },
            },
            {
                "$sort": {"averageScore": -1},
            },
        ]
    )
    return students
