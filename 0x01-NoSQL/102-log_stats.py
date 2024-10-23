#!/usr/bin/env python3
"""Provides enhanced stats about Nginx logs in MongoDB"""
from pymongo import MongoClient


def print_nginx_stats():
    """Prints statistics about Nginx logs including top 10 IPs"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})
    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = logs_collection.count_documents({"method": method})
        print(f"    method {method}: {count}")

    status_check = logs_collection.count_documents({
        "method": "GET",
        "path": "/status"
    })
    print(f"{status_check} status check")

    print("IPs:")
    top_ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    for ip_info in top_ips:
        print(f"    {ip_info['_id']}: {ip_info['count']}")


if __name__ == "__main__":
    print_nginx_stats()
