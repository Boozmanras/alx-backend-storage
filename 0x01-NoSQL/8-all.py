#!/usr/bin/env python3
"""List all documents in Python"""


def list_all(mongo_collection):
    """Lists all documents in a collection
    Return empty list if no documents"""
    return list(mongo_collection.find())
